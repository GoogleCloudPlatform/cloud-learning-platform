


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