



interface SelectPlaylist {
    selectedPlayList: Array<Object>,
    onPlaylistClick:Function,
    playListSeleted:string,
}

const SelectPlaylist: React.FunctionComponent<SelectPlaylist> = ({
    selectedPlayList,
    onPlaylistClick,
    playListSeleted

}) => {
    const isSelected = (index) => {
        if (playListSeleted === index) {
            return "card card-compact bg-base-100 shadow-xl image-full border-blue-100 border-2"
        }
        else {
            return "card card-compact bg-base-100 shadow-xl image-full"
        }
    }
    return (
        <div className="m-5">
            <p>Select Playlist</p>
            <div className='grid grid-cols-3 gap-4 '>
                {selectedPlayList.length === 0 ? <p>No playlist selected</p> : selectedPlayList.map((items, index) => {
                    return (
                        <div onClick={()=>onPlaylistClick(index)}>
                            <div className={isSelected(index)}>
                                <figure><img src={items.videos[0]?.thumbnail} alt="thumbnail" /></figure>
                                <div className="card-body">
                                    <div className="absolute inset-y-0 right-0 bottom-0 w-16 text-center " style={{ backgroundColor: 'rgba(0,0,0,0.51)' }}>
                                        <div style={{ marginTop: '85%', marginLeft: '35%' }}>{items.count}
                                            <svg width="20" height="16" viewBox="0 0 20 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                <path fill-rule="evenodd" clip-rule="evenodd" d="M12 0H0V2H12V0ZM12 4H0V6H12V4ZM0 8H10V10H0V8ZM20 11L13 15.2V6.8L20 11Z" fill="white" />
                                            </svg></div>

                                    </div>

                                </div>
                            </div>
                            <div>{items.title}</div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default SelectPlaylist;