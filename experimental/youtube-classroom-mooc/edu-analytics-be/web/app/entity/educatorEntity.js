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

const axios = require('axios');


class EducatorEntity {


    static async getUserInfoByToken(token) {
        try {
            const user = await axios({
                method: "get",
                headers: { Authorization: `Bearer ${token}` },
                url: `https://www.googleapis.com/oauth2/v1/userinfo`
            })
            const userData = user.data;
            return userData;
        } catch (error) {
            console.log(error);
            //res.send('Invalid user').status(400);
        }
    }

    static async createPlaylist(body) {
        const sql = `INSERT INTO playlist (title,educatorId) VALUES ('${body.title}',${body.educatorId});`;
        console.log(sql);
        /* dbConnection.query(sql, function (err, result, fields) {
            return result;
        });*/
        const data = await query(sql);
        const lastRowId = await query(`SELECT * FROM playlist where playlistId=${data.insertId};`);
        console.log('last row id' + JSON.stringify(lastRowId));
        body.playlists.forEach(async (video) => {
            /*const insertQuery = `INSERT INTO video (videoId,playlistId,title,description,channelTitle,thumbnail,youtubeLink,duration) VALUES ('${video.videoId}',${lastRowId[0].playlistId},'${video.title}','${video.description}','${video.channelTitle}','${video.thumbnail}','${video.youtubeLink ? video.youtubeLink : null}','${video.duration}');`;
            dbConnection.query(insertQuery, function (err) {
                if (err) console.log('Insert video table:' + err)
            });*/

            var sql = "INSERT INTO video SET ?";
            // Connection attained as listed above.
            dbConnection.query(sql, {
                videoId: video.videoId, playlistId: (lastRowId[0].playlistId), title: video.title,
                description: video.description, channelTitle: video.channelTitle, thumbnail: video.thumbnail, youtubeLink: video.youtubeLink ? video.youtubeLink : null, duration: video.duration
            }, function (err) {
                // check result if err is undefined.
                if (err) {
                    console.log('Insert video error:', err);
                }
            });

        })


        return lastRowId;
    }

    static async getAllVideos(playlistId) {
        dbConnection.query(`SELECT * FROM video where playlistId=${playlistId};`, function (err, result) {
            return result;
        });
    }

    static async getAllPlaylist() {
        const data = await query('SELECT * FROM playlist;');
        const respArray = [];
        for (let i = 0; i < data.length; i++) {
            const response = {
                playlistId: data[i].playlistId,
                title: data[i].title,
                videos: Object.values(JSON.parse(JSON.stringify(await this.getPlaylist(data[i].playlistId)))),
                count: Object.values(JSON.parse(JSON.stringify(await this.getPlaylist(data[i].playlistId)))).length
            }
            respArray.push(response);
        }


        return respArray;
    }

    static async getPlaylist(playlistId) {
        const data = await query(`SELECT * FROM video where playlistId=${playlistId};`);
        return data;
    }

    static async createEducator(body) {
        const sql = `INSERT INTO educators (email,firstName,lastName) VALUES ('${body.email}','${body.firstName}','${body.lastName}');`;
        console.log(sql);
        try {
            const data = await query(sql);
            return data;
        } catch (err) {
            if (err.code === 'ER_DUP_ENTRY') {
                return await query(`SELECT * FROM educators where email='${body.email}';`);
            }
            return err;
        }

    }

