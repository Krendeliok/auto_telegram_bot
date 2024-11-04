import React from 'react';
import styles from './Button.module.css';

function SecondaryButton({ children, additionalClasses, ...props }) {
    return ( 
        <button className={ [styles.secondary__button, ...additionalClasses].join(' ') } {...props}>{children}</button>
    );
}

export default SecondaryButton;