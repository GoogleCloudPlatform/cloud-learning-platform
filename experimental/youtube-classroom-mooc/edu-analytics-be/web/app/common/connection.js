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

const queries = require('./queries');
const mysql = require('mysql');

const ensureSchemas = () => {
    connection.query(queries.CREATE_TABLES, (err) => {
        if (err) {
            console.log("Failed to create tables :" + err);
        } else {
            console.log('Schema created')
        }
    })
}

let connection;
if (process.env.NODE_ENV === 'production') {
    try {
        connection = mysql.createPool({
            socketPath: process.env.INSTANCE_UNIX_SOCKET,
            user: process.env.DB_USER,
            password: process.env.DB_PASS,
            database: process.env.DB_NAME,
            multipleStatements: true
        })
    } catch (error) {
        console.log('Connection error:' + error)
    }
    ensureSchemas();

} else {
    connection = mysql.createPool({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        database: process.env.DB_NAME,
        multipleStatements: true
    });
    ensureSchemas();
}




/* connection.connect((err) => {
    if (err) {
        console.log(`Failed to connect to db ${err}`)
    } else {
        console.log('Database connected');
        connection.query(queries.CREATE_TABLES, (err) => {
            if (err) {
                console.log("Failed to create tables :" + err.message);
            }
        })
    }
}); */

module.exports = connection;