interface TutorCard {
    thumbNail: string,
    caption: string,
    avatar: string,
    onCardClick: Function,
    keys: React.Key,
    channelTitle: string,
    selectedVideoList: Array<Int16Array>
}

const TutorCard: React.FunctionComponent<TutorCard> = ({ thumbNail, caption, avatar, onCardClick, keys, channelTitle, selectedVideoList }) => {
    const isSelected = () => {
        if (selectedVideoList.includes(parseInt(keys))) {
            return "card card-compact border-2 border-blue-100"
        }
        else {
            return "card card-compact"
        }
    }
    return (
        <div className={isSelected()} onClick={() => onCardClick(keys)}>
            <figure><img src={thumbNail} alt="Thumbnail" /></figure>
            <div>
                {caption}
            </div>
            <div>
                <div className="avatar">
                    <div className="w-6 h-6 rounded-full">
                        <img src={avatar} />
                    </div>
                </div>
                <div>{channelTitle}</div>
            </div>
        </div>
    )
}

export default TutorCard;