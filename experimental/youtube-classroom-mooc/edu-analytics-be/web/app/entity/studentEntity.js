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

const dbConnection = require('../common/connection');
const util = require('util');
const query = util.promisify(dbConnection.query).bind(dbConnection);
const EducatorEntity = require('./educatorEntity');

class StudentEntity {
    static async createStudent(body) {
        const sql = `INSERT INTO students (email,firstName,lastName) VALUES ('${body.email}','${body.firstName}','${body.lastName}');`;
        console.log(sql);
        try {
            const data = await query(sql);
            return data;
        } catch (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                return await query(`SELECT * FROM students where email='${body.email}';`);
            }
            return err;
        }

    }

    static async addGoogleUser(token, userType) {
        const user = await EducatorEntity.getUserInfoByToken(token);

        if (userType === 'student') {
            const sql = `INSERT INTO students (email,firstName,lastName,stdId) VALUES ('${user.email}','${user.name}','${user.family_name}','${user.id}');`;
            console.log(sql);
            try {
                await query(sql);
                const data = await query(`SELECT * FROM students where email='${user.email}';`);
                return data[0];
            } catch (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return (await query(`SELECT * FROM students where email='${user.email}';`))[0];
                }
                return err;
            }
        } else if (userType === 'educator') {
            const sql = `INSERT INTO educators (email,firstName,lastName,eduId) VALUES ('${user.email}','${user.name}','${user.family_name}','${user.id}');`;
            console.log(sql);
            try {
                await query(sql);
                const data = await query(`SELECT * FROM educators where email='${user.email}';`);
                return data[0];
            } catch (err) {
                if (err.code === 'ER_DUP_ENTRY') {
                    return (await query(`SELECT * FROM educators where email='${user.email}';`))[0];
                }
                return err;
            }
        }

    }

    static async getStudentTasks(studentId, status) {
        const sql = `select A.* from video A where A.playlistId in (select B.playlistId from tasks B where B.taskId in
             (select C.taskId from tasks_status C where studentId=${studentId} and status='${status}'));`;
        const data = await query(sql);
        return data;
    }

    static async getVideo(videoId) {
        const data = await query(`SELECT * FROM video where id=${videoId};`);
        return data;
    }

    static async fetchStudentAnalytics(studentId) {
        const sql = `SELECT * FROM student_analytics where studentId=${studentId};`;
        const data = Object.values(JSON.parse(JSON.stringify(await query(sql))));
        const respArray = [];
        for (let i = 0; i < data.length; i++) {
            const resobject = {
                ...data[i],
                video: Object.values(JSON.parse(JSON.stringify(await this.getVideo(data[i].videoId))))[0],

            }
            respArray.push(resobject);
        }
        return respArray;
    }


    static async fetchStudentAnalyticsByClassroomTaskId(studentId, classRoomTaskId) {
        const sql = `SELECT * FROM student_analytics where studentId = ${studentId} and classRoomTaskId='${classRoomTaskId}';`;
        const data = Object.values(JSON.parse(JSON.stringify(await query(sql))));
        const respArray = [];
        for (let i = 0; i < data.length; i++) {
            const resobject = {
                ...data[i],
                video: Object.values(JSON.parse(JSON.stringify(await this.getVideo(data[i].videoId))))[0],

            }
            respArray.push(resobject);
        }
        return respArray;
    }

    static async createStudentAnalytics(body) {
        const sql = `INSERT INTO student_analytics (videoId,studentId,taskStatus,videoStatus) VALUES ('${body.videoId}',${body.studentId},'${body.taskStatus}','${body.videoStatus}');`;
        console.log(sql);
        try {
            const data = await query(sql);
            return data;
        } catch (err) {
            return err;
        }
    }

    static async updateStudentAnalytics(id, body) {
        const sql = `UPDATE student_analytics SET videoStatus = '${body.videoStatus}', videoProgress = '${body.progress}' WHERE id='${id}';`;
        console.log(sql);
        try {
            const data = await query(sql);
            await this.updateTaskStatus(id);
            return data;
        } catch (err) {
            return err;
        }
    }

    static async updateTaskStatus(id) {
        const sql = `SELECT * FROM student_analytics where id=${id};`;
        const analytics = Object.values(JSON.parse(JSON.stringify(await query(sql))))[0];
        const notStartedCountQuery = `SELECT  count(*) as count FROM student_analytics where studentId = ${analytics.studentId} and classRoomTaskId='${analytics.classRoomTaskId}' and videoStatus = 'NotStarted';`;
        const notStartedCount = Object.values(JSON.parse(JSON.stringify(await query(notStartedCountQuery))))[0];

        const inprogressCountQuery = `SELECT  count(*) as count FROM student_analytics where studentId = ${analytics.studentId} and classRoomTaskId='${analytics.classRoomTaskId}' and videoStatus = 'Inprogress';`;
        const inprogressCount = Object.values(JSON.parse(JSON.stringify(await query(inprogressCountQuery))))[0];

        const completedCountQuery = `SELECT  count(*) as count FROM student_analytics where studentId = ${analytics.studentId} and classRoomTaskId='${analytics.classRoomTaskId}' and videoStatus = 'Completed';`;
        const completedCount = Object.values(JSON.parse(JSON.stringify(await query(completedCountQuery))))[0];

        let status = 'NotStarted';
        let completedDate = null;
        if (notStartedCount.count === 0 && inprogressCount.count === 0 && completedCount.count > 0) {
            status = 'Completed';
            completedDate = new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60 * 1000).toJSON().slice(0, 19).replace('T', ' ');
            const updateTaskStatusSql = `UPDATE tasks_status SET status = '${status}',completedDate='${completedDate}' WHERE classRoomTaskId = '${analytics.classRoomTaskId}' AND studentId = ${analytics.studentId};`;
            console.log('updateTaskStatusSql:', updateTaskStatusSql);
            await query(updateTaskStatusSql);

        } else if (inprogressCount.count > 0 || completedCount.count > 0) {
            status = 'Inprogress';
            const updateTaskStatusSql = `UPDATE tasks_status SET status = '${status}',completedDate=${completedDate} WHERE classRoomTaskId = '${analytics.classRoomTaskId}' AND studentId = ${analytics.studentId};`;
            console.log('updateTaskStatusSql:', updateTaskStatusSql);
            await query(updateTaskStatusSql);
        }


    }


    static async getStudentByEmail(email) {
        const sql = `SELECT * FROM students where email = '${email}'`;
        console.log('query:', sql);
        const data = await query(sql);
        return data;
    }


    static async fetchStudentAnalyticsByCourseId(studentId, courseId) {
        const sql = `SELECT * FROM student_analytics where studentId = ${studentId} and courseId='${courseId}';`;
        const data = Object.values(JSON.parse(JSON.stringify(await query(sql))));
        const respArray = [];
        for (let i = 0; i < data.length; i++) {
            const resobject = {
                ...data[i],
                video: Object.values(JSON.parse(JSON.stringify(await this.getVideo(data[i].videoId))))[0],

            }
            respArray.push(resobject);
        }
        return respArray;
    }

    static async getStudentCourses(){
        return await query('SELECT * FROM courses;');
    }


}
module.exports = StudentEntity;