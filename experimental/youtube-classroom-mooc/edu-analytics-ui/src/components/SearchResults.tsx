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


import TutorCard from './TutorCard';

interface SearchResults {
    searchResults: Array<Object>,
    onSearchResultClick: Function,
    selectedVideoList: Array<Int16Array>
}

const SearchResults: React.FunctionComponent<SearchResults> = ({ searchResults, onSearchResultClick, selectedVideoList }) => {

    return (
        <div className='grid grid-cols-3 gap-4'>
            {searchResults.map((result, index) => {
                console.log('youtube list', result);
                return (
                    <TutorCard
                        thumbNail={result.thumbnails?.medium?.url}
                        caption={result?.title}
                        onCardClick={onSearchResultClick}
                        keys={index}
                        avatar={result.thumbnails?.default?.url}
                        channelTitle={result?.channelTitle}
                        selectedVideoList={selectedVideoList}
                    />
                )
            })}
        </div>

    )
}

export default SearchResults;