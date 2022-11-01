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




interface StudentCard {
  thumbNail: string,
  caption: string,
  description: string,
  timeStamp: string,
  onCardClick: Function,
  keys: React.Key
}

const StudentCard: React.FunctionComponent<StudentCard> = ({ thumbNail, caption, description, timeStamp, onCardClick, keys }) => {
  return (
    <div className="card card-side bg-base-100 shadow-xl" onClick={() =>onCardClick(keys)}>
      <figure><img className = 'w-40 h-28' src={thumbNail} /></figure>
      <div className="card-body">
        <h2 className="card-title">{caption}</h2>
        <p>{description}</p>
        {/* <p>{timeStamp}</p> */}
      </div>
    </div>
  )
}

export default StudentCard;