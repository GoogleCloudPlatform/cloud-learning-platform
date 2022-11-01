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
import YouTube, { YouTubeProps } from 'react-youtube';

interface YouTubePlayer {
    videoId: string
    setVideoStatus: Function,
    playbackStatus: Object
}

const YouTubePlayer: React.FunctionComponent<YouTubePlayer> = ({
    videoId, setVideoStatus, playbackStatus
}) => {
    const onPlayerReady: YouTubeProps['onReady'] = (event) => {
        if (playbackStatus.status === 'In Progress' && playbackStatus?.duration !== undefined) {
            event.target.pauseVideo();
            event.target.seekTo(Math.floor(parseFloat(playbackStatus?.duration)));
            event.target.playVideo();
            //event.target.playVideoAt(parseFloat(playbackStatus?.duration))
        }
        else {
            event.target.playVideo();
        }


    }
    const onVideoPaused: YouTubeProps['onPause'] = (event) => {
        setVideoStatus('Paused', event.target.getCurrentTime())
    }
    const onVideoEnd: YouTubeProps['onEnd'] = (event) => {
        setVideoStatus('End')
    }
    const onVideoPlay: YouTubeProps['onPlay'] = (event) => {
        setVideoStatus('Play')
    }
    const opts: YouTubeProps['opts'] = {
        height: '400',
        width: '640',
        playerVars: {
            autoplay: 1,
        }
    }
    return (
        <YouTube
            videoId={videoId}
            opts={opts}
            onReady={onPlayerReady}
            onPause={onVideoPaused}
            onEnd={onVideoEnd}
            onPlay={onVideoPlay} />
    )
}

export default YouTubePlayer;