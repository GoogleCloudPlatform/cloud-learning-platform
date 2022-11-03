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

module.exports = Object.freeze({
    CREATE_TABLES: 'CREATE TABLE if not exists students (studentId int NOT NULL AUTO_INCREMENT,email varchar(255) NOT NULL,firstName varchar(255) NOT NULL,lastName varchar(255) NOT NULL,stdId varchar(255),createdDate DATETIME DEFAULT NOW(),PRIMARY KEY (studentId),UNIQUE (email));'+
                    'CREATE TABLE if not exists educators (educatorId int NOT NULL AUTO_INCREMENT,email varchar(255) NOT NULL,firstName varchar(255) NOT NULL,lastName varchar(255) NOT NULL,eduId varchar(255),createdDate DATETIME DEFAULT NOW(),PRIMARY KEY (educatorId),UNIQUE (email));'+
                    'CREATE TABLE if not exists playlist (playlistId int NOT NULL AUTO_INCREMENT,title varchar(255) NOT NULL,educatorId int,createdDate DATETIME DEFAULT NOW(),PRIMARY KEY (playlistId),FOREIGN KEY (educatorId) REFERENCES educators(educatorId));'+
                    'CREATE TABLE if not exists video (id int NOT NULL AUTO_INCREMENT,videoId varchar(255),playlistId int,title varchar(255),description varchar(2048),channelTitle varchar(255),thumbnail varchar(8000),youtubeLink  varchar(2048),duration varchar(45),PRIMARY KEY (id),FOREIGN KEY (playlistId) REFERENCES playlist(playlistId));'+
                    'CREATE TABLE if not exists tasks (taskId int NOT NULL AUTO_INCREMENT,taskName varchar(255) NOT NULL,playlistId int,courseId varchar(255),classRoomTaskId varchar(255),studentId int,assignedDate DATETIME DEFAULT NOW(),PRIMARY KEY (taskId),FOREIGN KEY (playlistId) REFERENCES playlist(playlistId),FOREIGN KEY (studentId) REFERENCES students(studentId));'+
                    'CREATE TABLE if not exists tasks_status (id int NOT NULL AUTO_INCREMENT,taskId int,studentId int,status varchar(255),courseId varchar(255),classRoomTaskId varchar(255),completedDate DATETIME,PRIMARY KEY (id),FOREIGN KEY (taskId) REFERENCES tasks(taskId),FOREIGN KEY (studentId) REFERENCES students(studentId));'+
                    'CREATE TABLE if not exists student_analytics (id int NOT NULL AUTO_INCREMENT,videoId varchar(45),studentId int,videoStatus varchar(255),videoProgress varchar(255),playlistId int,courseId varchar(255),classRoomTaskId varchar(255),PRIMARY KEY (id),FOREIGN KEY (studentId) REFERENCES students(studentId));'+
                    'CREATE TABLE if not exists courses (id int NOT NULL AUTO_INCREMENT,courseId varchar(255) NOT NULL,name varchar(255) NOT NULL,descriptionHeading varchar(255) NOT NULL,ownerId varchar(255) NOT NULL,creator varchar(255) NOT NULL,courseState varchar(255) NOT NULL,creationTime DATETIME,PRIMARY KEY (id),UNIQUE (courseId));'+
                    'CREATE TABLE if not exists invitations (id int NOT NULL AUTO_INCREMENT,invitationId varchar(255),userId varchar(255),courseId varchar(255),role varchar(255),createdDate DATETIME DEFAULT NOW(),PRIMARY KEY (id));'
})