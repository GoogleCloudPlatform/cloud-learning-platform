/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from 'react';
import { Grid } from '@material-ui/core';
import axios from 'axios';
interface AddCourse {
    selectOptions: Array<string>,
    videoListSelected:Int16Array
}

const AddCourse: React.FunctionComponent<AddCourse> = ({ selectOptions,videoListSelected }) => {

    const [textContent, setTextContent] = React.useState('');
    const [coureseId,setCourseId] = React.useState('Data Analytics')

    const classRoomMap = {
        'Data Analytics': {
            id: 1,

        },
        'Machine Learning': {
            id: 2,
            
        }
    }

    const onTextChange = (event) => {
        setTextContent(event.target.value);
    }

    const onCourseChange = (event)=>{
        setCourseId(event.target.value);
    }

    const createStudentTask = () => {
        const payLoad = {
            "taskName": textContent,
            "playlistId": videoListSelected,
            "courseId": classRoomMap[coureseId].id,
            "classRoomTaskId": Math.floor(Math.random() * 100)
        }

        axios.post('https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/assignTask',payLoad)
        .then((res)=>{
            alert('Course Assigned');
            setTextContent('');
        })
        .catch((err)=>{
            alert('Failed to Assign')
        })
    }

    return (
        <div className='grid grid-row-3 mt-5 gap-4'>
            <div>
                <select className="select select-bordered w-full max-w-xs" onChange={onCourseChange}>
                    <option selected>Data Analytics</option>
                    <option>Machine Learning</option>
                </select>
            </div>

            <div><textarea className="textarea textarea-bordered" placeholder="Description" onChange={onTextChange}></textarea></div>
            <div><button className="btn" onClick={createStudentTask}>Create Task</button></div>

        </div>
    )
}

export default AddCourse;