    static async assignTask(token, body) {
        const tasks = Object.values(JSON.parse(JSON.stringify(await query(`SELECT * FROM tasks where playlistId =${body.playlistId} AND courseId =${body.courseId} ;`))));
        if (tasks.length > 0) {
            return {
                status: 400,
                msg: 'Selected playlist already assigned to the selected course'
            }
        }

        try {
            const video = Object.values(JSON.parse(JSON.stringify(await query(`SELECT * FROM video where playlistId=${body.playlistId} LIMIT 1;`))));
            const result = await axios({
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
                url: `https://classroom.googleapis.com/v1/courses/${body.courseId}/courseWork`,
                data: {
                    assigneeMode: "ALL_STUDENTS",
                    courseId: body.courseId,
                    title: body.taskName,
                    maxPoints: 100,
                    workType: "ASSIGNMENT",
                    state: "PUBLISHED",
                    materials: [
                        {
                            link: {
                                url: `${process.env.STD_PORTAL}?courseId=${body.courseId}&videoId=${video[0].videoId}`
                            }
                        }
                    ]
                }
            })

            console.log(result.data);
            body.classRoomTaskId = result.data.id;
        } catch (error) {
            console.log(error);
            return {
               status: error.response.status,
               msg: error.response.statusText
            }
            //res.send(error).status(400);
        }

        const sql = `INSERT INTO tasks(taskName,playlistId,courseId,studentId,classRoomTaskId) VALUES ('${body.taskName}',${body.playlistId},'${body.courseId}',${body.studentId ? body.studentId : null},'${body.classRoomTaskId}');`;
        console.log(sql);
        const data = await query(sql);

        const lastRowId = await query(`SELECT * FROM tasks where taskId=${data.insertId};`);
        body.taskId = lastRowId[0].taskId;
        const playlistId = body.playlistId;

        if (body.studentId && (body.courseId === null || body.courseId === undefined)) {
            body.status = 'NotStarted';
            await this.taskStatus(body);
        }
        if (body.courseId && (body.studentId === null || body.studentId === undefined)) {
            const students = await query(`SELECT * FROM students;`);
            dbConnection.query(
                'INSERT INTO tasks_status(taskId,studentId,status,courseId,classRoomTaskId) VALUES ?',
                [students.map(item => [body.taskId, item.studentId, 'NotStarted', body.courseId, body.classRoomTaskId])],
                (error) => {
                    console.log(error)
                }
            );

            const videos = Object.values(JSON.parse(JSON.stringify(await this.getPlaylist(playlistId))));
            for (let i = 0; i < videos.length; i++) {
                dbConnection.query(
                    'INSERT INTO student_analytics(videoId,studentId,videoStatus,videoProgress,playlistId,courseId,classRoomTaskId) VALUES ?',
                    [students.map(item => [videos[i].id, item.studentId, 'NotStarted', '00', playlistId, body.courseId, body.classRoomTaskId])],
                    (error) => {
                        console.log(error)
                    }
                );
            }
        }
        return {
            status: 201,
            msg: data
        };
    }

    static async taskStatus(body) {
        if (body.status === 'NotStarted' || body.status === 'Inprogress' || body.status === 'Completed') {
            const sql = `INSERT INTO tasks_status(taskId,studentId,status) VALUES (${body.taskId},${body.studentId},'${body.status}');`;
            console.log(sql);
            const data = await query(sql);
            return data;
        } else {
            return {
                status: 400,
                reason: "Invalid task status"
            }
        }

    }

    static async updateTaskStatus(taskId, studentId, status) {
        if (status === 'NotStarted' || status === 'Inprogress' || status === 'Completed') {
            const sql = `UPDATE tasks_status SET status = '${status}' WHERE taskId = ${taskId} AND studentId = ${studentId};`;
            console.log(sql);
            const data = await query(sql);
            console.log(data);
            return data;
        } else {
            return {
                status: 400,
                reason: "Invalid task status"
            }
        }

    }

    static async addVideosToPlaylist(playlistId, body) {
        body.playlists.forEach((video) => {
            const insertQuery = `INSERT INTO video (videoId,playlistId,title,description,channelTitle,thumbnail,youtubeLink,duration) VALUES ('${video.videoId}',${playlistId},'${video.title}','${video.description}','${video.channelTitle}','${video.thumbnail}','${video.youtubeLink ? video.youtubeLink : null}','${video.duration}');`;
            dbConnection.query(insertQuery, function (err) {
                if (err) console.log('Insert video table:' + err)
            });
        })
        return await this.getPlaylist(playlistId);
    }

    static async getEducatorByEmail(email) {
        const sql = `SELECT * FROM educators where email = '${email}'`;
        console.log('query:', sql);
        const data = await query(sql);
        return data;
    }

