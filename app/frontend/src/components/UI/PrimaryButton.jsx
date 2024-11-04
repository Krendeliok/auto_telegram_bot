import React from 'react';
import styles from './Button.module.css';

function PrimaryButton({ children, additionalClasses = [], ...props }) {
    return ( 
        <div className={[styles.primary__button, ...additionalClasses].join(' ')} {...props}>
            { children }
            <div className={styles.ellips}></div>
            <div className={styles.ellips}></div>
        </div>
     );
}

export default PrimaryButton;