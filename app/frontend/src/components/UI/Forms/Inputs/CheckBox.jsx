import React from 'react';
import styles from './Inputs.module.css';

function CheckBox({ groupName, id, text, isChecked,  onClick }) {
    return (  
        <label className={styles.checkboxes__checkbox}>
            <input type="checkbox" name={groupName} value={id} className={isChecked ? styles.checked : ""} onChange={() => onClick(id)} />
            {text}
        </label>
    );
}

export default CheckBox;