    static async pullCourseDataFromClassRoomApi(token) {
        let courses;
        let userData;
        try {
            const result = await axios({
                method: "get",
                headers: { Authorization: `Bearer ${token}` },
                url: 'https://classroom.googleapis.com/v1/courses?courseStates=ACTIVE'
            })
            courses = result.data.courses;
        } catch (error) {
            console.log(error);
            return error.response.status;
            //res.send(error).status(400);
        }


        try {
            const user = await axios({
                method: "get",
                headers: { Authorization: `Bearer ${token}` },
                url: `https://www.googleapis.com/oauth2/v1/userinfo`
            })
            userData = user.data;
        } catch (error) {
            console.log(error);
            //res.send('Invalid user').status(400);
        }

        await query(`DELETE FROM courses WHERE creator='${userData.email}';`);

        await query('INSERT INTO courses(courseId,name,descriptionHeading,ownerId,creator,courseState,creationTime) VALUES ?',
            [courses.map(item => [item.id, item.name, item.descriptionHeading, item.ownerId, userData.email, item.courseState, new Date(item.creationTime).toJSON().slice(0, 19).replace('T', ' ')])]);

        const result = await query(`SELECT * FROM courses WHERE creator='${userData.email}';`);
        return result;
    }

    static async invitation(token, body) {
        try {
            const result = await axios({
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
                url: `https://classroom.googleapis.com/v1/invitations`,
                data: {
                    userId: body.studentId,
                    courseId: body.courseId,
                    role: 'STUDENT'
                }
            })

            console.log(result.data);
            if (result.data) {
                await query(`INSERT INTO invitations(invitationId,userId,courseId,role) VALUES('${result.data.id}','${result.data.userId}','${result.data.courseId}','${result.data.role}');`);
                return result.data
            }
        } catch (error) {
            console.log(error);
            return error.response.status;
            //res.send(error).status(400);
        }
    }

    static async enrollStudentToCourse(token, body) {
        try {
            const result = await axios({
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
                url: `https://classroom.googleapis.com/v1/courses/${body.courseId}/students`,
                data: {
                    userId: body.studentId,
                    courseId: body.courseId,
                }
            })

            return result.data;
        } catch (error) {
            console.log(error);
            return error.response.status;
            //res.send(error).status(400);
        }
    }

    static async deletePlaylistId(playlistId, token) {
        try {
            const tasks = Object.values(JSON.parse(JSON.stringify(await query(`SELECT taskId,courseId,classRoomTaskId FROM tasks where playlistId=${playlistId};`))));
            if (tasks.length > 0) {
                const taskIds = [];
                tasks.forEach((obj) => {
                    taskIds.push(obj.taskId);
                });
                const taskIdString = taskIds.join();
                const delTask_status = `DELETE FROM tasks_status WHERE taskId IN(${taskIdString});`;
                await query(delTask_status);
                await query(`DELETE FROM student_analytics WHERE playlistId=${playlistId};`);
                await query(`DELETE FROM video WHERE playlistId = ${playlistId};`);
                await query(`DELETE FROM tasks WHERE playlistId=${playlistId};`);
                await query(`DELETE FROM playlist WHERE playlistId=${playlistId};`);

                if (token) {
                    console.log('token present');
                    tasks.forEach(async (task) => {
                        try {
                            await axios({
                                method: "DELETE",
                                headers: { Authorization: `Bearer ${token}` },
                                url: `https://classroom.googleapis.com/v1/courses/${task.courseId}/courseWork/${task.classRoomTaskId}`
                            })
                        } catch (error) {
                            console.log(error.response)
                        }

                    })
                }
                return {
                    msg: 'Playlist deleted successfully',
                    status: 200
                };
            } else {
                const playlist = Object.values(JSON.parse(JSON.stringify(await query(`SELECT * FROM playlist where playlistId=${playlistId};`))));
                if (playlist.length > 0) {
                    await query(`DELETE FROM video WHERE playlistId = ${playlistId};`);
                    await query(`DELETE FROM playlist WHERE playlistId=${playlistId};`);
                    return {
                        msg: 'Playlist deleted successfully',
                        status: 200
                    };
                }
                return {
                    msg: 'Invalid playlist id',
                    status: 400
                }
            }
        } catch (error) {
            console.log(error);
            return {
                msg: error,
                status: 500
            }
        }
    }

}
module.exports = EducatorEntity;