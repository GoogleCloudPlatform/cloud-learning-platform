"""
Pydantic Model for Skill to Knowledge alignment APIs
"""
from typing import List, Optional
from pydantic import BaseModel

# pylint: disable= line-too-long

class SkillToPassageByIdRequestModel(BaseModel):
  """Request Model"""
  ids: List[str]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "ids":
                ["ZJYw5XczcLAEtdM081oG"]
        }
    }


class SkillToPassageByQueryRequestModel(BaseModel):
  """Request Model"""
  name: Optional[str] = ""
  description: Optional[str] = ""

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "name": "Power Plant Operators",
            "description": "Control, operate, or maintain machinery to "
                "generate electric power. Includes auxiliary equipment "
                "operators."
          }
      }


class LUItem(BaseModel):
  """Model for LU item"""
  lu_id: str
  lu_score: float
  passages: List[str]
  passage_scores: List[float]
  learning_resource_id: str

class SkillQueryItem(BaseModel):
  """Model for Skill Item"""
  name: str
  description: str
  learning_units: List[LUItem]


class SkillToPassageQueryResponseModel(BaseModel):
  """Response model"""
  success: bool = True
  message: str = "Successfully Mapped the Skill to Knowledge"
  data: Optional[SkillQueryItem]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully Mapped the Skill to Knowledge",
        "data": {
            "name": "Purpose of Operating Systems",
            "description": "",
            "learning_units": [
                {
                    "lu_id": "jDz7evRd6WtnoZHVApqW",
                    "lu_score": 0.25,
                    "passages": [
                        "Before closing this introduction, let us present a brief history of how operating systems developed. Like any system built by humans, good ideas accumulated in operating systems over time, as engineers learned what was important in their design. Here, we discuss a few major devel- opments. For a richer treatment, see Brinch Hansen's excellent history of operating systems [BH00]."
                    ],
                    "passage_scores": [
                        0.7218145132064819
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                },
                {
                    "lu_id": "xefHtOUvPwXYphhRChpk",
                    "lu_score": 1.0,
                    "passages": [
                        "One goal in designing and implementing an operating system is to provide high performance ; another way to say this is our goal is to mini- mize the overheads of the OS. Virtualization and making the system easy to use are well worth it, but not at any cost; thus, we must strive to pro- vide virtualization and other OS features without excessive overheads.\n c ⃝ 2008–20, A -D",
                        "In the beginning, the operating system didn't do too much. Basically, it was just a set of libraries of commonly-used functions; for example, instead of having each programmer of the system write low-level I/O handling code, the \"OS\" would provide such APIs, and thus make life easier for the developer.",
                        "There is a body of software, in fact, that is responsible for making it easy to run programs (even allowing you to seemingly run many at the same time), allowing programs to share memory, enabling programs to interact with devices, and other fun stuff like that. That body of software 1 2 I O S T C P : H T V R One central question we will answer in this book is quite simple: how does the operating system virtualize resources? This is the crux of our problem. Why the OS does this is not the main question, as the answer should be obvious: it makes the system easier to use. Thus, we focus on the how : what mechanisms and policies are implemented by the OS to attain virtualization? How does the OS do so efficiently? What hardware support is needed? We will use the \"crux of the problem\", in shaded boxes such as this one, as a way to call out specific problems we are trying to solve in building an operating system. Thus, within a note on a particular topic, you may find one or more cruces (yes, this is the proper plural) which highlight the problem. The details within the chapter, of course, present the solution, or at least the basic parameters of a solution.\n is called the operating system ( OS ), as it is in charge of making sure the system operates correctly and efficiently in an easy-to-use manner."
                    ],
                    "passage_scores": [
                        0.9950962662696838,
                        0.8456541895866394,
                        0.7289135456085205
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                },
                {
                    "lu_id": "kaAKiOncIfjgwM9Uzm9y",
                    "lu_score": 0.25,
                    "passages": [
                        "The operating system must also run non-stop; when it fails, all appli- cations running on the system fail as well. Because of this dependence, operating systems often strive to provide a high degree of reliability . As operating systems grow evermore complex (sometimes containing mil- lions of lines of code), building a reliable operating system is quite a chal- lenge — and indeed, much of the on-going research in the field (including some of our own work [BS+09, SS+10]) focuses on this exact problem."
                    ],
                    "passage_scores": [
                        0.9603123664855957
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                },
                {
                    "lu_id": "NctXsNCc6YCqmX9Tw5Xc",
                    "lu_score": 0.3333333333333333,
                    "passages": [
                        "I O S 17 Thus, we have an introduction to the OS. Today's operating systems make systems relatively easy to use, and virtually all operating systems you use today have been influenced by the developments we will discuss throughout the book."
                    ],
                    "passage_scores": [
                        0.8585056662559509
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                },
                {
                    "lu_id": "mrkbBOyHjguHpH3Zcjfw",
                    "lu_score": 0.3333333333333333,
                    "passages": [
                        "Because we wish to allow many programs to run at the same time, we want to make sure that the malicious or accidental bad behavior of one does not harm others; we certainly don't want an application to be able to harm the OS itself (as that would affect all programs running on the system). Protection is at the heart of one of the main principles underlying an operating system, which is that of isolation ; isolating processes from one another is the key to protection and thus underlies much of what an OS must do."
                    ],
                    "passage_scores": [
                        0.5853044390678406
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                },
                {
                    "lu_id": "QLlhc7Oud5Xs7YRSS9od",
                    "lu_score": 0.5,
                    "passages": [
                        "So now you have some idea of what an OS actually does: it takes phys- ical resources, such as a CPU, memory, or disk, and virtualizes them. It handles tough and tricky issues related to concurrency . And it stores files persistently, thus making them safe over the long-term. Given that we want to build such a system, we want to have some goals in mind to help focus our design and implementation and make trade-offs as necessary; finding the right set of trade-offs is a key to building systems."
                    ],
                    "passage_scores": [
                        0.5805456042289734
                    ],
                    "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                }
            ]
        }
    }
  }



class SkillIdItem(BaseModel):
  """Model for Skill Item"""
  id: str
  learning_units: List[LUItem]

class SkillToPassageIdResponseModel(BaseModel):
  """Response model"""
  success: bool = True
  message: str = "Successfully Mapped the Skill to Knowledge"
  data: Optional[List[SkillIdItem]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully Mapped the Skill to Knowledge",
        "data": [
            {
                "id": "3kx3zp90VE6Xxckn1zCI",
                "learning_units": [
                    {
                        "lu_id": "jDz7evRd6WtnoZHVApqW",
                        "lu_score": 0.25,
                        "passages": [
                            "Before closing this introduction, let us present a brief history of how operating systems developed. Like any system built by humans, good ideas accumulated in operating systems over time, as engineers learned what was important in their design. Here, we discuss a few major devel- opments. For a richer treatment, see Brinch Hansen's excellent history of operating systems [BH00]."
                        ],
                        "passage_scores": [
                            0.8482568860054016
                        ],
                        "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                    },
                    {
                        "lu_id": "xefHtOUvPwXYphhRChpk",
                        "lu_score": 1.0,
                        "passages": [
                            "One goal in designing and implementing an operating system is to provide high performance ; another way to say this is our goal is to mini- mize the overheads of the OS. Virtualization and making the system easy to use are well worth it, but not at any cost; thus, we must strive to pro- vide virtualization and other OS features without excessive overheads.\n c ⃝ 2008–20, A -D",
                            "In the beginning, the operating system didn't do too much. Basically, it was just a set of libraries of commonly-used functions; for example, instead of having each programmer of the system write low-level I/O handling code, the \"OS\" would provide such APIs, and thus make life easier for the developer.",
                            "There is a body of software, in fact, that is responsible for making it easy to run programs (even allowing you to seemingly run many at the same time), allowing programs to share memory, enabling programs to interact with devices, and other fun stuff like that. That body of software 1 2 I O S T C P : H T V R One central question we will answer in this book is quite simple: how does the operating system virtualize resources? This is the crux of our problem. Why the OS does this is not the main question, as the answer should be obvious: it makes the system easier to use. Thus, we focus on the how : what mechanisms and policies are implemented by the OS to attain virtualization? How does the OS do so efficiently? What hardware support is needed? We will use the \"crux of the problem\", in shaded boxes such as this one, as a way to call out specific problems we are trying to solve in building an operating system. Thus, within a note on a particular topic, you may find one or more cruces (yes, this is the proper plural) which highlight the problem. The details within the chapter, of course, present the solution, or at least the basic parameters of a solution.\n is called the operating system ( OS ), as it is in charge of making sure the system operates correctly and efficiently in an easy-to-use manner."
                        ],
                        "passage_scores": [
                            0.9716930985450745,
                            0.9375210404396057,
                            0.6745027303695679
                        ],
                        "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                    },
                    {
                        "lu_id": "kaAKiOncIfjgwM9Uzm9y",
                        "lu_score": 0.25,
                        "passages": [
                            "The operating system must also run non-stop; when it fails, all appli- cations running on the system fail as well. Because of this dependence, operating systems often strive to provide a high degree of reliability . As operating systems grow evermore complex (sometimes containing mil- lions of lines of code), building a reliable operating system is quite a chal- lenge — and indeed, much of the on-going research in the field (including some of our own work [BS+09, SS+10]) focuses on this exact problem."
                        ],
                        "passage_scores": [
                            0.9361236691474915
                        ],
                        "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                    },
                    {
                        "lu_id": "NctXsNCc6YCqmX9Tw5Xc",
                        "lu_score": 0.3333333333333333,
                        "passages": [
                            "I O S 17 Thus, we have an introduction to the OS. Today's operating systems make systems relatively easy to use, and virtually all operating systems you use today have been influenced by the developments we will discuss throughout the book."
                        ],
                        "passage_scores": [
                            0.8515712022781372
                        ],
                        "learning_resource_id": "W1HAobJsOGp36R5u9qRO"
                    }
                ]
            }
        ]
    }
  }



