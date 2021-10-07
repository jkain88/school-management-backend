import json
from functools import partial

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import django_filters
from django_filters.fields import MultipleChoiceField
from graphql.error import GraphQLError
from graphene_django.fields import DjangoConnectionField
from promise import Promise


def patch_pagination_args(field: DjangoConnectionField):
    """Add descriptions to pagination arguments in a connection field.

    By default Graphene's connection fields comes without description for pagination
    arguments. This functions patches those fields to add the descriptions.
    """
    field.args["first"].description = "Return the first n elements from the list."
    field.args["last"].description = "Return the last n elements from the list."
    field.args[
        "before"
    ].description = (
        "Return the elements in the list that come before the specified cursor."
    )
    field.args[
        "after"
    ].description = (
        "Return the elements in the list that come after the specified cursor."
    )

class DefaultMultipleChoiceField(MultipleChoiceField):
    default_error_messages = {"invalid_list": _("Enter a list of values.")}

    def to_python(self, value):
        if not value:
            return []
        if not isinstance(value, list):
            value = [value]
        return value

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")
        if not isinstance(value, (list, tuple)):
            raise ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        return True



class BaseDjangoConnectionField(DjangoConnectionField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        patch_pagination_args(self)


class ListObjectTypeFilter(django_filters.MultipleChoiceFilter):
    field_class = DefaultMultipleChoiceField

    def __init__(self, input_class, *args, **kwargs):
        self.input_class = input_class
        super().__init__(*args, **kwargs)


class FilterInputConnectionField(BaseDjangoConnectionField):
    def __init__(self, *args, **kwargs):
        self.filter_field_name = kwargs.pop("filter_field_name", "filter")
        self.filter_input = kwargs.get(self.filter_field_name)
        self.filterset_class = None
        if self.filter_input:
            self.filterset_class = self.filter_input.filterset_class
        super().__init__(*args, **kwargs)

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        queryset_resolver,
        max_limit,
        enforce_first_or_last,
        filterset_class,
        filters_name,
        root,
        info,
        **args,
    ):
        # Disable `enforce_first_or_last` if not querying for `edges`.
        values = [
            field.name.value for field in info.field_asts[0].selection_set.selections
        ]
        if "edges" not in values:
            enforce_first_or_last = False

        first = args.get("first")
        last = args.get("last")

        if enforce_first_or_last and not (first or last):
            raise GraphQLError(
                f"You must provide a `first` or `last` value to properly paginate "
                f"the `{info.field_name}` connection."
            )

        if max_limit:
            if first:
                assert first <= max_limit, (
                    "Requesting {} records on the `{}` connection exceeds the "
                    "`first` limit of {} records."
                ).format(first, info.field_name, max_limit)
                args["first"] = min(first, max_limit)

            if last:
                assert last <= max_limit, (
                    "Requesting {} records on the `{}` connection exceeds the "
                    "`last` limit of {} records."
                ).format(last, info.field_name, max_limit)
                args["last"] = min(last, max_limit)

        iterable = resolver(root, info, **args)

        if iterable is None:
            iterable = default_manager
        # thus the iterable gets refiltered by resolve_queryset
        # but iterable might be promise
        iterable = queryset_resolver(connection, iterable, info, args)

        on_resolve = partial(
            cls.resolve_connection, connection, args, max_limit=max_limit
        )

        iterable = cls.filter_iterable(
            iterable, filterset_class, filters_name, info, **args
        )

        if Promise.is_thenable(iterable):
            return Promise.resolve(iterable).then(on_resolve)
        return on_resolve(iterable)

    @classmethod
    def filter_iterable(cls, iterable, filterset_class, filters_name, info, **args):
        filter_input = args.get(filters_name)

        if filter_input and filterset_class:
            instance = filterset_class(
                data=dict(filter_input), queryset=iterable, request=info.context
            )
            # Make sure filter input has valid values
            if not instance.is_valid():
                raise GraphQLError(json.dumps(instance.errors.get_json_data()))
            iterable = instance.qs
        return iterable

    def get_resolver(self, parent_resolver):
        return partial(
            super().get_resolver(parent_resolver),
            self.filterset_class,
            self.filter_field_name,
        )
