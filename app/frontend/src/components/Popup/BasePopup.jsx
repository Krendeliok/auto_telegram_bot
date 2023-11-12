import React from 'react';

import CloseSVG from "../../assets/close.svg"

function BasePopup({ children, visible, setVisible}) {
    const rootClasses = ["popup__wrapper"];

    if (visible) {
        rootClasses.push("active");
    }

    const closePopup = () => {
        setVisible(false);
    }


    return ( 
        <div className={rootClasses.join(" ")} onClick={closePopup}>
            <div className="popup__container" onClick={(e) => e.stopPropagation()}>
                <div className="popup__body">
                    { children }
                </div>
                <div className="popup__close" onClick={closePopup}><img src={CloseSVG} alt="" /></div>
            </div>
        </div>
    );
}

export default BasePopup;