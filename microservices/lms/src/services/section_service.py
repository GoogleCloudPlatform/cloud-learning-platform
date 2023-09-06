"""Section API services"""
import traceback
import datetime
import time
import requests
from common.utils import classroom_crud
from common.utils.bq_helper import insert_rows_to_bq
from common.utils.logging_handler import Logger
from common.models import (Section, CourseEnrollmentMapping,
                           CourseTemplateEnrollmentMapping, User, LmsJob)
from common.utils.http_exceptions import (InternalServerError,
                                          ResourceNotFound)
from common.utils.errors import ValidationError
from services import common_service
from config import BQ_TABLE_DICT, BQ_DATASET, auth_client
from googleapiclient.errors import HttpError




# disabling for linting to pass
# pylint: disable = broad-except, line-too-long
def copy_course_background_task(course_template_details,
                                sections_details,
                                cohort_details,
                                lms_job_id,
                                message=""):
  """Create section  Background Task to copy course and updated database
  for newly created section
  Args:
    course_template_details (template object): course template object which
    will referenced in section
    sections_details (str):Input section details provided by user in API
    cohort_details(str):course template object which will
    referenced in section
    headers(str):Authentications headers
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    True : (bool) on success
  """
  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs
  try:
    # Create a new course
    info_msg = f"Background Task started for the cohort id {cohort_details.id}\
                course template {course_template_details.id} \
                with section name{sections_details.name}"

    logs["info"].append(info_msg)
    Logger.info(info_msg)

    new_course = classroom_crud.create_course(course_template_details.name,
                                              sections_details.description,
                                              sections_details.name, "me")

    lms_job.classroom_id = new_course["id"]
    lms_job.start_time = datetime.datetime.utcnow()
    lms_job.status = "running"
    lms_job.update()

    # Create section with the required fields
    section = Section()
    section.name = course_template_details.name
    section.section = sections_details.name
    section.description = sections_details.description
    section.max_students = sections_details.max_students
    # Reference document can be get using get() method
    section.course_template = course_template_details
    section.cohort = cohort_details
    section.classroom_id = new_course["id"]
    section.classroom_code = new_course["enrollmentCode"]
    section.classroom_url = new_course["alternateLink"]
    section.enrolled_students_count = 0
    section.status = "PROVISIONING"
    section_id = section.save().id
    classroom_id = new_course["id"]

    lms_job.section_id = section_id
    lms_job.update()

    error_flag = False
    target_folder_id = new_course["teacherFolder"]["id"]
    logs["info"].append(
        f"ID of target drive folder for section {target_folder_id}")
    Logger.info(f"ID of target drive folder for section {target_folder_id}")

    # Get topics of current course
    topics = classroom_crud.get_topics(course_template_details.classroom_id)
    # add new_course to pubsub topic for both course work and roaster changes
    classroom_crud.enable_notifications(new_course["id"], "COURSE_WORK_CHANGES")
    classroom_crud.enable_notifications(new_course["id"],
                                        "COURSE_ROSTER_CHANGES")
    # add instructional designer
    list_course_template_enrollment_mapping = CourseTemplateEnrollmentMapping\
      .fetch_all_by_course_template(course_template_details.key)
    if list_course_template_enrollment_mapping:
      for course_template_mapping in list_course_template_enrollment_mapping:
        try:
          add_instructional_designer_into_section(section,
                                                  course_template_mapping)
        except Exception as error:
          error = traceback.format_exc().replace("\n", " ")
          Logger.error(f"Create teacher failed for \
              for {course_template_details.instructional_designer}")
          Logger.error(error)

    #If topics are present in course create topics returns a dict
    # with keys a current topicID and new topic id as values
    if topics is not None:
      topic_id_map = classroom_crud.create_topics(new_course["id"], topics)
    # Calling function to get edit_url and view url of
    # google form which returns
    # a dictionary of view_links as keys and edit
    #  links/  and file_id as values for all drive files
    url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()

    # Get coursework of current course and create a new course
    coursework_list = classroom_crud.get_coursework_list(
        course_template_details.classroom_id)

    # final_coursewok=[]
    for coursework in coursework_list:
      coursework_lti_assignment_ids = []
      try:
        #Check if a coursework is linked to a topic if yes then
        # replace the old topic id to new topic id using topic_id_map

        lti_assignment_details = {
            "section_id": section_id,
            "source_context_id": course_template_details.id,
            "coursework_title": coursework["title"],
            "start_date": None,
            "end_date": None,
            "due_date": None
        }

        # Update the due date of the course work if exists
        if coursework.get("dueDate"):
          coursework_due_date = coursework.get("dueDate")

          if coursework.get("dueTime"):
            coursework_due_time = coursework.get("dueTime")
            coursework_due_datetime = datetime.datetime(
                coursework_due_date.get("year"),
                coursework_due_date.get("month"),
                coursework_due_date.get("day"),
                coursework_due_time.get("hours", 0),
                coursework_due_time.get("minutes", 0))
          else:
            coursework_due_datetime = datetime.datetime(
                coursework_due_date.get("year"),
                coursework_due_date.get("month"),
                coursework_due_date.get("day"))

          curr_utc_timestamp = datetime.datetime.utcnow()
          lti_assignment_details["start_date"] = (
              cohort_details.start_date).strftime("%Y-%m-%dT%H:%M:%S%z")

          if coursework_due_datetime < curr_utc_timestamp:
            # Commented for now as the due dates are supposed to be updated by the user before
            # starting the copy course process

            # coursework["dueDate"] = {
            #   "year": cohort_details.end_date.year,
            #   "month": cohort_details.end_date.month,
            #   "day": cohort_details.end_date.day
            # }
            # coursework["dueTime"] = {
            #   "hours": cohort_details.end_date.hour,
            #   "minutes": cohort_details.end_date.minute
            # }

            lti_assignment_details["end_date"] = lti_assignment_details[
                "due_date"] = (
                    cohort_details.end_date).strftime("%Y-%m-%dT%H:%M:%S%z")

          else:
            lti_assignment_details["end_date"] = lti_assignment_details[
                "due_date"] = coursework_due_datetime.strftime(
                    "%Y-%m-%dT%H:%M:%S%z")

        if "topicId" in coursework.keys():
          coursework["topicId"] = topic_id_map[coursework["topicId"]]
        #Check if a material is present in coursework
        if "materials" in coursework.keys():
          coursework_update_output = update_coursework_material(
              materials=coursework["materials"],
              url_mapping=url_mapping,
              target_folder_id=target_folder_id,
              error_flag=error_flag,
              lti_assignment_details=lti_assignment_details,
              logs=logs)
          coursework["materials"] = coursework_update_output["material"]
          error_flag = coursework_update_output["error_flag"]
          coursework_lti_assignment_ids.extend(
              coursework_update_output["lti_assignment_ids"])
        # final_coursewok.append(coursework)

        coursework_data = classroom_crud.create_coursework(
            new_course["id"], coursework)

        for assignment_id in coursework_lti_assignment_ids:
          coursework_id = coursework_data.get("id")
          input_json = {"course_work_id": coursework_id}
          # update assignment with new coursework id
          lti_assignment_req = requests.patch(
              f"http://classroom-shim/classroom-shim/api/v1/lti-assignment/{assignment_id}",
              headers={
                  "Authorization": f"Bearer {auth_client.get_id_token()}"
              },
              json=input_json,
              timeout=60)

          if lti_assignment_req.status_code != 200:
            error_flag = True
            error_msg = f"Failed to update assignment {assignment_id} with course work id \
                          {coursework_id} due to error - {lti_assignment_req.text} with \
                            status code - {lti_assignment_req.status_code} for course work"

            logs["errors"].append(error_msg)
            Logger.error(error_msg)

          logs["info"].append(
              f"Updated the course work id for new LTI assignment - {assignment_id}"
          )
          Logger.info(
              f"Updated the course work id for new LTI assignment - {assignment_id}"
          )

      except Exception as error:
        title = coursework["title"]
        error_flag = True
        logs["errors"].append(f"Error - {error} for '{title}'")
        logs["errors"].append(f"Copy coursework failed for \
              course_id {course_template_details.classroom_id} for '{title}'")
        Logger.error(f"Copy coursework failed for \
              course_id {course_template_details.classroom_id} for '{title}'")
        error = traceback.format_exc().replace("\n", " ")
        Logger.error(error)
        continue

    # # Create coursework in new course
    # # return final_coursewok
    # if final_coursewok is not None:
    #   classroom_crud.create_coursework(new_course["id"],final_coursewok)
    # Get the list of courseworkMaterial
    # final_coursewok_material = []
    coursework_material_list = classroom_crud.get_coursework_material_list(
        course_template_details.classroom_id)
    for coursework_material in coursework_material_list:
      coursework_material_lti_assignment_ids = []
      try:
        #Check if a coursework material is linked to a topic if yes then
        # replace the old topic id to new topic id using topic_id_map

        lti_assignment_details = {
            "section_id": section_id,
            "source_context_id": course_template_details.id,
            "coursework_title": coursework_material["title"],
            "start_date": None,
            "end_date": None,
            "due_date": None
        }

        if "topicId" in coursework_material.keys():
          coursework_material["topicId"] = topic_id_map[
              coursework_material["topicId"]]
        #Check if a material is present in coursework
        if "materials" in coursework_material.keys():

          coursework_material_update_output = update_coursework_material(
              materials=coursework_material["materials"],
              url_mapping=url_mapping,
              target_folder_id=target_folder_id,
              error_flag=error_flag,
              lti_assignment_details=lti_assignment_details,
              logs=logs)

          coursework_material["materials"] = coursework_material_update_output[
              "material"]
          error_flag = coursework_update_output["error_flag"]
          coursework_material_lti_assignment_ids.extend(
              coursework_update_output["lti_assignment_ids"])
          print("Updated coursework material attached")

        coursework_material_data = classroom_crud.create_coursework_material(new_course["id"],
                                                coursework_material)

        for assignment_id in coursework_material_lti_assignment_ids:
          coursework_id = coursework_material_data.get("id")
          input_json = {"course_work_id": coursework_id}
          # update assignment with new coursework id
          lti_assignment_req = requests.patch(
              f"http://classroom-shim/classroom-shim/api/v1/lti-assignment/{assignment_id}",
              headers={
                  "Authorization": f"Bearer {auth_client.get_id_token()}"
              },
              json=input_json,
              timeout=60)

          if lti_assignment_req.status_code != 200:
            error_flag = True
            error_msg = f"Failed to update assignment {assignment_id} with course work id \
                          {coursework_id} due to error - {lti_assignment_req.text} with \
                            status code - {lti_assignment_req.status_code} for course work material"

            logs["errors"].append(error_msg)
            Logger.error(error_msg)

          logs["info"].append(
              f"Updated the id for course work material for new LTI assignment - {assignment_id}"
          )
          Logger.info(
              f"Updated the id course work material for new LTI assignment - {assignment_id}"
          )

        # final_coursewok_material.append(coursework_material)
      except Exception as error:
        title = coursework_material["title"]
        error_flag = True
        Logger.error(f"Get coursework material failed for\
        course_id {course_template_details.classroom_id} for {title}")

        logs["errors"].append(f"Error - {error}")
        logs["errors"].append(f"Get coursework material failed for\
        course_id {course_template_details.classroom_id} for {title}")
        error = traceback.format_exc().replace("\n", " ")
        Logger.error(error)
        continue

    # # Create coursework in new course
    # if final_coursewok_material is not None:
    #   classroom_crud.create_coursework_material(new_course["id"],
    #                                             final_coursewok_material)

    # Classroom copy is successful then the section status is changed to active
    if error_flag:
      section.status = "FAILED_TO_PROVISION"
    else:
      section.status = "ACTIVE"
    section.update()

    rows=[{
      "sectionId":section_id,\
      "courseId":new_course["id"],\
      "classroomUrl":new_course["alternateLink"],\
        "name":new_course["section"],\
        "description":new_course["description"],\
          "cohortId":cohort_details.id,\
        "courseTemplateId":course_template_details.id,\
          "status":section.status,\
        "enrollmentStatus": section.enrollment_status,
        "maxStudents": section.max_students,
          "timestamp":datetime.datetime.utcnow()
    }]
    insert_rows_to_bq(
        rows=rows,
        dataset=BQ_DATASET,
        table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"])
    Logger.info(message)
    Logger.info(f"Background Task Completed for section Creation for cohort\
                {cohort_details.id}")
    Logger.info(f"Section Details are section id {section_id},\
                classroom id {classroom_id}")

    logs["info"].append(
        f"Background Task Completed for section Creation for cohort\
                {cohort_details.id}")
    logs["info"].append(f"Section Details are section id {section_id},\
                classroom id {classroom_id}")

    lms_job.logs = logs
    if error_flag:
      lms_job.status = "failed"
    else:
      lms_job.status = "success"
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.update()

    return True
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    Logger.error(e)

    logs["errors"].append(str(e))
    lms_job.logs = logs
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.status = "failed"
    lms_job.update()

    raise InternalServerError(str(e)) from e


def copy_course_background_task_alpha(
                        course_template_details,
                                sections_details,
                                cohort_details,
                                lms_job_id,
                                message=""):
  """
    This function is background function for alpha copy course

  """
  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs
  try:
    # Create a new course
    original_courseworks = classroom_crud.get_coursework_list(
      course_template_details.classroom_id)
    original_coursework_materials =  classroom_crud.get_coursework_material_list(
      course_template_details.classroom_id)
    Logger.info(message)
    Logger.info(f"Origial coursework list \
                {len(original_courseworks)}")
    Logger.info(f"Original coursework Material list\
                {len(original_coursework_materials)}")
    logs["info"].append(f"Original Courseworks {len(original_courseworks)}")
    logs["info"].append(f"Original Coursework Materials \
                        {len(original_coursework_materials)}")
    # Call classroom copy course API in Alpha version
    copied_course = classroom_crud.copy_classroom_course(course_template_details.classroom_id,
                                          course_template_details.name)
    classroom_id = copied_course["id"]
    logs["info"].append(f"Classroom copy course API competed {classroom_id}")
    lms_job.classroom_id = copied_course["id"]
    lms_job.start_time = datetime.datetime.utcnow()
    lms_job.status = "running"
    lms_job.update()
    # Create section with the required fields
    section = Section()
    section.name = course_template_details.name
    section.section = sections_details.name
    section.description = sections_details.description
    section.max_students = sections_details.max_students
    # Reference document can be get using get() method
    section.course_template = course_template_details
    section.cohort = cohort_details
    section.classroom_id = copied_course["id"]
    section.classroom_code = copied_course["enrollmentCode"]
    section.classroom_url = copied_course["alternateLink"]
    section.enrolled_students_count = 0
    section.status = "PROVISIONING"
    section_id = section.save().id
    lms_job.section_id = section_id
    lms_job.update()
    lms_job.logs = logs
    lms_job.update()
    course_template_id = course_template_details.id
    # Call check_copy_course function to verify all courseworks and coursework\
    #  material is copied
    error_flag = check_copy_course_alpha(original_courseworks,
                                    original_coursework_materials,
                                    copied_course,lms_job_id, section_id,
                                    course_template_id)
    # Calling classroom Update course API to update section name and
    # description
    try:
      copied_course = classroom_crud.update_course(classroom_id,
                        sections_details.name,
                        sections_details.description)
    except Exception as error:
      error = traceback.format_exc().replace("\n", " ")
      Logger.error(error)
      error_flag = True
      lms_job = LmsJob.find_by_id(lms_job_id)
      logs= lms_job.logs
      logs["errors"].append("Classroom course update failed")
      logs["errors"].append(error)
      lms_job.logs = logs
      lms_job.update()

    # Calling Classroom registrations API to send classroom event noifications
    try:
      classroom_crud.enable_notifications(copied_course["id"], "COURSE_WORK_CHANGES")
      classroom_crud.enable_notifications(copied_course["id"],
                                          "COURSE_ROSTER_CHANGES")
    except Exception as error:
      error = traceback.format_exc().replace("\n", " ")
      Logger.error(error)
      error_flag = True
      lms_job = LmsJob.find_by_id(lms_job_id)
      logs= lms_job.logs
      logs["errors"].append("Enable notification for classroom failed")
      logs["errors"].append(error)
      lms_job.logs = logs
      lms_job.update()
    # add instructional designer
    list_course_template_enrollment_mapping = CourseTemplateEnrollmentMapping\
      .fetch_all_by_course_template(course_template_details.key)
    if list_course_template_enrollment_mapping:
      for course_template_mapping in list_course_template_enrollment_mapping:
        try:
          add_instructional_designer_into_section(section,
                                            course_template_mapping)
        except Exception as error:
          error = traceback.format_exc().replace("\n", " ")
          Logger.error(f"Create teacher failed for \
              for {course_template_details.instructional_designer}")
          Logger.error(error)
    rows=[{
      "sectionId":section_id,\
      "courseId":copied_course["id"],\
      "classroomUrl":copied_course["alternateLink"],\
        "name":sections_details.name,\
        "description":sections_details.description,\
        "cohortId":cohort_details.id,\
        "courseTemplateId":course_template_details.id,\
          "status":section.status,\
        "enrollmentStatus": section.enrollment_status,
        "maxStudents": section.max_students,
          "timestamp":datetime.datetime.utcnow()
    }]
    insert_rows_to_bq(
        rows=rows,
        dataset=BQ_DATASET,
        table_name=BQ_TABLE_DICT["BQ_COLL_SECTION_TABLE"])
    if error_flag:
      section.status = "FAILED_TO_PROVISION"
    else:
      section.status = "ACTIVE"
    section.update()
    lms_job = LmsJob.find_by_id(lms_job_id)
    logs = lms_job.logs
    logs["info"].append(
        f"Background Task Completed for section Creation for cohort\
                {cohort_details.id}")
    logs["info"].append(f"Section Details are section id {section_id},\
                classroom id {classroom_id}")

    if error_flag:
      lms_job.status = "failed"
    else:
      lms_job.status = "success"
    Logger.info( f"Background Task Completed for section Creation for cohort\
                {cohort_details.id}")
    Logger.info(f"Section Details are section id {section_id},\
                classroom id {classroom_id} {lms_job.id}")
    lms_job.logs = logs
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.update()
    return True
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    Logger.error(e)
    logs["errors"].append(str(e))
    lms_job.logs = logs
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.status = "failed"
    lms_job.update()
    raise InternalServerError(str(e)) from e


def check_copy_course_alpha(original_courseworks,
                      original_coursework_materials,
                      copied_course,
                      lms_job_id, section_id,course_template_id):

  """
  This function checks if the copy course process is completed successfully
  It returns a boolean error flag if the error flag is True then copy course
  process had errors It can be missing coursework or coursework attachments
  """

  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs
  try:
    count = 0
    max_count = 3
    original_coursework_titles = sort_titles(original_courseworks)
    original_coursework_dict =  make_title_key_coursework(original_courseworks)
    original_coursework_material_titles = sort_titles(
      original_coursework_materials)
    original_coursework_material_dict =  make_title_key_coursework(
      original_coursework_materials)
    duplicate_coursework=[]
    duplicate_coursework_material=[]
    duplicate_coursework = [
    title for title in original_coursework_titles
      if original_coursework_titles.count(title) > 1]
    duplicate_coursework_material = [
    title for title in original_coursework_material_titles
      if original_coursework_material_titles.count(title) > 1]
    if duplicate_coursework or duplicate_coursework_material:
      Logger.error(
        f"Given course has duplicate coursework {duplicate_coursework}\
                  Duplicate coursework Material{duplicate_coursework_material}")
      logs["errors"].append(
        f"Given course has duplicate coursework {duplicate_coursework}\
                  Duplicate coursework Material{duplicate_coursework_material}")
      lms_job.logs = logs
      lms_job.update()
      error_flag =True
      return error_flag

    original_coursework_titles = set(original_coursework_titles)
    original_coursework_material_titles = set(original_coursework_material_titles)

    while count<max_count :
      Logger.info(f"Iteration  count {count} to verify copy_course process")
      logs["info"].append(f"Iteration  count {count} to verify copy_course process")
      time.sleep(120)
      count+=1
      error_flag = False
      copied_courseworks = classroom_crud.get_coursework_list(
        copied_course["id"],"DRAFT")
      copied_coursework_materials = classroom_crud.get_coursework_material_list(
            copied_course["id"],"DRAFT")

      # Get course title
      # Todo : Seperate these two conditions
      if copied_courseworks is None :
        Logger.error("Courseworks not copied ")
        logs["errors"].append("Courseworks not copied ")
        error_flag = True
        continue
      if copied_coursework_materials is None:
        Logger.error("Coursework material not copied ")
        logs["errors"].append("Coursework material not copied ")
        error_flag = True
        continue
      copied_coursework_titles = sort_titles(copied_courseworks)
      copied_coursework_material_titles = sort_titles(copied_coursework_materials)
      copied_coursework_titles = set(copied_coursework_titles)
      copied_coursework_material_titles = set(copied_coursework_material_titles)
      missing_coursework =[]
      missing_coursework_material = []
      title_mismatch_coursework = []
      title_mismatch_coursework_material =[]

      if copied_coursework_titles != original_coursework_titles:
        error_flag = True
        Logger.error("Length of coursework are not  matching")
        logs["errors"].append("Length of coursework are not  matching")
        missing_coursework = original_coursework_titles - copied_coursework_titles
        title_mismatch_coursework = copied_coursework_titles - original_coursework_titles

        if title_mismatch_coursework or missing_coursework:
          logs["errors"].append(f"Missing courseworks are {missing_coursework} or \
                                Title mismatch are {title_mismatch_coursework}")
          Logger.error(f"Missing courseworks are {missing_coursework} or\
                        Title mismatch are {title_mismatch_coursework}")

      if copied_coursework_material_titles != original_coursework_material_titles:
        error_flag = True
        Logger.error("Length of coursework Material are not matching")
        logs["errors"].append("Length of coursework Material are not  matching")
        missing_coursework_material = original_coursework_material_titles -\
            copied_coursework_material_titles
        title_mismatch_coursework_material =copied_coursework_material_titles -\
                                        original_coursework_material_titles
        if missing_coursework_material or title_mismatch_coursework_material:
          logs["errors"].append(
          f"Missing courseworks are {missing_coursework_material} or \
            Title mismatch are {title_mismatch_coursework_material}")
          Logger.error(f"Missing courseworks are {missing_coursework_material} or\
                        Title mismatch are {title_mismatch_coursework_material}")

      lms_job.logs = logs
      lms_job.update()

      # If there is mistmatch in coursework name or coursework name continue to wait
      if error_flag:
        continue

      # make_title_key_coursework function takes the list of coursework or coursework
      # material and returns a dictionary with keys as title and coursework_details as value
      copied_coursework_dict = make_title_key_coursework(
        copied_courseworks)
      copied_coursework_material_dict = make_title_key_coursework(
        copied_coursework_materials)
      for coursework_title in original_coursework_titles:
        missing_attachment=[]
        if "materials" in original_coursework_dict[coursework_title]:
          missing_attachment = verifiy_attachment(coursework_title,
                                                  original_coursework_dict,
                                                  copied_coursework_dict,
                                                  lms_job_id
                                                  )

        lms_job = LmsJob.find_by_id(lms_job_id)
        logs = lms_job.logs
        if missing_attachment:
          Logger.error(f"Missing attachment are {coursework_title} {missing_attachment }")
          logs["errors"].append(f"Missing attachment are {coursework_title} {missing_attachment }")
          error_flag=True
        else:
          logs["info"].append(f"No Missing attachment for {coursework_title}")
          Logger.info(f"No Missing attachment for {coursework_title}")
        lms_job.logs = logs
        lms_job.update()
        Logger.info("")
      #Errror in copying coursework attachments restart wait loop
      for coursework_material_title in original_coursework_material_titles:
        missing_attachment=[]
        if "materials" in original_coursework_material_dict[coursework_material_title]:
          missing_attachment = verifiy_attachment(coursework_material_title,
                                                  original_coursework_material_dict,
                                                  copied_coursework_material_dict,
                                                  lms_job_id)

        lms_job = LmsJob.find_by_id(lms_job_id)
        logs = lms_job.logs
        if  missing_attachment:
          Logger.error(f"Missing attachment are {coursework_material_title} {missing_attachment}")
          logs["errors"].append(f"Missing attachment are {coursework_material_title} {missing_attachment}")
          error_flag=True
        else :
          logs["info"].append(f"No Missing attachment for {coursework_material_title}")
          Logger.info(f" No Missing attachment for {coursework_material_title}")
        lms_job.logs = logs
        lms_job.update()
      if error_flag:
        continue
      else:
        break

    logs = lms_job.logs
    if not error_flag:
      for coursework in copied_courseworks:
        coursework_title = coursework["title"]

        lti_assignment_details = {
            "section_id": section_id,
            "coursework_title": coursework_title,
            "coursework_id": coursework["id"],
            "source_context_id": course_template_id,
            "start_date": None,
            "end_date": None,
            "due_date": None
        }
        material_update = False
        if "materials" in coursework.keys():
          for material in coursework["materials"]:
            if "link" in material.keys():
              link = material["link"]
              if "/classroom-shim/api/v1/launch?lti_assignment_id=" in link["url"]:
                copy_resp = copy_lti_shim_assignment(link["url"], lti_assignment_details, logs)
                logs = copy_resp["logs"]
                if copy_resp.get("copy_resp_status") == 200:
                  material_update = True
                  material["link"]["url"] = copy_resp.get("updated_lti_link")
                else:
                  error_flag = True
        try:
          updated_data = {"state": "PUBLISHED"}
          if "dueDate" in original_coursework_dict[coursework_title].keys():
            updated_data["dueDate"] = original_coursework_dict[coursework_title].get(
              "dueDate")
            if "dueTime" in original_coursework_dict[coursework_title].keys()  :
              updated_data["dueTime"]=original_coursework_dict[coursework_title].get("dueTime")
            else:
              updated_data["dueTime"]={
                "hours": 23,
                "minutes": 59,
                "seconds": 0
              }
          if material_update:
            updated_data["materials"] = coursework["materials"]
          update_mask = ",".join(updated_data)
          classroom_crud.patch_coursework_alpha(copied_course["id"],
                                                coursework["id"], update_mask,
                                                updated_data)
          logs["info"].append(f"Coursework published for {coursework_title}")
          Logger.info(f"Coursework published for {coursework_title}")
        except HttpError as error:
          Logger.error(error)
          error_flag=True
          logs["errors"].append(
            f"Coursework state update failed for {coursework_title}\
                                {error}")

      for coursework_material in copied_coursework_materials:
        coursework_material_title = coursework_material["title"]

        lti_assignment_details = {
            "section_id": section_id,
            "coursework_title": coursework_material_title,
            "coursework_id": coursework_material["id"],
            "source_context_id": course_template_id,
            "start_date": None,
            "end_date": None,
            "due_date": None
        }
        material_update = False
        if "materials" in coursework_material.keys():
          for material in coursework_material["materials"]:
            if "link" in material.keys():
              link = material["link"]
              if "/classroom-shim/api/v1/launch?lti_assignment_id=" in link["url"]:
                copy_resp = copy_lti_shim_assignment(link["url"], lti_assignment_details, logs)
                logs = copy_resp["logs"]
                if copy_resp.get("copy_resp_status") == 200:
                  material_update = True
                  material["link"]["url"] = copy_resp.get("updated_lti_link")
                else:
                  error_flag = True
        try:
          updated_data = {"state": "PUBLISHED"}
          if material_update:
            updated_data["materials"] = coursework_material["materials"]
          update_mask = ",".join(updated_data)
          classroom_crud.patch_coursework_material_alpha(
              copied_course["id"], coursework_material["id"], update_mask,
              updated_data)
          logs["info"].append(
            f"Coursework Material published for {coursework_material_title}")
          Logger.info(
            f"Coursework Material published for {coursework_material_title}")
        except HttpError as error:
          Logger.error(error)
          logs["errors"].append(
            f"Coursework Material state update failed for {coursework_material_title}\
                                {error}")


    logs["info"].append(
    f"Error flag to check copied items in copy course alpha is {error_flag}")
    lms_job.logs=logs
    lms_job.update()
    return error_flag
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(f"Error in check copy course -{error} {e}")
    logs["errors"].append(f"Error in check copy course -{error}")
    lms_job.logs =logs
    lms_job.update()
    return True

def verifiy_attachment(title ,original_coursework_dict,
                       copied_coursework_dict,lms_job_id):
  """
  This function is verifies the attachment of coursework
  It compares the original coursework dict and copid coursework dict
  returns the missing attachments in list
  """
  missing_attachments = set()
  original_drive_files= set()
  original_youtube_video= set()
  original_link=set()
  original_form=set()
  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs
  try:
    for attachment in original_coursework_dict[title]["materials"]:
      if "driveFile" in attachment.keys():
        original_drive_files.add(attachment["driveFile"]["driveFile"]["title"])
      if "youtubeVideo" in attachment.keys():
        original_youtube_video.add(attachment["youtubeVideo"]["title"])
      if "link" in attachment.keys():
        Logger.error(f"coursework{title} {attachment}")
        original_link.add(attachment["link"]["title"])
      if "form" in attachment.keys():
        original_form.add(attachment["form"]["title"])

    copied_drive_files= set()
    copied_youtube_video= set()
    copied_link= set()
    copied_form=set()
    for attachment in copied_coursework_dict[title]["materials"]:
      if "driveFile" in attachment.keys():
        copied_drive_files.add(attachment["driveFile"]["driveFile"]["title"])
      if "youtubeVideo" in attachment.keys():
        copied_youtube_video.add(attachment["youtubeVideo"]["title"])
      if "link" in attachment.keys():
        copied_link.add(attachment["link"]["title"])
      if "form" in attachment.keys():
        copied_form.add(attachment["form"]["title"])
    missing_attachments = []

    if original_drive_files != copied_drive_files:
      missing_drive_files = original_drive_files - copied_drive_files
      missing_attachments.extend(missing_drive_files)
    if original_youtube_video !=copied_youtube_video:
      missing_youtube_video = original_youtube_video - copied_youtube_video
      missing_attachments.extend(missing_youtube_video)

    if original_link != copied_link:
      missing_link = original_link - copied_link
      missing_attachments.extend(missing_link)

    if original_form != copied_form:
      missing_form = original_form - copied_form
      missing_attachments.extend(missing_form)

    return missing_attachments
  except Exception as e:
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(f"Error {title} in attachment -{error} {e}")
    logs["errors"].append(f"Error {title} in attachment -{error}")
    lms_job.logs =logs
    lms_job.update()
    return attachment


def make_title_key_coursework(courseworks):
  """This function takes the list of coursework dict and reurns
    update dictionary with keys as coursework titile and value as
    entire coursework object
  """
  updated_coursework_dict ={}
  for coursework in courseworks:
    updated_coursework_dict[coursework["title"]]=coursework
  return updated_coursework_dict

def sort_titles(courseworks):
  "This function sorts the tiles for coursework list"
  Logger.info(f"In sort titles {len(courseworks)}")
  titles = [coursework["title"] for coursework in courseworks]
  titles.sort()
  return titles

def update_coursework_material(materials,
                               url_mapping,
                               target_folder_id,
                               error_flag,
                               lti_assignment_details=None,
                               logs=None):
  """Takes the material attached to any type of cursework and copy it in the
    target folder Id also removes duplicates from material list
  Args:
    materials (list of dictionary): Coursework materials list which is obtained
      from list coursework method
    url_mapping (dict):Dict of view url as key and edit url, fileid as values
    target_folder_id(str):Drive folder Id of section
  Returns:
    updated_material : (list of dict) returns a updated
  """
  drive_ids = []
  youtube_ids = []
  link_urls = []
  updated_material = []
  lti_assignment_ids = []
  # Loop to check the different types of material attached to coursework
  # 1.If a material is driveFile call called copy_material function which
  #  copies is drivefile in target_folder_id and updates the driveFile
  #  dict with new file id for section drive folder
  # 2.If a material is YoutubeVideo or link check for duplicate youtube
  #   video and link
  # 3.If a material is form use url_mapping dictionary to get the file_id
  # of form which is used to copy form in target_folder_id of section and
  # attach form as link in coursework since attaching forms via api is not
  # supported by classroom

  for material in materials:
    if "driveFile" in material.keys():
      if material["driveFile"]["driveFile"]["id"] not in drive_ids:
        classroom_crud.copy_material(material, target_folder_id)
        drive_ids.append(material["driveFile"]["driveFile"]["id"])
        updated_material.append({"driveFile": material["driveFile"]})

    if "youtubeVideo" in material.keys():
      if material["youtubeVideo"]["id"] not in youtube_ids:
        youtube_ids.append(material["youtubeVideo"]["id"])
        updated_material.append({"youtubeVideo": material["youtubeVideo"]})
    if "link" in material.keys():
      if material["link"]["url"] not in link_urls:
        link = material["link"]

        # Update lti assignment with the course work/course work material details
        if "/classroom-shim/api/v1/launch?lti_assignment_id=" in link["url"]:
          split_url = link["url"].split(
              "/classroom-shim/api/v1/launch?lti_assignment_id=")
          lti_assignment_id = split_url[-1]
          coursework_title = lti_assignment_details.get("coursework_title")
          logs["info"].append(
              f"LTI Course copy started for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'")
          Logger.info(
              f"LTI Course copy started for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'")
          copy_assignment = requests.post(
              "http://classroom-shim/classroom-shim/api/v1/lti-assignment/copy",
              headers={
                  "Authorization": f"Bearer {auth_client.get_id_token()}"
              },
              json={
                  "lti_assignment_id": lti_assignment_id,
                  "context_id": lti_assignment_details.get("section_id"),
                  "source_context_id": lti_assignment_details.get("source_context_id"),
                  "start_date": lti_assignment_details.get("start_date"),
                  "end_date": lti_assignment_details.get("end_date"),
                  "due_date": lti_assignment_details.get("due_date")
              },
              timeout=60)

          if copy_assignment.status_code == 200:
            new_lti_assignment_id = copy_assignment.json().get("data").get(
                "id")
            updated_material_link_url = link["url"].replace(
                lti_assignment_id, new_lti_assignment_id)
            lti_assignment_ids.append(new_lti_assignment_id)

            updated_material.append(
                {"link": {
                    "url": updated_material_link_url
                }})
            Logger.info(
                f"LTI Course copy completed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}', new assignment id - {new_lti_assignment_id}"
            )
            logs["info"].append(
                f"LTI Course copy completed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}', new assignment id - {new_lti_assignment_id}"
            )
          else:
            logs["info"].append(
                f"LTI Course copy failed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'"
            )
            error_msg = f"Copying an LTI Assignment failed for {lti_assignment_id}, coursework title - '{coursework_title}'\
                          in the new section {lti_assignment_details.get('section_id')} with status code: \
                          {copy_assignment.status_code} and error msg: {copy_assignment.text}"

            logs["errors"].append(error_msg)
            Logger.error(error_msg)
            error_flag = True
        else:
          updated_material.append({"link": material["link"]})

        link_urls.append(material["link"]["url"])

    if "form" in material.keys():
      if "title" not in material["form"].keys():
        raise ResourceNotFound("Form to be copied is deleted")
      result1 = classroom_crud.drive_copy(
          url_mapping[material["form"]["formUrl"]]["file_id"], target_folder_id,
          material["form"]["title"])
      material["link"] = {
          "title": material["form"]["title"],
          "url": result1["webViewLink"]
      }
      updated_material.append({"link": material["link"]})
      material.pop("form")

  return {
      "material": updated_material,
      "error_flag": error_flag,
      "lti_assignment_ids": lti_assignment_ids
  }


def update_grades(material, section, coursework_id, lms_job_id):
  """Takes the forms all responses ,section, and coursework_id and
  updates the grades of student who have responsed to form and
  submitted the coursework
  """
  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs

  try:
    student_grades = {}
    count = 0

    info_msg = f"Student grade update background tasks started\
                for coursework_id {coursework_id}"

    logs["info"].append(info_msg)
    Logger.info(info_msg)
    lms_job.start_time = datetime.datetime.utcnow()
    lms_job.status = "running"
    lms_job.update()

    #Get url mapping of google forms view links and edit ids
    url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
    form_details = url_mapping[material["form"]["formUrl"]]

    form_id = form_details["file_id"]
    # Get all responses for the form if no responses of
    # the form then return
    all_responses_of_form = classroom_crud.\
    retrieve_all_form_responses(form_id)

    if all_responses_of_form == {}:
      logs["errors"].append("Responses not available for google form")
      Logger.error("Responses not available for google form")

    for response in all_responses_of_form.get("responses", []):
      try:
        if "respondentEmail" not in response.keys():
          error_msg = f"Respondent Email is not collected in form for\
          coursework {coursework_id} Update form settings to collect Email"

          logs["errors"].append(error_msg)
          raise Exception(error_msg)

        respondent_email = response["respondentEmail"]
        submissions = classroom_crud.list_coursework_submissions_user(
            section.classroom_id, coursework_id, response["respondentEmail"])

        if submissions:
          if submissions[0]["state"] == "TURNED_IN":
            logs["info"].append(f"Updating grades for {respondent_email}")
            Logger.info(f"Updating grades for {respondent_email}")

            if "totalScore" not in response.keys():
              response["totalScore"] = 0
            classroom_crud.patch_student_submission(section.classroom_id,
                                                    coursework_id,
                                                    submissions[0]["id"],
                                                    response["totalScore"],
                                                    response["totalScore"])
            count += 1
            student_grades[response["respondentEmail"]] = response["totalScore"]
            logs["info"].append(f"Updated grades for {respondent_email}")
            Logger.info(f"Updated grades for {respondent_email}")

          else:
            logs["info"].append(
                f"Submission state is not turn in {respondent_email}")
            Logger.info(f"Submission state is not turn in {respondent_email}")

      except Exception as e:
        error = traceback.format_exc().replace("\n", " ")
        Logger.error(error)
        Logger.error(e)
        logs["errors"].append(f"Error - {e}")
        continue

    Logger.info(f"Student grades updated\
                  for {count} student_data {student_grades}")

    logs["info"].append(f"Student grades updated\
                  for {count} student_data {student_grades}")
    lms_job.logs = logs
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.status = "success"
    lms_job.update()

    return count, student_grades

  except Exception as e:
    Logger.error(f"Grade import failed due to error - {str(e)}")
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(f"Traceback - {error}")

    logs["errors"].append(f"Grade import failed due to error - {str(e)}")
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.logs = logs
    lms_job.status = "failed"
    lms_job.update()

    raise InternalServerError(str(e)) from e


def add_teacher(headers, section, teacher_email):
  """_summary_

  Args:
      headers (_type_): _description_
      course_id (_type_): _description_
      teacher_email (_type_): _description_
  """
  invitation_object = classroom_crud.invite_user(section.classroom_id,
                                                 teacher_email, "TEACHER")
  try:
    classroom_crud.acceept_invite(invitation_object["id"], teacher_email)
    user_profile = classroom_crud.\
        get_user_profile_information(teacher_email)

    data = {
        "first_name": user_profile["name"]["givenName"],
        "last_name": user_profile["name"]["familyName"],
        "email": teacher_email,
        "user_type": "faculty",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False,
        "gaia_id": user_profile["id"],
        "photo_url": user_profile["photoUrl"]
    }
    status = "active"
    invitation_id = ""
  except Exception as hte:
    Logger.info(hte)
    data = {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": teacher_email,
        "user_type": "faculty",
        "user_groups": [],
        "status": "active",
        "is_registered": True,
        "failed_login_attempts_count": 0,
        "access_api_docs": False
    }
    status = "invited"
    invitation_id = invitation_object["id"]
  user_dict = common_service.create_teacher(headers, data)
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.role = "faculty"
  course_enrollment_mapping.user = User.find_by_user_id(user_dict["user_id"])
  course_enrollment_mapping.status = status
  course_enrollment_mapping.invitation_id = invitation_id
  course_enrollment_mapping.save()
  insert_section_enrollment_to_bq(course_enrollment_mapping,section)
  return course_enrollment_mapping

def validate_section(section):
  """
  Validate the section if it is eligile for enrollment
  validate the count of enrolled students ,enrollment status, max_students
  """
  if section.enrolled_students_count >= section.max_students:
    raise ValidationError(
      "Maximum student count reached for section hence student can't be enrolled"
      )
  Logger.info(f"Enrollment status  {section.enrolled_students_count} {section.status}")
  if section.enrollment_status !="OPEN" or section.status != "ACTIVE":
    raise ValidationError("Enrollment is not active for this section"
      )
  return True


def add_instructional_designer_into_section(section, course_template_mapping):
  """Add instructional designer into section

  Args:
      section (Section): section object
      course_template_mapping (CourseTemplateMapping):
      course template enrollment mapping object

  Returns:
      CourseEnrollmentMapping: enrollment mapping
  """
  invitation_object = classroom_crud.invite_user(
    section.classroom_id, course_template_mapping.user.email, "TEACHER")
  classroom_crud.acceept_invite(invitation_object["id"],
                                course_template_mapping.user.email)
  status = "active"
  course_enrollment_mapping = CourseEnrollmentMapping()
  course_enrollment_mapping.section = section
  course_enrollment_mapping.role = "faculty"
  course_enrollment_mapping.user = course_template_mapping.user
  course_enrollment_mapping.status = status
  course_enrollment_mapping.save()
  insert_section_enrollment_to_bq(course_enrollment_mapping,section)
  return course_enrollment_mapping

def insert_section_enrollment_to_bq(enrollment_record,section):
  """helper function to insert enrollment record to BQ

  Args:
    enrollment_record (CourseEnrollmentMapping): enrollment object
    section (Section): section object
  """
  rows=[{
        "enrollment_id" : enrollment_record.id,
        "email" : enrollment_record.user.email,
        "user_id" : enrollment_record.user.user_id,
        "role" : enrollment_record.role,
        "status" : enrollment_record.status,
        "invitation_id" : enrollment_record.invitation_id,
        "section_id" : section.id,
        "cohort_id" : section.cohort.id,
        "course_id" : section.classroom_id,
        "timestamp" : datetime.datetime.utcnow()
      }]
  insert_rows_to_bq(
            rows=rows, dataset=BQ_DATASET,
            table_name=BQ_TABLE_DICT["BQ_ENROLLMENT_RECORD"])


def copy_lti_shim_assignment(link, lti_assignment_details, logs):
  """Makes a copy of the given LTI Assignment in the new context"""
  split_url = link.split("/classroom-shim/api/v1/launch?lti_assignment_id=")
  lti_assignment_id = split_url[-1]
  coursework_title = lti_assignment_details.get("coursework_title")
  logs["info"].append(
      f"LTI Course copy started for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'"
  )
  Logger.info(
      f"LTI Course copy started for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'"
  )
  copy_assignment = requests.post(
      "http://classroom-shim/classroom-shim/api/v1/lti-assignment/copy",
      headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
      json={
          "lti_assignment_id": lti_assignment_id,
          "context_id": lti_assignment_details.get("section_id"),
          "source_context_id": lti_assignment_details.get("source_context_id"),
          "course_work_id": lti_assignment_details.get("coursework_id"),
          "start_date": lti_assignment_details.get("start_date"),
          "end_date": lti_assignment_details.get("end_date"),
          "due_date": lti_assignment_details.get("due_date")
      },
      timeout=60)

  copy_resp_status = copy_assignment.status_code
  final_resp = {"copy_resp_status": copy_resp_status}

  if copy_resp_status == 200:
    new_lti_assignment_id = copy_assignment.json().get("data").get("id")
    updated_material_link_url = link.replace(lti_assignment_id,
                                             new_lti_assignment_id)
    Logger.info(
        f"LTI Course copy completed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}', new assignment id - {new_lti_assignment_id}"
    )
    logs["info"].append(
        f"LTI Course copy completed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}', new assignment id - {new_lti_assignment_id}"
    )
    final_resp["updated_lti_link"] = updated_material_link_url
  else:
    logs["info"].append(
        f"LTI Course copy failed for assignment - {lti_assignment_id}, coursework title - '{coursework_title}'"
    )
    error_msg = f"Copying an LTI Assignment failed for {lti_assignment_id}, coursework title - '{coursework_title}'\
                  in the new section {lti_assignment_details.get('section_id')} with status code: \
                  {copy_resp_status} and error msg: {copy_assignment.text}"

    logs["errors"].append(error_msg)
    Logger.error(error_msg)
  final_resp["logs"] = logs
  return final_resp

def post_null_value_background_task(section_details,coursework_id_details,lms_job_id):
  """Post null grade for a courseworkid
  """
  lms_job = LmsJob.find_by_id(lms_job_id)
  logs = lms_job.logs
  try:
    lms_job.start_time = datetime.datetime.utcnow()
    lms_job.status = "running"
    lms_job.update()
    classroom_submissions = classroom_crud.list_coursework_submissions\
        (section_details.classroom_id,coursework_id_details)
    for student in classroom_submissions:
      if student.get("assignedGrade") is None:
        classroom_crud.post_grade_of_the_user\
          (section_details.id,coursework_id_details,student["id"],0,0)
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.status = "success"
    lms_job.update()

  except Exception as e:
    Logger.error(f"Post null grade failed due to error - {str(e)}")
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(f"Traceback - {error}")
    logs["errors"].append(f"Post null grade failed due to error - {str(e)}")
    lms_job.end_time = datetime.datetime.utcnow()
    lms_job.logs = logs
    lms_job.status = "failed"
    lms_job.update()


