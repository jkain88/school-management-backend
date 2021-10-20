import graphene
from graphql_jwt.decorators import login_required
import graphene_django_optimizer as gql_optimizer

from .mutations import (
    AddressCreate,
    AddressUpdate,
    AddressDelete,
    CreateToken,
    StudentCreate,
    StudentUpdate,
    StudentDelete,
)
from .types import Student
from .filters import StudentFilter, StudentFilterInput
from ..core.fields import FilterInputConnectionField
from ..core.types import FilterInputObjectType
from ...account import models


class AccountQueries(graphene.ObjectType):
    #me = graphene.Field(User, description="Return authenticated user instance")
    students = FilterInputConnectionField(
        Student,
        filter=StudentFilterInput(description="Filtering options for users."),
        description="List of users"
    )

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_students(self, info, **_kwargs):
        qs = models.Student.objects.all()
        qs = qs.order_by("id")

        return gql_optimizer.query(qs, info)


class AccountMutations(graphene.ObjectType):
    student_create = StudentCreate.Field()
    student_update = StudentUpdate.Field()
    student_delete = StudentDelete.Field()

    address_create = AddressCreate.Field()
    address_update = AddressUpdate.Field()
    address_delete = AddressDelete.Field()

    create_token = CreateToken.Field()
