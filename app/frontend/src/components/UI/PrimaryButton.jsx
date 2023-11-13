import React from 'react';

function PrimaryButton({ children, additionalClasses, ...props }) {
    return ( 
        <div className={["primary__button", ...additionalClasses].join(' ')} {...props}>
            { children }
            <div className="ellips"></div>
            <div className="ellips"></div>
        </div>
     );
}

export default PrimaryButton;