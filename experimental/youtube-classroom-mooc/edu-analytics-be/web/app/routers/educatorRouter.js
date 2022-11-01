/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

const router = require('express').Router();

const EducatorController =require('../controller/educatorController');
const StudentController =require('../controller/studentController');

/**
 * @swagger
 * /test:
 *  get:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: test api
 *      description: test swagger api
 *      responses:
 *          200:
 *             description: "Successfull operation"
 */
router.get('/test',(req,res)=>{
    res.send("Hello world");
});

/**
 * @swagger
 * definitions:
 *    Youtube:
 *        type: "object"
 *        properties:
 *              videoId:
 *                  type: "string"
 *                  example: "https"
 *              title:
 *                  type: "string"
 *                  example: "https"
 *              description:
 *                  type: "string"
 *                  example: "https"
 *              channelTitle:
 *                  type: "string"
 *                  example: "https"
 *              thumbnail:
 *                  type: "string"
 *                  example: "{thubmbnail objects}"
 *              duration:
 *                  type: "string"
 *                  example: "12"
 */

/**
 * @swagger
 * /playlist:
 *  post:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Create new playlist
 *      description: API to Create new playlist
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      title:
 *                        type: "string"
 *                        example: "playlist1"
 *                      educatorId:
 *                         type: "integer"
 *                         example: "1"
 *                      playlists:
 *                          type: "array"
 *                          items:
 *                              $ref: '#definitions/Youtube'
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
router.post('/playlist', EducatorController.createPlaylist);

/**
 * @swagger
 * /playlist/{playlistId}/videos:
 *  post:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Add videos to existing playlist
 *      description: API to Add videos to existing playlist
 *      parameters:
 *          - in: path
 *            name: playlistId
 *            required: true
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      playlists:
 *                          type: "array"
 *                          items:
 *                              $ref: '#definitions/Youtube'
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
 router.post('/playlist/:playlistId/videos', EducatorController.addVideosToPlaylist);

/**
 * @swagger
 * /playlist:
 *  get:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: List playlist
 *      description: API to list all playlist
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
 router.get('/playlist', EducatorController.getAllPlaylist);

 /**
 * @swagger
 * /playlist/{playlistId}/videos:
 *  get:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: List playlist videos
 *      description: API to list playlist videos
 *      parameters:
 *              - in: path
 *                name: playlistId
 *                required: true
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
  router.get('/playlist/:playlistId/videos', EducatorController.getPlaylist);


/**
 * @swagger
 * /educator:
 *  post:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Create new educator
 *      description: Creating a new educator
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      email:
 *                          type: "string"
 *                          example: "edu@google.com"
 *                      firstName:
 *                          type: "string"
 *                          example: "John"
 *                      lastName:
 *                          type: "string"
 *                          example: "C"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */ 
router.post('/educator',EducatorController.createEducator);


/**
 * @swagger
 * /educator/{email}:
 *  get:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Get educator details by email
 *      description: Get educator details by email
 *      parameters:
 *              - in: path
 *                name: email
 *                required: true
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
 router.get('/educator/:email', EducatorController.getEducatorByEmail);



/**
 * @swagger
 * /assignTask:
 *  post:
 *      tags:
 *          - Educator
 *      summary: Create and Assign new task to a student or class
 *      description: Creating a new task
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      taskName:
 *                          type: "string"
 *                          example: "Story writing"
 *                      playlistId:
 *                          type: "integer"
 *                          example: "1"
 *                      courseId:
 *                          type: "string"
 *                          example: "abcd10"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */
router.post('/assignTask',EducatorController.assignTask);


/**
 * @swagger
 * /taskStatus:
 *  post:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Add task status of a student
 *      description: Add task status to a student
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      taskId:
 *                          type: "integer"
 *                          example: "1"
 *                      studentId:
 *                          type: "integer"
 *                          example: "16"
 *                      status:
 *                          type: "string"
 *                          enum:
 *                              - Not started
 *                              - Inprogress
 *                              - Completed
 *      responses:
 *             201:
 *                description: "Successfully created"
 */
router.post('/taskStatus',EducatorController.taskStatus);

/**
 * @swagger
 * /taskStatus/{taskId}/student/{studentId}/{status}:
 *  put:
 *      tags:
 *          - Educator
 *      security: []
 *      summary: Update task status
 *      description: Update task status to a student
 *      parameters:
 *              - in: path
 *                name: taskId
 *                required: true
 *              - in: path
 *                name: studentId
 *                required: true
 *              - in: path
 *                name: status
 *                required: true
 *                enum:
 *                    - NotStarted
 *                    - Inprogress
 *                    - Completed
 *      responses:
 *             200:
 *                description: "Updated Successfully"
 */
router.put('/taskStatus/:taskId/student/:studentId/:status',EducatorController.updateTaskStatus);


/**
 * @swagger
 * /courses:
 *  get:
 *      tags:
 *          - Educator
 *      summary: fetch courses
 *      description: fetch courses
 *      responses:
 *             200:
 *                description: "Updated Successfully"
 */
 router.get('/courses',EducatorController.pullCourseDataFromClassRoomApi);


 /**
 * @swagger
 * /student/courses:
 *  get:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Get student courses
 *      description: Get student courses
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
 router.get('/student/courses',StudentController.getStudentCourseList);


 /**
 * @swagger
 * /invitations:
 *  post:
 *      tags:
 *          - Educator
 *      summary: Invite student to course
 *      description: Invite student to course
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      courseId:
 *                          type: "string"
 *                          example: "12345re"
 *                      studentId:
 *                          type: "string"
 *                          example: "103670714513850984378"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */
router.post('/invitations',EducatorController.invitation);

/**
 * @swagger
 * /enrollStudent:
 *  post:
 *      tags:
 *          - Educator
 *      summary: Enroll student to course
 *      description: Enroll student to course
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      courseId:
 *                          type: "string"
 *                          example: "520709412969"
 *                      studentId:
 *                          type: "string"
 *                          example: "103670714513850984378"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */
 router.post('/enrollStudent',EducatorController.enrollStudentToCourse);


 /**
 * @swagger
 * /playlist/{id}:
 *  delete:
 *      tags:
 *          - Educator
 *      summary: Delete playlist by playlist id
 *      description: Delete playlist by playlist id
 *      parameters:
 *              - in: path
 *                name: id
 *                required: true
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
  router.delete('/playlist/:id', EducatorController.deletePlaylistId);

module.exports = router;