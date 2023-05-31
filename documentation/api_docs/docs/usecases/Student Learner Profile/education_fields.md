---
sidebar_label: Learner Profile Education Fields
sidebar_position: 4
---
# API to fetch all education fields

To fetch all the options for potential career goals, education goals and employment status related to education tab of learner profile, a **GET** request is made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner-profile/education-fields`**

This will return a json response as follows:

```json
{
        "success": true,
        "message": "Successfully fetched the possible options for"
        " education goals, employment status, potential career fields",
        "data": {
            "education_goals" : [
              "To be able to do what I love",
              "To start a new career",
              "To make more money",
              "To provide a better life for my family",
              "To feel proud of what I've done",
              "To advance my existing career",
              "To make my family proud of me",
              "To make the world a better place"
            ],

            "employment_status" : [
              "Full-time",
              "Part-time",
              "Seeking work",
              "Unemployed"
            ],

            "potential_career_fields" : [
              {
                "field_name": "Architecture, engineering",
                "examples": "e.g., architect, drafter, electrical engineer"
              },
              {
                "field_name": "Arts, design, entertainment, sports, media",
                "examples": "e.g., fashion designer, video editor, author"
              },
              {
                "field_name": "Business, financial operations",
                "examples": "e.g., project manager, accountant, human resources specialist, marketing specialist"
              },
              {
                "field_name": "Community, social services",
                "examples": "e.g., social worker, clergy, community health worker"
              },
              {
                "field_name": "Computers, mathematics",
                "examples": "e.g., video game designer, actuary"
              },
              {
                "field_name": "Construction, extraction",
                "examples": "e.g., general contractor, carpenter, electrician"
              },
              {
                "field_name": "Educational instruction, library sciences",
                "examples": "e.g., teacher, professor, librarian"
              },
              {
                "field_name": "Farming, fishing, forestry",
                "examples": "e.g., forest ranger, animal breeder, agricultural inspector"
              },
              {
                "field_name": "Food preparation, service",
                "examples": "e.g., chef, bartender"
              },
              {
                "field_name": "Healthcare",
                "examples": "e.g., medical transcriptionist, pharmacist, registered nurse, medical assistant"
              },
              {
                "field_name": "Installation, maintenance, repair",
                "examples": "e.g., HVAC technician, auto mechanic, locksmith"
              },
              {
                "field_name": "Legal", "examples": "e.g., lawyer, paralegal"
              },
              {
                "field_name": "Personal care, service",
                "examples": "e.g., animal trainer, funeral attendant, cosmetologist"
              },
              {
                "field_name": "Protective service",
                "examples": "e.g., police officer, firefighter"
              },
              {
                "field_name": "Sales",
                "examples": "e.g., insurance agent, sales representative, real estate broker"
              },
              {
                "field_name": "Sciences (life, physical, social)",
                "examples": "e.g., chemist, clinical psychologist, forensic scientist"
              },
              {
                "field_name": "Support (office, administrative)",
                "examples": "e.g., executive secretary, proofreader, data entry clerk"
              },
              {
                "field_name": "Something else not listed here", "examples": ""
              }
            ]
          }

    }
```