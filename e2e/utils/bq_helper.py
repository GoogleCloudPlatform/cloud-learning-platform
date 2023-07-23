"""_summary_
"""
import os
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"
BQ_TABLE_DICT = {
    "BQ_COLL_SECTION_TABLE": "section",
    "BQ_COLL_COHORT_TABLE": "cohort",
    "BQ_COLL_COURSETEMPLATE_TABLE": "courseTemplate",
    "BQ_ANALYTICS_VIEW":"gradeBookEnrichedView",
    "BQ_ENROLLMENT_RECORD" : "sectionEnrollmentRecord",
    "EXISTS_IN_CLASSROOM_NOT_IN_DB_VIEW":"roastersExitsInClassroomNotInDB",
    "EXISTS_IN_DB_NOT_IN_CLASSROOM_VIEW":"roastersExitsInDBNotInClassroom"
}
