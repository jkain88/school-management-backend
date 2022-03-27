# TODO:CREATE GradeLevel Model
class GradeLevel:
    ELEMENTARY_GRADE_1 = "elementary_grade_1"
    ELEMENTARY_GRADE_2 = "elementary_grade_2"
    JUNIOR_HIGH_SCHOOL_GRADE_7 = "junior_high_school_grade_7"
    SENIOR_HIGH_SCHOOL_GRADE_11 = "senior_high_school_grade_11"

    CHOICES = [
        (ELEMENTARY_GRADE_1, "Elementary Grade 1"),
        (ELEMENTARY_GRADE_2, "Elementary Grade 2"),
        (JUNIOR_HIGH_SCHOOL_GRADE_7, "Junior High School Grade 7"),
        (SENIOR_HIGH_SCHOOL_GRADE_11, "Senior High School Grade 11"),
    ]
