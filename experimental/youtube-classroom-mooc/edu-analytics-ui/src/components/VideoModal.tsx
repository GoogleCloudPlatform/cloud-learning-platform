import React from 'react';
import { Modal, Box } from '@material-ui/core'
import YoutubePlayer from './YoutubePlayer';

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 700,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

interface VideoModal {
    videoId: string,
    open: boolean,
    onClose: EventListener,
    onVideoClosed: Function,
    playbackStatus: Object,

}


const VideoModal: React.FunctionComponent<VideoModal> = ({ videoId, open, onClose, onVideoClosed, playbackStatus }) => {

    const [isVideoStopped, setIsVideoStopped] = React.useState(false);
    const [videoDuration, setVideoDuration] = React.useState(0);
    const [videoStatus, setVideoStatus] = React.useState('');

    const onVideoStatusChange = (videoStatus: string, videoDuration) => {
        if (videoStatus === 'Paused' || videoStatus === 'End') {
            setIsVideoStopped(true);
            setVideoStatus(videoStatus);
            setVideoDuration(videoDuration);
        }
        else {
            setIsVideoStopped(false);
        }
    }

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"

        >

            <Box sx={style}>
                {isVideoStopped ? <div className='float-right cursor-pointer p-1 border-2 border-black' onClick={() => onVideoClosed(videoStatus, videoDuration)}>X</div> : <></>}
                <YoutubePlayer videoId={videoId} setVideoStatus={onVideoStatusChange} playbackStatus={playbackStatus}/>
                <div><span style={{ color: 'red' }}>Note:Please pause/complete the video to close the modal</span></div>
            </Box>
        </Modal>
    )

}

export default VideoModal;
