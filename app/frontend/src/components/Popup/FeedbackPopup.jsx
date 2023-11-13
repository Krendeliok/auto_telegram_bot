import React from 'react';
import BasePopup from './BasePopup';
import FeedbackForm from '../UI/Forms/FeedbackForm';

function FeedbackPopup(props) {
    return (  
        <BasePopup visible={props.visible} setVisible={props.setVisible}>
            <div className="popup__text">
                <div className="popup__title">Залишилися питання?</div>
                <div className="popup__subtitle">Напишіть нам свій номер телефону і ми Вам зателефонуємо протягом 30 хвилин.</div>
            </div>
            <div className="popup__form">
                <FeedbackForm setVisiblePopup={props.setVisible}/>
            </div>
        </BasePopup>
    );
}

export default FeedbackPopup;  