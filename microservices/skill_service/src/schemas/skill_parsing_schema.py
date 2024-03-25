"""
Pydantic Model for Skill-Parsing
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, conlist

class SkillParsingByQueryRequestModel(BaseModel):
  name: Optional[str]
  description : Optional[str]
  top_k: Optional[int] = 10
  skill_alignment_sources: Optional[List[str]] = ["snhu"]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "name": "API Design",
            "description": "In computing, an application programming interface "
                "(API) is an interface that defines interactions between "
                "multiple software applications or mixed hardware-software "
                "intermediaries. It defines the kinds of calls or requests that"
                " can be made, how to make them, the data formats that should "
                "be used, the conventions to follow, etc. It can also provide "
                "extension mechanisms so that users can extend existing "
                "functionality in various ways and to varying degrees. An API "
                "can be entirely custom, specific to a component, or designed "
                "based on an industry-standard to ensure interoperability. "
                "Through information hiding, APIs enable modular programming, "
                "allowing users to use the interface independently of the "
                "implementation.",
            "top_k": 5,
            "skill_alignment_sources": [
                "osn"
            ]
        }
    }


class SkillParsingByIdRequestModel(BaseModel):
  ids: conlist(str, min_items=1)
  top_k: Optional[int] = 10
  skill_alignment_sources: Optional[List[str]] = ["snhu"]

  class Config():
    orm_mode = True
    schema_extra = {
       "example": {
            "ids": [
                "05C6gGMNsoBpjT85c0fO",
                "06u327hrFYJVvSlUcX3T"
            ],
            "top_k": 10,
            "skill_alignment_sources": [
                "osn"
            ]
        }
   }


class AlignAllRequestModel(BaseModel):
  ids: Optional[List[str]]
  source_name: Optional[List[str]]
  top_k: Optional[int] = 10
  skill_alignment_sources: List[str]
  update_alignments: Optional[bool] = True

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "ids": ["06u327hrFYJVvSlUcX3T"],
            "source_name": ["o*net"],
            "top_k": 5,
            "skill_alignment_sources" : ["emsi"],
            "update_alignments": True
        }
    }



class MappingObject(BaseModel):
  name: str
  id: str
  score: float

class QueryData(BaseModel):
  name: str
  description : str
  aligned_skills: Dict[str, List[MappingObject]]

class IdData(BaseModel):
  aligned_skills: Dict[str, Dict[str, List[MappingObject]]]


class SkillParsingByQueryResponseModel(BaseModel):
  success: bool = True
  message: str = "Successfully extracted skills from given query"
  data: Optional[QueryData]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
          "success": True,
          "message": "Successfully extracted skills from given query",
          "data": {
            "name": "cyber security",
            "description": "",
            "aligned_skills": [{"name": "name", "id": "id",
                     "score": 0
            }]
          }
        }
      }


class BaseResponse(BaseModel):
  name: str
  id: str
  score: float

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "id": "0pgLV4eAsbzdMLVzFul5",
            "name": "Communication Access",
            "score": 0.9822302460670471
        }
    }

class SkillParsingByIdResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully found the alignments for\
     given skill(s)"
  data: Optional[IdData]

  class Config():
    orm_mode = True
    schema_extra = {
       "example": {
           "success": True,
           "message": "Successfully found the alignments for given skill(s)",
           "data": {
              "aligned_skills": {
                "019K8aiPapVS1qF5omVl": {
                    "emsi": [
                        {
                            "name": "International Association Of Engineers",
                            "id": "KS124XB6K4SGGNZYFZJG",
                            "score": 0.41999998688697815
                        },
                        {
                            "name": "Certified Engineering Technologist",
                            "id": "KS121LM6HCBPJZYFPSL8",
                            "score": 0.3720000088214874
                        },
                        {
                            "name": "Chartered Engineer",
                            "id": "KS121K86SHMK9X46YPWT",
                            "score": 0.5649999976158142
                        }
                    ]
                },
                "05C6gGMNsoBpjT85c0fO": {
                    "emsi": [
                        {
                            "name": "Bookbinding",
                            "id": "ES4F86CE1E7AB8D7BB46",
                            "score": 0.5649999976158142
                        },
                        {
                            "name": "Book Printing",
                            "id": "KS1214J6FRTK453B6F4L",
                            "score": 0.4959999918937683
                        },
                        {
                            "name": "Print Servers",
                            "id": "KS126ZM787JTJ3Z7TVQX",
                            "score": 0.47699999809265137
                        },
                        {
                            "name": "Printing Press",
                            "id": "ESCF77734F2CFD90FDA6",
                            "score": 0.4950000047683716
                        },
                        {
                            "name": "Print Shops",
                            "id": "KS128116S1F5PP2B598V",
                            "score": 0.4959999918937683
                        },
                        {
                            "name": "Comb Binding",
                            "id": "KS1224973ZJQDYTB1Z3W",
                            "score": 0.5659999847412109
                        },
                        {
                            "name": "Wire Binding",
                            "id": "KS4423T60NS7B2BBXC4B",
                            "score": 0.5260000228881836
                        },
                        {
                            "name": "Xerox Copiers",
                            "id": "BGS937CBD2778845F9D9",
                            "score": 0.5019999742507935
                        },
                        {
                            "name": "Print Production",
                            "id": "ES7741B7C8D0491E7BCC",
                            "score": 0.6970000267028809
                        },
                        {
                            "name": "Print Finishing Systems",
                            "id": "KS128116BHVDNTZPWLFX",
                            "score": 0.6970000267028809
                        }
                    ]
                }
             }
          }
       }
   }
