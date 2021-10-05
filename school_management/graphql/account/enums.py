from enum import Enum


class Role(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    ADMIN = "admin"


class AddressType(Enum):
    PERMANENT = "permanent"
    CURRENT = "current"
