"""
    User should be able to upload valid madcap SRL zip against any Learning experience
"""
import behave
import sys

sys.path.append("../")
from common.utils.collection_references import collection_references
from common.models import LearningExperience, LearningObject, LearningResource
from setup import post_method, get_method
from environment import (TEST_LEARNING_HIERARCHY_FOR_SRL, 
                            TEST_CONTENT_SERVING_SRL_V1_PATH,
                            TEST_CONTENT_SERVING_SRL_V2_PATH,
                            TEST_CONTENT_SERVING_SRL_V3_PATH,
                            TEST_CONTENT_SERVING_MADCAP_V1_PATH)
from test_config import API_URL_LEARNING_OBJECT_SERVICE
API_URL = API_URL_LEARNING_OBJECT_SERVICE
LEARNING_RESOURCE_UUID=""

def get_all_nodes_for_alias(uuid: str,
                                level: str,
                                final_alias: str,
                                nodes: list):
    """
    This method traverses the learning hierarchy from given level uuid till the
    final_alias and retrieves all the node where alias=final_alias.
    Args:
        uuid (str): uuid of the node from where to traverse.
        level (str): current level/type of the Node for given uuid.
        final_alias (str): alias till which the traverse should be done.
        nodes (list): list to be used to return list of nodes
    Returns:
        nodes (list): List of nodes of alias=final_alias
    """
    node = collection_references[level].find_by_uuid(uuid)
    node = node.get_fields(reformat_datetime=True)
    if node.get("alias", "") == final_alias:
        nodes.append(node)
        return
    child_nodes = node.get("child_nodes", [])
    if child_nodes:
        for child_level in child_nodes:
            for child_uuid in child_nodes[child_level]:
                get_all_nodes_for_alias(child_uuid, child_level, final_alias, nodes)
    return nodes

# -----------------------------------------------------
# Scenario 1: User wants to be able to upload a valid madcap SRL zip against any Learning experience and it will be made available for all sibling LEs
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a valid madcap SRL zip against any Learning experience")
def step_impl_1(context):
    context.program_uuid = ""

    url = f"{API_URL}/curriculum-pathway/bulk-import/json"
    with open(TEST_LEARNING_HIERARCHY_FOR_SRL, encoding="UTF-8") as pathways_json_file:
        resp = post_method(
            url, files={"json_file": pathways_json_file})

        assert resp.status_code == 200
        resp_json = resp.json()
        context.program_uuid = resp_json["data"][0]

    sibling_le_list = []
    le_list = get_all_nodes_for_alias(
        uuid=context.program_uuid,
        level="curriculum_pathways",
        final_alias="learning_experience",
        nodes=sibling_le_list
    )

    context.le_1_uuid = le_list[0]["uuid"]
    context.le_2_uuid = le_list[1]["uuid"]

@behave.when("API request is sent to upload a valid madcap SRL zip against any Learning experience")
def step_impl_2(context):
    file_path = f"{TEST_CONTENT_SERVING_SRL_V1_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("SRL_content_serving_valid.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

@behave.then("LOS will return a success response for the upload and all sibling LEs get access to it")
def step_impl_3(context):

    print(context.res.status_code)
    print(context.res_json)

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {context.le_1_uuid}"
    assert context.res_json["data"].get("prefix") == "learning-resources/SRL_content_serving_valid/"

    res = get_method(url=f"{API_URL}/learning-experience/{context.le_1_uuid}")
    res_json = res.json()
    assert res_json["data"]["srl_resource_path"] == "learning-resources/SRL_content_serving_valid/"

    res = get_method(url=f"{API_URL}/learning-experience/{context.le_2_uuid}")
    res_json = res.json()
    assert res_json["data"]["srl_resource_path"] == "learning-resources/SRL_content_serving_valid/"

