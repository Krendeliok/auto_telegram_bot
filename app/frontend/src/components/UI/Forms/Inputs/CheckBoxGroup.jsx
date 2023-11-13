import React from 'react';
import CheckBox from './CheckBox';

function CheckBoxGroup({label, groupName, checkboxList, onClick}) {
    return (  
        <div className="checkboxes__group">
            <label>{label}</label>
            <div className="checkboxes__group-items">
                {checkboxList?.map(val => 
                    <CheckBox key={val.id} groupName={groupName} id={val.id} text={val.name} isChecked={val.checked} onClick={ onClick } />
                )}
            </div>
            
        </div>
    );
}

export default CheckBoxGroup;