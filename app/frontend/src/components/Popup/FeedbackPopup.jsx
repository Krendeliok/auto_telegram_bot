import React from 'react';
import BasePopup from './BasePopup';
import FeedbackForm from '../UI/Forms/FeedbackForm';
import styles from "./Popup.module.css";

function FeedbackPopup(props) {
    return (  
        <BasePopup visible={props.visible} setVisible={props.setVisible}>
            <div className={styles.popup__text}>
                <div className={styles.popup__title}>Залишилися питання?</div>
                <div className={styles.popup__subtitle}>Напишіть нам свій номер телефону і ми Вам зателефонуємо протягом 30 хвилин.</div>
            </div>
            <div className={styles.popup__form}>
                <FeedbackForm setVisiblePopup={props.setVisible}/>
            </div>
        </BasePopup>
    );
}

export default FeedbackPopup;  