# -----------------------------------------------------
# Scenario 2: User wants to upload a madcap zip with invalid SRL name against any Learning experience
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to upload a madcap SRL zip with invalid SRL name against any Learning experience")
def step_impl_1(context):
    context.program_uuid = ""

    url = f"{API_URL}/curriculum-pathway/bulk-import/json"
    with open(TEST_LEARNING_HIERARCHY_FOR_SRL, encoding="UTF-8") as pathways_json_file:
        resp = post_method(
            url, files={"json_file": pathways_json_file})

        assert resp.status_code == 200
        resp_json = resp.json()
        context.program_uuid = resp_json["data"][0]

    sibling_le_list = []
    le_list = get_all_nodes_for_alias(
        uuid=context.program_uuid,
        level="curriculum_pathways",
        final_alias="learning_experience",
        nodes=sibling_le_list
    )

    context.le_1_uuid = le_list[0]["uuid"]
    context.le_2_uuid = le_list[1]["uuid"]

@behave.when("API request is sent to upload a madcap SRL zip with invalid SRL name against any Learning experience")
def step_impl_2(context):
    file_path = f"{TEST_CONTENT_SERVING_MADCAP_V1_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("content_serving_sample_upload_madcap_v1.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

@behave.then("LOS will return a failure response for the upload because the file name does not follow the SRL naming convention")
def step_impl_3(context):

    print(context.res.status_code)
    print(context.res_json)

    assert context.res.status_code == 422
    assert context.res_json["success"] is False
    assert context.res_json["message"] == f"""File name should start with the prefix "SRL". eg: "SRL_file_1.zip" """

# -----------------------------------------------------
# Scenario 3: User wants to be able to reupload a valid madcap SRL zip against any Learning experience and it will be made available for all sibling LEs and underlying LRs resource_paths will be updated
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to reupload a valid madcap SRL zip against any Learning experience")
def step_impl_1(context):
    context.program_uuid = ""

    url = f"{API_URL}/curriculum-pathway/bulk-import/json"
    with open(TEST_LEARNING_HIERARCHY_FOR_SRL, encoding="UTF-8") as pathways_json_file:
        resp = post_method(
            url, files={"json_file": pathways_json_file})

        assert resp.status_code == 200
        resp_json = resp.json()
        context.program_uuid = resp_json["data"][0]

    sibling_le_list = []
    le_list = get_all_nodes_for_alias(
        uuid=context.program_uuid,
        level="curriculum_pathways",
        final_alias="learning_experience",
        nodes=sibling_le_list
    )

    context.le_1_uuid = le_list[0]["uuid"]
    context.le_2_uuid = le_list[1]["uuid"]

    file_path = f"{TEST_CONTENT_SERVING_SRL_V1_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("SRL_content_serving_valid.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {context.le_1_uuid}"
    assert context.res_json["data"].get("prefix") == "learning-resources/SRL_content_serving_valid/"

    res = get_method(url=f"{API_URL}/learning-experience/{context.le_1_uuid}")
    res_json = res.json()
    assert res_json["data"]["srl_resource_path"] == "learning-resources/SRL_content_serving_valid/"

    res = get_method(url=f"{API_URL}/learning-experience/{context.le_2_uuid}")
    res_json = res.json()
    assert res_json["data"]["srl_resource_path"] == "learning-resources/SRL_content_serving_valid/"

    lo_1 = LearningObject.find_by_uuid(le_list[0]["child_nodes"]["learning_objects"][0])
    lo_2 = LearningObject.find_by_uuid(le_list[1]["child_nodes"]["learning_objects"][0])

    context.lr_1 = LearningResource.find_by_uuid(lo_1.child_nodes["learning_resources"][0])
    context.lr_2 = LearningResource.find_by_uuid(lo_2.child_nodes["learning_resources"][0])

    # Link content to lr_1
    res = post_method(
        url=f"{API_URL}/content-serving/link/madcap/{context.le_1_uuid}/{context.lr_1.uuid}",
        request_body={
            "resource_path":"learning-resources/SRL_content_serving_valid/SRL_Dummy/Content/SRL_html_1.htm",
            "type":"html"
        },
        query_params={
            "is_srl": True
        }
    )
    res_json = res.json()

    print(res_json)

    assert res.status_code == 200
    assert res_json["success"] is True
    assert res_json["message"] == f"Successfully linked content to Learning Resource with uuid {context.lr_1.uuid}"

