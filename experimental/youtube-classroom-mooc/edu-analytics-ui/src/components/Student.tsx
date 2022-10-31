import React from 'react';
import { Tab, Tabs, Grid, Divider, Typography, duration } from '@material-ui/core';
import axios from 'axios';

import StudentCard from './StudentCard';
import VideoModal from './VideoModal';


interface Student {

}

const Student: React.FunctionComponent<Student> = ({

}) => {
    const [tabValue, setTabValue] = React.useState('Assigned');
    const [assigmentList, setAssignmentList] = React.useState([]);
    const [displayList, setDisplayList] = React.useState([]);
    const [modalStatus, setModalStatus] = React.useState(false);
    const [videoId, setVideoId] = React.useState('');
    const [playbackStatus, setPlayBackStatus] = React.useState({});

    React.useEffect(() => {
        //Call the web api and assign the result to assigmentList

        axios.get(`https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/student/1/analytics`)
            .then((res) => {
                setAssignmentList(res.data);
                setDisplayList(res.data.filter(x => x.videoStatus === 'NotStarted'))
            })
    }, [])

    React.useEffect(() => {
        if (tabValue === 'Assigned') {
            setDisplayList(assigmentList.filter(x => x.videoStatus === 'NotStarted'))
        }
        else if (tabValue === 'In Progress') {
            setDisplayList(assigmentList.filter(x => x.videoStatus === 'Inprogress'))
        }
        else {
            setDisplayList(assigmentList.filter(x => x.videoStatus === 'Completed'))
        }
    }, [tabValue])

    const onCardClick = (index) => {
        const selectedVideo = displayList[index];
        const link = selectedVideo?.video?.videoId;
        const videoStatus = {
            status: tabValue,
            duration: displayList[index]?.videoProgress
        }
        setVideoId(link);
        setPlayBackStatus(videoStatus);
        setModalStatus(true);


    }
    const handleChange = (event, newValue) => {
        setTabValue(newValue);
    };

    const onModalClose = (event: object, reason: string) => {
        if (reason !== 'backdropClick') {
            setModalStatus(false);
            setVideoId('');
        }
    }

    const onVideoClosed = (status, duration = 0) => {

        const video = displayList.filter(x => x.video?.videoId === videoId)[0];

        const videoStatus = status === 'Paused' ? 'Inprogress' : status === 'End' ? 'Completed' : 'Inprogress'
        const payLoad = {

            "videoStatus": videoStatus,
            "progress": duration.toString()

        }

        axios.put(`https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/studentAnalytics/${video?.id}`, payLoad)
            .then((res) => {
                console.log(res);
                axios.get(`https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/student/1/analytics`)
                    .then((res) => {
                        setAssignmentList(res.data);
                        setDisplayList(res.data.filter(x => x.videoStatus === 'NotStarted'))
                        setTabValue('Assigned');
                    })
            })
            .catch((err) => {
                console.error(err);
            })
            .finally(() => {
                setModalStatus(false);
            })


    }
    const displayAllAssigments = () => {
        return (<div className='grid grid-cols-2 gap-4'>
            {displayList.map((assigment, index) => {
                return (
                    <StudentCard
                        thumbNail={assigment.video?.thumbnail}
                        caption={assigment.video?.channelTitle}
                        description={assigment.video?.title}
                        timeStamp={assigment.video?.duration}
                        onCardClick={onCardClick}
                        keys={index}
                    />
                )
            })
            }
        </div >)
    };

    const onSelectChange = (event, value) => {
        console.log(event.target.value)
    }
    return (
        <>
            <Grid>
                <Grid container item
                    direction="row"
                >
                    <Grid item lg={9} md={9}>
                        <Tabs
                            value={tabValue}
                            onChange={handleChange}
                            textColor="secondary"
                            indicatorColor="secondary"
                            aria-label="secondary tabs example"
                        >
                            <Tab value="Assigned" label="Assigned" />
                            <Tab value="In Progress" label="In Progress" />
                            <Tab value="Completed" label="Completed" />
                        </Tabs>
                    </Grid>
                    <Grid item lg={3} md={3}>
                        <select className="select select-ghost w-full max-w-xs" onChange={onSelectChange}>
                            <option >All</option>
                            <option selected>Videos</option>
                            <option>Documents</option>
                            <option>Sheets</option>
                            <option>Others</option>
                        </select>

                    </Grid>
                </Grid>
                <Divider></Divider>
                <Grid container direction='row' item>
                    <Grid item lg={12} sm={12} md={12}>
                        <Typography variant='h6' >
                            {tabValue === 'Assigned' ? 'Not Started' : tabValue}
                        </Typography>
                    </Grid>
                    <Grid item container lg={12} sm={12} md={12}>
                        {assigmentList.length === 0 ? <p>There are no assigments in this section.</p> : displayAllAssigments()}
                    </Grid>

                </Grid>
            </Grid>

            <VideoModal open={modalStatus} videoId={videoId} onClose={onModalClose} onVideoClosed={onVideoClosed} playbackStatus={playbackStatus} />
        </>
    )
}

export default Student;