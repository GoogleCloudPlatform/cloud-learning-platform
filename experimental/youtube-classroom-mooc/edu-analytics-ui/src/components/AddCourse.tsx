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