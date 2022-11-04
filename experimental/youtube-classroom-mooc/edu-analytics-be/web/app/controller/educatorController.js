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

const EducatorEntity = require('../entity/educatorEntity');

class EducatorController {

    static async createPlaylist(req, res, next) {
        try {
            const data = await EducatorEntity.createPlaylist(req.body);
            if (data.length > 0) {
                res.status(201).send(data[0]);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }

    }

    static async getAllPlaylist(req, res, next) {
        try {
            const data = await EducatorEntity.getAllPlaylist();
            if (data.length > 0) {
                res.status(200).send(data);
            } else {
                res.status(404).send(data);
            }

        } catch (err) {
            next(err);
        }

    }

    static async getPlaylist(req, res, next) {
        try {
            const data = await EducatorEntity.getPlaylist(req.params.playlistId);
            if (data.length > 0) {
                res.status(200).send(data);
            } else {
                res.status(404).send(data);
            }

        } catch (err) {
            next(err);
        }

    }

    static async createEducator(req, res, next) {
        try {
            const data = await EducatorEntity.createEducator(req.body);
            if (data.affectedRows && data.affectedRows > 0) {
                res.status(201).send(data);
            } else if (data.length > 0) {
                res.status(200).send(data[0]);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }

    }

    static async assignTask(req, res, next) {
        try {
            const token = req.get('Authorization');
            const data = await EducatorEntity.assignTask(token, req.body);
            res.status(data.status).send(data.msg);
        } catch (err) {
            next(err);
        }

    }

    static async taskStatus(req, res, next) {
        try {
            const data = await EducatorEntity.taskStatus(req.body);
            if (data.affectedRows && data.affectedRows > 0) {
                res.status(201).send(data);
            } else {
                res.status(400).send(data.reason);
            }

        } catch (err) {
            next(err);
        }
    }

    static async updateTaskStatus(req, res, next) {
        try {
            const data = await EducatorEntity.updateTaskStatus(req.params.taskId, req.params.studentId, req.params.status);
            if (data.affectedRows && data.affectedRows > 0) {
                res.status(201).send(data);
            } else {
                res.status(400).send(data.reason);
            }

        } catch (err) {
            next(err);
        }
    }

    static async addVideosToPlaylist(req, res, next) {
        try {
            const data = await EducatorEntity.addVideosToPlaylist(req.params.playlistId, req.body);
            if (data.length > 0) {
                res.status(200).send(data);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }

    }


    static async getEducatorByEmail(req, res, next) {
        try {
            const data = await EducatorEntity.getEducatorByEmail(req.params.email);
            if (data.length > 0) {
                res.status(200).send(data[0]);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }

    }

    static async pullCourseDataFromClassRoomApi(req, res, next) {
        try {
            const token = req.get('Authorization');
            const data = await EducatorEntity.pullCourseDataFromClassRoomApi(token);
            res.status(200).send(data);
        } catch (err) {
            next(err);
        }

    }


    static async invitation(req, res, next) {
        try {
            const token = req.get('Authorization');
            const data = await EducatorEntity.invitation(token, req.body);
            if (data) {
                res.status(201).send(data);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }
    }

    static async enrollStudentToCourse(req, res, next) {
        try {
            const token = req.get('Authorization');
            const data = await EducatorEntity.enrollStudentToCourse(token, req.body);
            if (data) {
                res.status(201).send(data);
            } else {
                res.status(400).send(data);
            }

        } catch (err) {
            next(err);
        }
    }

    static async deletePlaylistId(req, res, next) {
        try {
            const token = req.get('Authorization');
            const data = await EducatorEntity.deletePlaylistId(req.params.id, token);
            res.status(data.status).send(data);
        } catch (err) {
            next(err);
        }
    }
}

module.exports = EducatorController;