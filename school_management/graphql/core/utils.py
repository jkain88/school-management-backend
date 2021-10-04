import binascii
from typing import Union

from django.core.exceptions import ValidationError
import graphene
from graphene import ObjectType


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
