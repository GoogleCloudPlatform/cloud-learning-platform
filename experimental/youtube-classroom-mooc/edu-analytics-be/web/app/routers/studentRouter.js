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

const StudentController =require('../controller/studentController');


/**
 * @swagger
 * /student:
 *  post:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Create new student
 *      description: Creating a new student
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      email:
 *                          type: "string"
 *                          example: "std@google.com"
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
 router.post('/student',StudentController.createStudent);

 /**
 * @swagger
 * /student/{studentId}/tasks/{status}:
 *  get:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Fetch tasks for a student
 *      description: Fetch tasks for student
 *      parameters:
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
 *                description: "Success"
 */
router.get('/student/:studentId/tasks/:status',StudentController.getStudentTasks);

/**
 * @swagger
 * /student/{studentId}/analytics:
 *  get:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Student analytics by student id
 *      description: Student anayltics
 *      parameters:
 *              - in: path
 *                name: studentId
 *                required: true
 *      responses:
 *             200:
 *                description: "Success"
 */
 router.get('/student/:studentId/:analytics',StudentController.fetchStudentAnalytics);


 /**
 * @swagger
 * /student/analytics:
 *  post:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Create student analytics
 *      description: Creating student analytics
 *      parameters:
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      videoId:
 *                          type: "string"
 *                          example: "123"
 *                      playlistId:
 *                          type: "integer"
 *                          example: "123"
 *                      studentId:
 *                          type: "integer"
 *                          example: "124"
 *                      taskStatus:
 *                          type: "string"
 *                          example: "Inprogress"
 *                      videoStatus:
 *                          type: "string"
 *                          example: "124"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */ 
  router.post('/student/analytics',StudentController.createStudentAnalytics);



  /**
 * @swagger
 * /studentAnalytics/{id}:
 *  put:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Update student analytics
 *      description: Update student analytics
 *      parameters:
 *          - in: path
 *            name: id
 *            required: true
 *          - name: body
 *            in: body
 *            schema:
 *               type: "object"
 *               properties:
 *                      videoStatus:
 *                          type: "string"
 *                          example: "Inprogress"
 *                          enum:
 *                              - NotStarted
 *                              - Inprogress
 *                              - Completed
 *                      progress:
 *                          type: "string"
 *                          example: "1:23"
 *      responses:
 *             201:
 *                description: "Successfully created"
 */ 
   router.put('/studentAnalytics/:id',StudentController.updateStudentAnalytics);


   /**
 * @swagger
 * /student/{studentId}/classRoomTask/{classRoomTaskId}/analytics:
 *  get:
 *      tags:
 *          - Student
 *      summary: Student analytics by student id and classromm task id
 *      description: Student anayltics
 *      parameters:
 *              - in: path
 *                name: studentId
 *                required: true
 *              - in: path
 *                name: classRoomTaskId
 *                required: true
 *      responses:
 *             200:
 *                description: "Success"
 */
 router.get('/student/:studentId/classRoomTask/:classRoomTaskId/:analytics',StudentController.fetchStudentAnalyticsByClassroomTaskId);


 /**
 * @swagger
 * /student/{email}:
 *  get:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Get student details by email
 *      description: Get student details by email
 *      parameters:
 *              - in: path
 *                name: email
 *                required: true
 *      responses:
 *          201:
 *              description: "Successfull operation"
 */
  router.get('/student/:email', StudentController.getStudentByEmail);



   /**
 * @swagger
 * /user/create/{userType}:
 *  post:
 *      tags:
 *          - User
 *      summary: Create/add google user into edu analytics
 *      description: Create/add google user into edu analytics
 *      parameters:
 *              - in: path
 *                name: userType
 *                required: true
 *                enum:
 *                    - student
 *                    - educator
 *      responses:
 *             200:
 *                description: "Success"
 */
router.post('/user/create/:userType',StudentController.addGoogleUser);

/**
 * @swagger
 * /student/{studentId}/course/{courseId}/analytics:
 *  get:
 *      tags:
 *          - Student
 *      security: []
 *      summary: Student analytics by student id and classromm task id
 *      description: Student anayltics
 *      parameters:
 *              - in: path
 *                name: studentId
 *                required: true
 *              - in: path
 *                name: courseId
 *                required: true
 *      responses:
 *             200:
 *                description: "Success"
 */
 router.get('/student/:studentId/course/:courseId/:analytics',StudentController.fetchStudentAnalyticsByCourseId);



module.exports = router;