@behave.when("API request is sent to reupload a valid madcap SRL zip against any Learning experience")
def step_impl_2(context):
    file_path = f"{TEST_CONTENT_SERVING_SRL_V2_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("SRL_content_serving_v2_valid.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

@behave.then("LOS will return a success response for the upload and all LE siblings srl_resource_path is updated")
def step_impl_3(context):
    print(context.res.status_code)
    print(context.res_json)

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {context.le_1_uuid}"
    assert context.res_json["data"].get("prefix") == "learning-resources/SRL_content_serving_v2_valid/"

@behave.then("underlying LRs resource_path will be updated")
def step_impl_4(context):
    lr_1 = LearningResource.find_by_uuid(context.lr_1.uuid)
    lr_2 = LearningResource.find_by_uuid(context.lr_2.uuid)

    assert lr_1.resource_path == f"learning-resources/SRL_content_serving_v2_valid/SRL_Dummy/Content/SRL_html_1.htm"
    assert lr_2.resource_path == ""

# -----------------------------------------------------
# Scenario 4: User wants to reupload a madcap SRL zip against any Learning experience with missing files
# -----------------------------------------------------
@behave.given("that an LXE or CD has access to the content authoring tool and wants to reupload a madcap SRL zip with missing files against any Learning experience")
def step_impl_1(context):
    context.program_uuid = ""

    url = f"{API_URL}/curriculum-pathway/bulk-import/json"
    with open(TEST_LEARNING_HIERARCHY_FOR_SRL, encoding="UTF-8") as pathways_json_file:
        resp = post_method(
            url, files={"json_file": pathways_json_file})

        assert resp.status_code == 200
        resp_json = resp.json()
        context.program_uuid = resp_json["data"][0]

    sibling_le_list = []
    le_list = get_all_nodes_for_alias(
        uuid=context.program_uuid,
        level="curriculum_pathways",
        final_alias="learning_experience",
        nodes=sibling_le_list
    )

    context.le_1_uuid = le_list[0]["uuid"]
    context.le_2_uuid = le_list[1]["uuid"]

    file_path = f"{TEST_CONTENT_SERVING_SRL_V1_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("SRL_content_serving_valid.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

    assert context.res.status_code == 200
    assert context.res_json["success"] is True
    assert context.res_json[
        "message"] == f"Successfully uploaded the SRL content for learning experience with uuid {context.le_1_uuid}"
    assert context.res_json["data"].get("prefix") == "learning-resources/SRL_content_serving_valid/"

    res = get_method(url=f"{API_URL}/learning-experience/{context.le_1_uuid}")
    res_json = res.json()
    assert res_json["data"]["srl_resource_path"] == "learning-resources/SRL_content_serving_valid/"

@behave.when("API request is sent to reupload a madcap SRL zip with missing files against any Learning experience")
def step_impl_2(context):
    file_path = f"{TEST_CONTENT_SERVING_SRL_V3_PATH}"

    context.res = post_method(
        url=f"{API_URL}/content-serving/upload/madcap/{context.le_1_uuid}",
        query_params={
            "is_srl": True
        },
        files={
            "content_file": ("SRL_content_serving_v3_invalid.zip", 
                                open(file_path,"rb"), 
                                "application/zip")
        })
    context.res_json = context.res.json()

@behave.then("LOS will return a validation error with list of missing files in new SRL zip")
def step_impl_3(context):
    print(context.res.status_code)
    print(context.res_json)

    assert context.res.status_code == 422
    assert context.res_json["success"] is False
    assert f"Content override is forbidden because of missing files." in context.res_json["message"]
