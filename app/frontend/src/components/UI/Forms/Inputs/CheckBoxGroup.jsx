import React from 'react';
import CheckBox from './CheckBox';
import styles from './Inputs.module.css';

function CheckBoxGroup({label, groupName, checkboxList, onClick}) {
    return (  
        <div className={styles.checkboxes__group}>
            <label>{label}</label>
            <div className={styles.checkboxes__groupItems}>
                {checkboxList?.map(val => 
                    <CheckBox key={val.id} groupName={groupName} id={val.id} text={val.name} isChecked={val.checked} onClick={ onClick } />
                )}
            </div>
            
        </div>
    );
}

export default CheckBoxGroup;