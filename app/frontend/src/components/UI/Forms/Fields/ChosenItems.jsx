import React from 'react';
import styles from './Fields.module.css';

function ChosenItems({ items }) {
    let countChecked = 0;
    items?.map((obj) => {
        countChecked += obj.checkboxList?.filter((val) => val.checked).length
        return obj;
    }) 
    

    if (countChecked > 0) {
        return ( 
            <div className={styles.chosen__items}>
                <span>Обрано:</span>
                {items?.map((obj) => 
                    obj.checkboxList?.filter((val) => val.checked).map((el) => 
                        <div className={styles.chosen__itemsItem} key={el.name}>
                            <span>{el.name}</span>
                            <span className={styles.remove__item} onClick={() => { obj.onClick(el.id) }} >x</span>
                        </div>
                    )
                )}
            </div>
        );
    } else {
        return null;
    }
    
}

export default ChosenItems;