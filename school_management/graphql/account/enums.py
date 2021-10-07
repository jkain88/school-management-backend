import graphene


class Role(graphene.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    ADMIN = "admin"


class AddressType(graphene.Enum):
    PERMANENT = "permanent"
    CURRENT = "current"
