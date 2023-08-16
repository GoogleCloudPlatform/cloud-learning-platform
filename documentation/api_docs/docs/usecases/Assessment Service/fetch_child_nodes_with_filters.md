---
sidebar_label: Fetch child nodes with filters
sidebar_position: 2
---

# Filter Submitted Assessments for an assessor

To fetch a list of child nodes with filters from a given node_id and node_type in the learning hierarchy, the following
endpoint will be used:
**`<APP_URL>/learning-object-service/api/v1/{level}/{node_id}/nodes/{node_type}`**


Possible values for the path parameters:
| Path Parameter   |      Type      |  Description |
|----------|:-------------:|------:|
| level |  str | Literal[curriculum-pathways, learning-experiences, learning-objects, learning-resources, assessments] |
| node_id |  str | Name of the Assessment Data Item that will be created |
| node_type |  str | Literal[curriculum-pathways, learning-experiences, learning-objects, learning-resources, assessments, skills, competencies] |


The endpoint uses the following query parameters:
| Query Parameter   |      Type      |  Description |
|----------|:-------------:|------:|
| alias |  str | Alias applicable to the node_type mentioned in path parameter |
| type |  str | Type applicable to the node_type mentioned in path parameter |
| is_autogradable |  bool | Applicable only when filtering on assessments node_type |

**EXAMPLE**

**Endpoint = `<APP_URL>/learning-object-service/api/v1/learning-objects/UnuAiIGOXksIjNWgK3DN/nodes/assessments`**.

Upon successfully hitting the above endpoint would give the following response:
```json
{
    "success": true,
    "message": "Data fetched successfully",
    "data": [
        {
            "uuid": "8AfFxGfuezOYgNLZ4plZ",
            "collection": "assessments",
            "description": "",
            "name": "Submit your project",
            "alias": "assessment",
            "type": "project",
            "is_autogradable": null
        }
    ]
}
```