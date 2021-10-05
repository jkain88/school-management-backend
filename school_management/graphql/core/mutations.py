from itertools import chain
from typing import Tuple

from django.core.exceptions import (
    ValidationError,
    ImproperlyConfigured
)
import graphene
from graphene.types.mutation import MutationOptions
from graphene_django.registry import get_global_registry
from graphql.error import GraphQLError
from graphql_jwt.exceptions import PermissionDenied

from .types import (
    Error,
    Upload
)
from .utils import (
    from_global_id_strict_type,
    get_error_fields,
    validation_error_to_error_type,
)

registry = get_global_registry()


def get_model_name(model):
    """Return name of the model with first letter lowercase."""
    model_name = model.__name__
    return model_name[:1].lower() + model_name[1:]


def get_output_fields(model, return_field_name):
    """Return mutation output field for model instance."""
    model_type = registry.get_type_for_model(model)
    if not model_type:
        raise ImproperlyConfigured(
            "Unable to find type for model %s in graphene registry" % model.__name__
        )
    fields = {return_field_name: graphene.Field(model_type)}
    return fields

class ModelMutationOptions(MutationOptions):
    exclude = None
    model = None
    return_field_name = None


class BaseMutation(graphene.Mutation):
    errors = graphene.List(
        graphene.NonNull(Error),
        description="List of errors that occurred executing the mutation.",
    )

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        description=None,
        permissions: Tuple = None,
        _meta=None,
        error_type_class=None,
        error_type_field=None,
        **options,
    ):
        if not _meta:
            _meta = MutationOptions(cls)

        if not description:
            raise ImproperlyConfigured("No description provided in Meta")

        if isinstance(permissions, str):
            permissions = (permissions,)

        if permissions and not isinstance(permissions, tuple):
            raise ImproperlyConfigured(
                "Permissions should be a tuple or a string in Meta"
            )

        _meta.permissions = permissions
        _meta.error_type_class = error_type_class
        _meta.error_type_field = error_type_field
        super().__init_subclass_with_meta__(
            description=description, _meta=_meta, **options
        )
        if error_type_class and error_type_field:
            cls._meta.fields.update(
                get_error_fields(error_type_class, error_type_field)
            )

    @classmethod
    def get_node_or_error(cls, info, node_id, field="id", only_type=None, qs=None):
        if not node_id:
            return None

        try:
            if only_type is not None:
                pk = from_global_id_strict_type(node_id, only_type, field=field)
            else:
                # FIXME: warn when supplied only_type is None?
                only_type, pk = graphene.Node.from_global_id(node_id)

            if isinstance(only_type, str):
                only_type = info.schema.get_type(only_type).graphene_type

            node = cls.get_node_by_pk(info, graphene_type=only_type, pk=pk, qs=qs)
        except (AssertionError, GraphQLError) as e:
            raise ValidationError(
                {field: ValidationError(str(e), code="graphql_error")}
            )
        else:
            if node is None:
                raise ValidationError(
                    {
                        field: ValidationError(
                            "Couldn't resolve to a node: %s" % node_id, code="not_found"
                        )
                    }
                )
        return node

    @classmethod
    def _update_mutation_arguments_and_fields(cls, arguments, fields):
        cls._meta.arguments.update(arguments)
        cls._meta.fields.update(fields)

    @classmethod
    def check_permissions(cls, context):
        """Determine whether user or service account has rights to perform this mutation.

        Default implementation assumes that account is allowed to perform any
        mutation. By overriding this method or defining required permissions
        in the meta-class, you can restrict access to it.

        The `context` parameter is the Context instance associated with the request.
        """
        if not cls._meta.permissions:
            return True
        if context.user.has_perms(cls._meta.permissions):
            return True
        service_account = getattr(context, "service_account", None)
        if service_account and service_account.has_perms(cls._meta.permissions):
            return True
        return False

    @classmethod
    def mutate(cls, root, info, **data):
        if not cls.check_permissions(info.context):
            raise PermissionDenied()

        try:
            response = cls.perform_mutation(root, info, **data)
            if response.errors is None:
                response.errors = []
            return response
        except ValidationError as e:
            return cls.handle_errors(e)

    @classmethod
    def perform_mutation(cls, root, info, **data):
        pass

    @classmethod
    def handle_errors(cls, error: ValidationError, **extra):
        errors = validation_error_to_error_type(error)
        return cls.handle_typed_errors(errors, **extra)

    @classmethod
    def handle_typed_errors(cls, errors: list, **extra):
        """Return class instance with errors."""
        if (
            cls._meta.error_type_class is not None
            and cls._meta.error_type_field is not None
        ):
            typed_errors = [
                cls._meta.error_type_class(field=e.field, message=e.message, code=code)
                for e, code, _params in errors
            ]
            extra.update({cls._meta.error_type_field: typed_errors})
        return cls(errors=[e[0] for e in errors], **extra)


