import React from 'react';
import BasePopup from './BasePopup';
import AboutCarForm from '../UI/Forms/AboutCarForm';

function AboutCarPopup(props) {
    return (
        <BasePopup visible={props.visible} setVisible={props.setVisible}>
            <div className="popup__text">
                <div className="popup__title">Хочете дізнатися більше про авто?</div>
                <div className="popup__subtitle">Залиште свій номер телефону і ми Вам зателефонуємо протягом 30 хвилин.</div>
            </div>
            <div className="popup__form">
                <AboutCarForm advertisement_id={props.advertisement_id} setVisiblePopup={props.setVisible} />
            </div>
        </BasePopup>
    );
}

export default AboutCarPopup;  