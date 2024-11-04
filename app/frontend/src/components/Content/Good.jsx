import React from 'react';
import styles from './Content.module.css';

function Good({good_data}) {
    return ( 
        <div className={styles.goods__good}>
            <div className={styles.good__title}>
                <div className={styles.title__number}>{good_data.number}</div>
                <div className={styles.title__text}>{good_data.title}</div>
            </div>
            <div className={styles.good__text}>{good_data.body}</div>
        </div>
     );
}

export default Good;