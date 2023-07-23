"""Example Items for testing"""

TEST_LEARNING_CONTENT = {
    "title": "test course",
    "description": "test description",
    "document_type": "pdf"
}

TEST_COURSE = {
    "title": "test course",
    "label": "test label for course",
    "type": "test type",
    "is_valid": True
}

TEST_COMPETENCY = {
    "title": "test competency",
    "description": "test description for competency",
    "label": "test label",
    "type": "test type",
    "is_valid": True,
}

TEST_SUB_COMPETENCY = {
    "title": "test sub_competency",
    "description": "test description for sub_competency",
    "all_learning_resource": "the full content of the learning resource",
    "label": "test label",
    "total_lus": 1,
    "is_valid": True
}

TEST_LEARNING_OBJECTIVE = {
    "title": "test learning_objective",
    "description": "test description for learning_objective",
    "is_valid": True,
    "text": "sample_paragraph1<p>sample_paragraph2"
}

TEST_LEARNING_UNIT = {
    "title": "test learning_unit",
    "text": "test text for learning_unit",
    "pdf_title": "test pdf title",
    "topics": "test topics",
    "is_valid": True
}

TEST_TRIPLE = {
    "subject": "dummy subject",
    "predicate": "dummy predicate",
    "object": "dummy object",
    "confidence": 0.9,
    "sentence": "dummy sentence"
}
