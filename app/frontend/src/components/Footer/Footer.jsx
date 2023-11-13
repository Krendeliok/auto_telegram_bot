import React, { useState } from 'react';

import Menu from '../Header/Menu';
import SecondaryButton from '../UI/SecondaryButton';
import FeedbackPopup from '../Popup/FeedbackPopup';

function Footer({ lockBody }) {
    const [feedbackModal, setFeedbackModal] = useState(false);
    const setFeedbackModalVisible = (v) => {
        setFeedbackModal(v);
        lockBody(v);
    }

    return (
        <footer className="footer">
            <FeedbackPopup visible={feedbackModal} setVisible={setFeedbackModalVisible} />
            <div className="container">
                <div className="footer__body">
                    <a href="/" className="header__logo">
                        <img src={require('../../assets/logo.svg').default} alt="" />
                    </a>
                    <div className="footer__menu">
                        <Menu />
                    </div>
                    <div className="footer__copyright">© ТМ «АвтоЯрмарок». Всі права захищено.</div>
                    <SecondaryButton additionalClasses={["footer__button"]} onClick={() => { setFeedbackModalVisible(true) }}>Зворотній дзвінок</SecondaryButton>
                </div>
            </div>
        </footer>
    );
}

export default Footer;