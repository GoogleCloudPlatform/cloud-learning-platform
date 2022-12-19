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
    ]
}

FULL_TOOL_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_TOOL_EXAMPLE, "client_id": "174875a8-9c35-4963-89f7-cae31be3d78e",
    "deployment_id": "8434c79b-ba17-443d-a561-2e3ce7d7c804",
    "issuer": ISSUER,
    "platform_auth_url": f"{ISSUER}/lti-service/api/v1/authorize",
    "platform_token_url": f"{ISSUER}/lti-service/api/v1/token",
    "platform_keyset_url": f"{ISSUER}/lti-service/api/v1/jwks",
    "is_archived": False,
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
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_PLATFORM_EXAMPLE,
    "tool_auth_url": f"{ISSUER}/lti-service/api/v1/authorize",
    "tool_token_url": f"{ISSUER}/lti-service/api/v1/token",
    "tool_keyset_url": f"{ISSUER}/lti-service/api/v1/jwks/SoD1uf9V1nc9",
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
