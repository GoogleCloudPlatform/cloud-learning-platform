""" Config used for testing in unit tests """

import os

API_URL = "http://localhost/learning-object-service/api/v1"

TESTING_FOLDER_PATH = os.path.join(os.getcwd(), "testing")
DEL_KEYS = [
    "version", "is_archived", "root_version_uuid", "uuid",
    "parent_version_uuid", "created_time", "last_modified_time", "status",
    "progress", "created_by", "last_modified_by", "id", "is_deleted", "key",
    "earned_achievements", "child_nodes_count", "completed_child_nodes_count",
    "archived_at_timestamp", "archived_by", "deleted_by", "deleted_at_timestamp"
]
