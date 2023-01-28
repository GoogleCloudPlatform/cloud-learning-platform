""" Schema examples and test objects for unit test """
# pylint: disable=line-too-long
from config import ISSUER

BASIC_TOOL_EXAMPLE = {
    "name": "Test tool",
    "description": "Test tool integration",
    "tool_url": "https://example-tool.com",
    "tool_login_url": "https://example-tool.com/admin/api/ltilaunch/oidclogin",
    "public_key_type": "JWK URL",
    "tool_keyset_url": "https://example-tool.com/admin/ui/jwks",
    "content_selection_url": "https://example-tool.com/admin/ui/deep_link",
    "redirect_uris": [
        "https://example-tool.com/admin/api/ltilaunch/ltitoollaunch"
    ],
    "enable_grade_sync": False
}

FULL_TOOL_EXAMPLE = {
    "id": "asd98798as7dhjgkjsdfh",
    **BASIC_TOOL_EXAMPLE, "client_id": "174875a8-9c35-4963-89f7-cae31be3d78e",
    "deployment_id": "8434c79b-ba17-443d-a561-2e3ce7d7c804",
    "issuer": ISSUER,
    "platform_auth_url": f"{ISSUER}/lti/api/v1/authorize",
    "platform_token_url": f"{ISSUER}/lti/api/v1/token",
    "platform_keyset_url": f"{ISSUER}/lti/api/v1/jwks",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

BASIC_PLATFORM_EXAMPLE = {
    "name": "Test Platform",
    "description": "Test Platform Desc",
    "client_id": "client_id1",
    "issuer": "issuer1",
    "platform_keyset_url": "https://platformurl.com/jwks",
    "platform_auth_url": "https://platformurl.com/auth",
    "platform_token_url": "https://platformurl.com/token",
    "deployment_ids": ["deploy_id1"]
}

FULL_PLATFORM_EXAMPLE = {
    "id": "asd98798as7dhjgkjsdfh",
    **BASIC_PLATFORM_EXAMPLE, "tool_auth_url": f"{ISSUER}/lti/api/v1/authorize",
    "tool_token_url": f"{ISSUER}/lti/api/v1/token",
    "tool_keyset_url": f"{ISSUER}/lti/api/v1/jwks/SoD1uf9V1nc9"
}

BASIC_LINE_ITEM_EXAMPLE = {
    "scoreMaximum": 50,
    "label": "50",
    "tag": "50",
    "resourceId": "50",
    "resourceLinkId": "50",
    "startDateTime": "2022-02-05T22:23:11+0000",
    "endDateTime": "2022-02-07T22:23:11+0000"
}

UPDATE_LINE_ITEM_EXAMPLE = {
    "scoreMaximum": 50,
    "label": "50",
    "startDateTime": "2022-02-05T22:23:11+0000",
    "endDateTime": "2022-02-07T22:23:11+0000"
}

UPDATE_LINE_ITEM_USING_ID_EXAMPLE = {
    **UPDATE_LINE_ITEM_EXAMPLE, "id":
        "https://platformurl.com/context_id/line_items/bv9oyqvq9no"
}

FULL_LINE_ITEM_EXAMPLE = {
    "uuid": "bv9oyqvq9no",
    "id": "https://platformurl.com/context_id/line_items/bv9oyqvq9no",
    **BASIC_LINE_ITEM_EXAMPLE
}

BASIC_SCORE_EXAMPLE = {
    "userId": "ATc1ob81ca1vb98",
    "scoreGiven": 50,
    "scoreMaximum": 50,
    "comment": "",
    "timestamp": "2017-04-16T18:54:36.736+00:00",
    "activityProgress": "Completed",
    "gradingProgress": "FullyGraded"
}

FULL_SCORE_EXAMPLE = {"uuid": "Ar1F79GnqG8enw", **BASIC_SCORE_EXAMPLE}

BASIC_RESULT_EXAMPLE = {
    "userId": "ATc1ob81ca1vb98",
    "resultScore": 50,
    "resultMaximum": 50,
    "comment": "Test comment",
    "scoreOf": "https://platformurl.com/x1b62/line_items/1c82be"
}

FULL_RESULT_EXAMPLE = {
    "uuid":
        "DVad8vs5boSN",
    "id":
        "https://platformurl.com/x1b62/line_items/1c82be/results/DVad8vs5boSN",
    **BASIC_RESULT_EXAMPLE
}

BASIC_CONTENT_ITEM_EXAMPLE = {
    "tool_id": "A6cS8vaCsOavO",
    "content_item_type": "ltiResourceLink",
    "content_item_info": {
        "custom": {
            "resourceid": "d83dd1d0-a937-3341-8e9a-eb3cf1146bff"
        },
        "text": "test-image.jpg",
        "title": "test-image.jpg",
        "type": "ltiResourceLink",
        "url": "https://testtool.com/api/ltilaunch/ltitoollaunch"
    }
}

FULL_CONTENT_ITEM_EXAMPLE = {
    "uuid": "aC72Vos31iFQt09c",
    **BASIC_CONTENT_ITEM_EXAMPLE, "is_archived": False,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}