class ModelMutation(BaseMutation):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        arguments=None,
        model=None,
        exclude=None,
        return_field_name=None,
        _meta=None,
        **options,
    ):
        if not model:
            raise ImproperlyConfigured("model is required for ModelMutation")
        if not _meta:
            _meta = ModelMutationOptions(cls)

        if exclude is None:
            exclude = []

        if not return_field_name:
            return_field_name = get_model_name(model)
        if arguments is None:
            arguments = {}
        fields = get_output_fields(model, return_field_name)

        _meta.model = model
        _meta.return_field_name = return_field_name
        _meta.exclude = exclude
        super().__init_subclass_with_meta__(_meta=_meta, **options)
        cls._update_mutation_arguments_and_fields(arguments=arguments, fields=fields)

    @classmethod
    def clean_input(cls, info, instance, data, input_cls=None):
        """Clean input data received from mutation arguments.

        Fields containing IDs or lists of IDs are automatically resolved into
        model instances. `instance` argument is the model instance the mutation
        is operating on (before setting the input data). `input` is raw input
        data the mutation receives.

        Override this method to provide custom transformations of incoming
        data.
        """

        def is_list_of_ids(field):
            return (
                isinstance(field.type, graphene.List)
                and field.type.of_type == graphene.ID
            )

        def is_id_field(field):
            return (
                field.type == graphene.ID
                or isinstance(field.type, graphene.NonNull)
                and field.type.of_type == graphene.ID
            )

        def is_upload_field(field):
            if hasattr(field.type, "of_type"):
                return field.type.of_type == Upload
            return field.type == Upload

        if not input_cls:
            input_cls = getattr(cls.Arguments, "input")
        cleaned_input = {}

        for field_name, field_item in input_cls._meta.fields.items():
            if field_name in data:
                value = data[field_name]
                # handle list of IDs field
                if value is not None and is_list_of_ids(field_item):
                    instances = (
                        cls.get_nodes_or_error(value, field_name) if value else []
                    )
                    cleaned_input[field_name] = instances

                # handle ID field
                elif value is not None and is_id_field(field_item):
                    instance = cls.get_node_or_error(info, value, field_name)
                    cleaned_input[field_name] = instance

                # handle uploaded files
                elif value is not None and is_upload_field(field_item):
                    value = info.context.FILES.get(value)
                    cleaned_input[field_name] = value

                # handle other fields
                else:
                    cleaned_input[field_name] = value
        return cleaned_input

    @classmethod
    def _save_m2m(cls, info, instance, cleaned_data):
        opts = instance._meta
        for f in chain(opts.many_to_many, opts.private_fields):
            if not hasattr(f, "save_form_data"):
                continue
            if f.name in cleaned_data and cleaned_data[f.name] is not None:
                f.save_form_data(instance, cleaned_data[f.name])

    @classmethod
    def success_response(cls, instance):
        """Return a success response."""
        return cls(**{cls._meta.return_field_name: instance, "errors": []})

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()

    @classmethod
    def get_instance(cls, info, **data):
        """Retrieve an instance from the supplied global id.

        The expected graphene type can be lazy (str).
        """
        object_id = data.get("id")
        if object_id:
            model_type = registry.get_type_for_model(cls._meta.model)
            instance = cls.get_node_or_error(info, object_id, only_type=model_type)
        else:
            instance = cls._meta.model()
        return instance

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        """Perform model mutation.

        Depending on the input data, `mutate` either creates a new instance or
        updates an existing one. If `id` argument is present, it is assumed
        that this is an "update" mutation. Otherwise, a new instance is
        created based on the model associated with this mutation.
        """
        instance = cls.get_instance(info, **data)
        data = data.get("input")
        cleaned_input = cls.clean_input(info, instance, data)
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(instance)
        cls.save(info, instance, cleaned_input)
        cls._save_m2m(info, instance, cleaned_input)
        return cls.success_response(instance)
