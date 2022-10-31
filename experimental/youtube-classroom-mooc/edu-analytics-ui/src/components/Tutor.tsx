import React, { useEffect } from "react";
import { Divider, Grid, Tab, Tabs } from "@material-ui/core";
import * as youtubeSearch from "youtube-search";
import axios from 'axios';


import SearchResults from './SearchResults';
import AddCourse from './AddCourse';
import SelectPlaylist from './SelectPlayList';

interface Tutor {

}

const Tutor: React.FunctionComponent<Tutor> = ({

}) => {

    const inputRef = React.useRef(null);
    const [searchResult, setSearchResult] = React.useState([]);
    const [selectedVideoList, setSelectedVideoList] = React.useState([]);
    const [selectedPlayList, setSelectedPlaylist] = React.useState([]);
    const [tabValue, setTabValue] = React.useState('Tasks');
    const [playListName, setPlayListName] = React.useState('');
    const [playListSelected,setPlayListSelected] = React.useState(null);
    const [videolistID,setVideoListID] = React.useState(0);

    const opts: youtubeSearch.YouTubeSearchOptions = {
        maxResults: 6,
        key: "AIzaSyDDVPLxast_MpLE87ekpafXNiM8sHeIQGc"
    };

    React.useEffect(() => {
        getSelectPlayList();
    }, [])

    const getSelectPlayList = () => {
        axios.get('https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/playlist')
            .then((res) => {

                setSelectedPlaylist(res?.data)
            })
            .catch((err) => {
                setSelectedPlaylist([]);
            })
    }

    const onSearch = () => {
        setSelectedVideoList([]);
        youtubeSearch(inputRef?.current?.value, opts, (err, results) => {
            if (err) {
                setSearchResult([]);
            }
            else {
                setSearchResult(results);
            }
        });
    }

    const onSearchResultClick = (index) => {
        const currentSelectedList = [...selectedVideoList];

        const videoIndex = currentSelectedList.indexOf(index);

        if (videoIndex === -1) {
            currentSelectedList.push(index)
        }
        else {
            currentSelectedList.splice(videoIndex, 1);
        }
        setSelectedVideoList(currentSelectedList);
    }

    const onPlaylistClick = (index)=>{
        setPlayListSelected(index);
        setVideoListID(selectedPlayList[index].playlistId)
    }

    const addVideosToPlayList = () => {

        let payLoad = {};

        payLoad.title = playListName;
        payLoad.educatorId = 1;

        payLoad.playlists = selectedVideoList.map((selectedVideo, index) => {
            return {
                "videoId": searchResult[selectedVideo]?.id,
                "title": searchResult[selectedVideo]?.title,
                "description": searchResult[selectedVideo]?.description,
                "channelTitle": searchResult[selectedVideo]?.channelTitle,
                "thumbnail": searchResult[selectedVideo]?.thumbnails?.medium.url
            }
        })
        axios.post('https://edu-classroom-analytics.uc.r.appspot.com/eduAnalytics/playlist', payLoad)
            .then((resp) => {
                getSelectPlayList();
                setSelectedVideoList([]);
            })
            .catch((err) => {
                console.log(err);
            })

    }

    const handleChange = (event, newValue) => {
        setTabValue(newValue);
    };

    const ontextChange = (event, value) => {
        setPlayListName(event.target.value);
    }

    return (
        <>
            <Grid container item
                direction="row"
                justifyContent="center"
                alignItems="center">
                <Grid item>
                    <Tabs
                        value={tabValue}
                        onChange={handleChange}
                        textColor="secondary"
                        indicatorColor="secondary"
                        aria-label="secondary tabs example"
                    >
                        <Tab value="Tasks" label="Create task" />
                        <Tab value="Analytics" label="Analytics" />

                    </Tabs>
                </Grid>
            </Grid>

            <Divider></Divider>
            {tabValue === 'Tasks' ?
                <div className="grid grid-cols-12 ">
                    <div className="grid col-span-10 ">
                        <div className="grid grid-cols-12 ">
                            <div className="grid col-span-11">
                                <div className="m-5 place-items-center">
                                    <div className="input-group">
                                        <input type="text" placeholder="Search…" className="input input-bordered w-full" ref={inputRef} />
                                        <button className="btn btn-square" onClick={onSearch}>
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                                        </button>
                                    </div>
                                </div>
                                <div className="m-5"><SearchResults searchResults={searchResult} onSearchResultClick={onSearchResultClick} selectedVideoList={selectedVideoList} /></div>
                                {selectedVideoList.length >= 1 ? <div style={{ marginLeft: '35%' }}><input type='text' placeholder="Playlist name" onChange={ontextChange} /><button className="btn w-44 h-6" style={{ marginLeft: '3%' }} onClick={() => addVideosToPlayList()} disabled={playListName === '' || playListName === undefined}>Create PlayList</button></div> : <></>}
                                <SelectPlaylist selectedPlayList={selectedPlayList} onPlaylistClick = {onPlaylistClick} playListSeleted = {playListSelected}/>
                            </div>
                            <Divider orientation="vertical" />

                        </div>
                    </div>

                    <div className="col-span-2">
                        <AddCourse selectOptions={['abc', 'xyz']} videoListSelected={videolistID}/>
                    </div>
                </div> : <div><iframe src="https://googlecloud.looker.com/dashboards-legacy/sa-looker-myid-dev::sa-looker-myid-dev" title="Edu Analytics"></iframe></div>}
        </>
    )
}

export default Tutor;