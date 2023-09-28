---
sidebar_label: Fetch Child Nodes
sidebar_position: 1
---

# Fetch Child Nodes

### Fetch all child skills for a list of competencies

To fetch the child skills for a list of competencies, a **GET** request has to be made to the API endpoint - **`<APP_URL>/skill-service/api/v1/competencies/fetch_skills?competencies=<competency_id1>&competencies=<competency_id2>`**.

Here, competencies is passed as a list to the query parameter with values `[<competency_id1>, <competency_id2>]`


The above stated response is a list of skill name and ids assigned to each competency in the query parameter.

```json
    {
        "success": true,
        "message": "Successfully created FAQ",
        "data": {
          "<competency_id1>" : [
            {
              "skill_name": "<skill_id1>",
              "skill_id": "<skill_name1>"
            },
            {
              "skill_name": "<skill_id2>",
              "skill_id": "<skill_name2>"
            }
            ],
          "competency_2" :  [
            {
              "skill_name": "<skill_id3>",
              "skill_id": "<skill_name3>"
            },
            {
              "skill_name": "<skill_id4>",
              "skill_id": "<skill_name4>"
            }
            ]
        }
    }
```

