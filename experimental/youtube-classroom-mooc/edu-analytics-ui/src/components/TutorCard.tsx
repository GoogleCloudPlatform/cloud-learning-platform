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