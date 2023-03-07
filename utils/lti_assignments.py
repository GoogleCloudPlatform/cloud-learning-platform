from common.models import LTIAssignment

assignments = LTIAssignment.collection.filter("tool_id", "==",
                                              "aJ4149mb6aOH805OrAr4").fetch()
print("| context\_id | resource\_id | assignment\_id")
print("| :--- | :--- |")
for assignment in assignments:
  print(
      f"{assignment.section_id} | {assignment.lti_content_item_id} | {assignment.id}"
  )
