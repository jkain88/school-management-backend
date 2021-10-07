import binascii
from enum import Enum
from typing import Union

from django.core.exceptions import (
    ValidationError,
    NON_FIELD_ERRORS
)
import graphene
from graphene import List
from graphene import ObjectType
from graphene_django.forms.converter import convert_form_field

from .filters import (
    ListObjectTypeFilter,
    ObjectTypeFilter,
    EnumFilter
)
from .types import Error


DJANGO_VALIDATORS_ERROR_CODES = [
    "invalid",
    "invalid_extension",
    "limit_value",
    "max_decimal_places",
    "max_digits",
    "max_length",
    "max_value",
    "max_whole_digits",
    "min_length",
    "min_value",
    "null_characters_not_allowed",
]

DJANGO_FORM_FIELDS_ERROR_CODES = [
    "contradiction",
    "empty",
    "incomplete",
    "invalid_choice",
    "invalid_date",
    "invalid_image",
    "invalid_list",
    "invalid_time",
    "missing",
    "overflow",
]


def from_global_id_strict_type(
    global_id: str, only_type: Union[ObjectType, str], field: str = "id"
):
    """Resolve a node global id with a strict given type required."""
    try:
        _type, _id = graphene.Node.from_global_id(global_id)
    except (binascii.Error, UnicodeDecodeError) as exc:
        raise ValidationError(
            {
                field: ValidationError(
                    "Couldn't resolve to a node: %s" % global_id, code="not_found"
                )
            }
        ) from exc

    if str(_type) != str(only_type):
        raise ValidationError(
            {field: ValidationError(f"Must receive a {only_type} id", code="invalid")}
        )
    return _id


def get_error_fields(error_type_class, error_type_field):
    return {
        error_type_field: graphene.Field(
            graphene.List(
                graphene.NonNull(error_type_class),
                description="List of errors that occurred executing the mutation.",
            ),
            default_value=[],
        )
    }


def get_error_code_from_error(error) -> str:
    """Return valid error code from ValidationError.

    It unifies default Django error codes and checks
    if error code is valid.
    """
    code = error.code
    if code in ["required", "blank", "null"]:
        return "required"
    if code in ["unique", "unique_for_date"]:
        return "unique"
    if code in DJANGO_VALIDATORS_ERROR_CODES or code in DJANGO_FORM_FIELDS_ERROR_CODES:
        return "invalid"
    if isinstance(code, Enum):
        code = code.value

    # TODO: Create List Error codes
    if code not in []:
        return "invalid"
    return code


def snake_to_camel_case(name):
    """Convert snake_case variable name to camelCase."""
    if isinstance(name, str):
        split_name = name.split("_")
        return split_name[0] + "".join(map(str.capitalize, split_name[1:]))
    return name


def validation_error_to_error_type(validation_error: ValidationError) -> list:
    """Convert a ValidationError into a list of Error types."""
    err_list = []
    if hasattr(validation_error, "error_dict"):
        # convert field errors
        for field, field_errors in validation_error.error_dict.items():
            field = None if field == NON_FIELD_ERRORS else snake_to_camel_case(field)
            for err in field_errors:
                err_list.append(
                    (
                        Error(field=field, message=err.messages[0]),
                        get_error_code_from_error(err),
                        err.params,
                    )
                )
    else:
        # convert non-field errors
        for err in validation_error.error_list:
            err_list.append(
                (
                    Error(message=err.messages[0]),
                    get_error_code_from_error(err),
                    err.params,
                )
            )
    return err_list


@convert_form_field.register(ListObjectTypeFilter)
def convert_list_object_type(field):
    return List(field.input_class)


@convert_form_field.register(ObjectTypeFilter)
@convert_form_field.register(EnumFilter)
def convert_convert_enum(field):
    return field.input_class()
