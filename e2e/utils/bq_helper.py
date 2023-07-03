"""_summary_
"""
import os
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"
BQ_TABLE_DICT = {
    "BQ_COLL_SECTION_TABLE": "section",
    "BQ_COLL_COHORT_TABLE": "cohort",
    "BQ_COLL_COURSETEMPLATE_TABLE": "courseTemplate",
    "BQ_ANALYTICS_VIEW":"gradeBookEnrichedView"
}
