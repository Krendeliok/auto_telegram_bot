import React from 'react';

function SecondaryButton({ children, additionalClasses, ...props }) {
    return ( 
        <button className={ ["secondary__button", ...additionalClasses].join(' ') } {...props}>{children}</button>
    );
}

export default SecondaryButton;