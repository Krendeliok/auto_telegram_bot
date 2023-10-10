import React from 'react';

function Good({good_data}) {
    return ( 
        <div className="goods__good">
            <div className="good__title">
                <div className="title__number">{good_data.number}</div>
                <div className="title__text">{good_data.title}</div>
            </div>
            <div className="good__text">{good_data.body}</div>
        </div>
     );
}

export default Good;