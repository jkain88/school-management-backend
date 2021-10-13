class Role:
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    ADMIN = "admin"

    CHOICES = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (STAFF, "Staff"),
        (ADMIN, "Admin")
    ]


class AddressType:
    PERMANENT = "permanent"
    CURRENT = "current"

    CHOICES = [
        (PERMANENT, "Permanent"),
        (CURRENT, "Current")
    ]


class Sex:
    MALE = "male"
    FEMALE = "female"

    CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female")
    ]
