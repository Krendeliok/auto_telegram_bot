import React from 'react';

function ConcernItem({item_data}) {
    return ( 
        <div className="concern__item">
            <div className="concern__item-title">{ item_data.title }</div>
            <div className="concern__item-text">{ item_data.body }</div>
        </div>
    );
}

export default ConcernItem;