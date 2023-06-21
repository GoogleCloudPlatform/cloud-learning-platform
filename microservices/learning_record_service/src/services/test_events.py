"""Test LRS Events"""
events = [{
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "e8oKpDUSBSmGb8eqeBIG",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:gautam.patidar@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "Cw574DIr4Lh1Sb0EAMJt",
        "name": "started",
        "url": "http://example.com/xapi/verbs#started",
        "canonical_data": {}
    },
    "object": {
        "uuid": "JlMKQIpF8UACsbXlPykM",
        "name": "Sequencing 1",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Sequencing 1",
            "type": "learning_resources",
            "uuid": "0idJJWYLtKrDVYjHnkBI"
        }
    }
},
{
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "e8oKpDUSBSmGb8eqeBIG",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:gautam.patidar@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "0y3v7l18KrjWclpUoZcT",
        "name": "completed",
        "url": "http://example.com/xapi/verbs#completed",
        "canonical_data": {}
    },
    "object": {
        "uuid": "JlMKQIpF8UACsbXlPykM",
        "name": "Sequencing 1",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Sequencing 1",
            "type": "learning_resources",
            "uuid": "0idJJWYLtKrDVYjHnkBI"
        }
    }
},

    {
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "e8oKpDUSBSmGb8eqeBIG",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:gautam.patidar@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "stJJVsAaOB7nGCjtCoxf",
        "name": "submitted",
        "url": "http://activitystrea.ms/schema/1.0/submit",
        "canonical_data": {}
    },
    "object": {
        "uuid": "VZCfMASrlZbu2qzXZShB",
        "name": "Summative Assessment",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Summative Assessment",
            "type": "assessment_items",
            "uuid": "VZCfMASrlZbu2qzXZShB"
        }
    },
    "result_score_min": 0,
    "result_score_max": 100,
    "result_score_raw" : 60
},
{
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "e8oKpDUSBSmGb8eqeBIG",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:gautam.patidar@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "stJJVsAaOB7nGCjtCoxf",
        "name": "submitted",
        "url": "http://activitystrea.ms/schema/1.0/submit",
        "canonical_data": {}
    },
    "object": {
        "uuid": "5nDAn6eVGai9UYQYNjGL",
        "name": "Summative Assessment",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Summative Assessment",
            "type": "summative_assessment",
            "achievements": ["qu3b0wz5uiFU7tkvLarR", "51FgPMHdRTmh0lpwlta7"],
            "prerequisites": []
        }
    },
    "result_score_min": 0,
    "result_score_max": 100,
    "result_score_raw" : 60
}
]
