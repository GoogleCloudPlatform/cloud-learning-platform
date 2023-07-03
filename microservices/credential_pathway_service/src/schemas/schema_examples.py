"""
  Schema Examples
"""

BASIC_BADGE_EXAMPLE = {
    "entity_type": "badge",
    "entity_id": "12345",
    "open_badge_id": "12",
    "created_by": "badge",
    "issuer": "university",
    "issuer_open_badge_id": "string",
    "name": "Jon",
    "image": "string",
    "description": "best start",
    "achievement_type": "Achievement",
    "criteria_url": "string",
    "criteria_narrative": "string",
    "alignments": {},
    "tags": [],
    "expires": {},
    "extensions": "string"
}

BASIC_ISSUER_EXAMPLE = {
    "entity_type": "issuer",
    "entity_id": "987",
    "open_badge_id": "13",
    "name": "Jon",
    "image": "string",
    "email": "jon@example.com",
    "description": "issue",
    "url": "https://www.example.com",
    "staff": [{}],
    "extensions": "string",
    "badgr_domain": "string"
}

BASIC_ASSERTION_EXAMPLE = {
    "entity_type": "assertion",
    "entity_id": "986",
    "open_badge_id": "31",
    "created_by": "user",
    "badgeclass": "badger",
    "badgeclass_open_badge_id": "string",
    "issuer": "uni",
    "issuer_open_badge_id": "string",
    "image": "string",
    "recipient": {},
    "issued_on": "string",
    "narrative": "string",
    "evidence": [{}],
    "revocation_reason": "string",
    "acceptance": "string",
    "extensions": "string",
    "expires": "2022-07-21 15:01:27",
    "badgeclass_name": "string"
}
