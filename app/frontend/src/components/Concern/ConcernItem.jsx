import React from 'react';
import styles from "./Concern.module.css";

function ConcernItem({item_data}) {
    return ( 
        <div className={styles.concern__item}>
            <div className={styles.concern__itemTitle}>{ item_data.title }</div>
            <div className={styles.concern__itemText}>{ item_data.body }</div>
        </div>
    );
}

export default ConcernItem;