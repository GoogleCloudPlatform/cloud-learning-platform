import os
from behave import fixture, use_fixture
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE_TEMPLATE
import logging
@fixture
def create_course_templates(context):
    """Fixture to create temprory data"""
    course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()
    context.course_template=course_template
    yield context.course_template

fixture_registry = {
    "fixture.create.course_tepmlate": create_course_templates,
}

def before_tag(context, tag):
    if tag.startswith("fixture."):
        try:
            fixture_data = fixture_registry.get(tag, None)
            if fixture_data is None:
                raise LookupError("Unknown fixture-tag: %s" % tag)
            return use_fixture(fixture_data, context)
        except Exception as e:
            print(e)
            logging.error(str(e))
