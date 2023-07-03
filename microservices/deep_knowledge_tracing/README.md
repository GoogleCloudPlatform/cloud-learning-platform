This folder contains the code base to setup firestore database and run student mastery using DeepKnowledge Tracing algorithm (https://arxiv.org/pdf/1506.05908.pdf)

Steps to run service in local

Install all requirements as mentioned in requirements.txt

Setup and start firebase emulator locally

Update the firestore variables (project-id, port) in main.py with the ones configured for local firestore emulator

Run the following 

pip install requirements.txt

cd src

uvicorn main:app

This starts uvicorn server which runs in port 8000 by default

Open the swagger specs running at localhost:8000/docs/



Creating data (for dev purpose)

Since we haven't created any data, lets first create some data using /create_fake_data endpoint

POST 

/deep_knowledge_tracing/api/v1/fake_data/

Request Body

{
  "num_users": 50,
  "num_lus": 10,
  "item_type": "ctf"
}

Response

{
  "success": true,
  "message": "Successfully created the fake data"
}



Training

Once the data is populated, we can start training DKT model

POST 

/deep_knowledge_tracing/api/v1/train/

{
  "course_id": "sample_course_id"
}

Currently in the firebase emulator, model doesn't consider course_id passed in the request and trains model based on all LUs present in the local firestore

Response

{
  "success": true,
  "message": "Successfully trained dkt model"
}



Inference

POST 

/deep_knowledge_tracing/api/v1/predict/

{
  "user_id": "sample_user_id"
}

Response

{
  "success": true,
  "message": "Successfully generated predictions from dkt model",
  "data": {
    "sample_lu_id": 0.91
  }
}
