---
sidebar_label: Deletion of user events
sidebar_position: 5
---

# Deletion of user events using course_id and/or user_id

The following are possible scanrios for deleting use_events from the collection

### Scenario 1:

If the user wants to delete user_events filtered on a specific user_id and course_id

The user needs to enter the required user_id and course_id, and a filtered list of user_events containg the given user_id and course_id will be deleted from the collection.

When we need to delete a user_item/set of user_items then we would make a DELETE request to the API endpoint - <APP_URL>/deep-knowledge-tracing/api/v1/delete.
The request body should have a valid user_id and/or course_id for deleting the user_events.

user can delete user_events filtered based on user_id, course_id, or using both. However, the user cannot delete have both the fields(user_id and course_id) set to blank

Once the events are deleted succesfully, it shows up the following response:

```json
{
  "success": true,
  "message": "Successfully deleted the user events",
  "deleted_user_events": ["uuid1", "uiid2"]
}
```

### Scenario 2:

If the user enters an invalid user_id or course_id, then no deletion of user_event takes place, rather an appropriate error message is returned.
Invalid user_id or course_id can also represent values that are not existing in the collection i.e no user event exist with the given user_id or course_id or the combination of both

Sample response on entering invalid user_id and/or course_id:

```json
{
  "success": false,
  "message": "No such user event data found",
  "deleted_user_events": []
}
```

