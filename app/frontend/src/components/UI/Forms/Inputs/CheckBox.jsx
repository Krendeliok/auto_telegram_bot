import React from 'react';

function CheckBox({ groupName, id, text, isChecked,  onClick }) {
    return (  
        <label className='checkboxes__checkbox'>
            <input type="checkbox" name={groupName} value={id} className={isChecked ? "checked" : ""} onChange={() => onClick(id)} />
            {text}
        </label>
    );
}

export default CheckBox;