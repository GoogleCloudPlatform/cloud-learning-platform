
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