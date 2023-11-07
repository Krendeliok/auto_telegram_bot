import React from 'react';

function ChoosenItems({ items }) {
    let countChecked = 0;
    items?.map((obj) => {
        countChecked += obj.checkboxList?.filter((val) => val.checked).length
        return obj;
    }) 
    

    if (countChecked > 0) {
        return ( 
            <div className="choosen__items">
                <span>Обрано:</span>
                {items?.map((obj) => 
                    obj.checkboxList?.filter((val) => val.checked).map((el) => 
                        <div className="choosen__items-item" key={el.name}>
                            <span>{el.name}</span>
                            <span className='remove__item' onClick={() => { obj.onClick(el.id) }} >x</span>
                        </div>
                    )
                )}
            </div>
        );
    } else {
        return null;
    }
    
}

export default ChoosenItems;