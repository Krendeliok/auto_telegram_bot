import React from 'react';

import CloseSVG from "../../assets/close.svg"
import styles from "./Popup.module.css";

function BasePopup({ children, visible, setVisible}) {
    const rootClasses = [styles.popup__wrapper];

    if (visible) {
        rootClasses.push(styles.active);
    }

    const closePopup = () => {
        setVisible(false);
    }


    return ( 
        <div className={rootClasses.join(" ")} onClick={closePopup}>
            <div className={styles.popup__container} onClick={(e) => e.stopPropagation()}>
                <div className={styles.popup__body}>
                    { children }
                </div>
                <div className={styles.popup__close} onClick={closePopup}><img src={CloseSVG} alt="" /></div>
            </div>
        </div>
    );
}

export default BasePopup;