import React, { useState } from 'react';

import Menu from '../Header/Menu';
import SecondaryButton from '../UI/SecondaryButton';
import FeedbackPopup from '../Popup/FeedbackPopup';

import styles from './Footer.module.css';

function Footer({ lockBody }) {
    const [feedbackModal, setFeedbackModal] = useState(false);
    const setFeedbackModalVisible = (v) => {
        setFeedbackModal(v);
        lockBody(v);
    }

    return (
        <footer>
            <FeedbackPopup visible={feedbackModal} setVisible={setFeedbackModalVisible} />
            <div className="container">
                <div className={styles.footer__body}>
                    <a href="/" className={styles.footer__logo}>
                        <img src={require('../../assets/logo.svg').default} alt="" />
                    </a>
                    <div className={styles.footer__menu}>
                        <Menu />
                    </div>
                    <div className={styles.footer__copyright}>© ТМ «АвтоЯрмарок». Всі права захищено.</div>
                    <SecondaryButton additionalClasses={[styles.footer__button]} onClick={() => { setFeedbackModalVisible(true) }}>Зворотній дзвінок</SecondaryButton>
                </div>
            </div>
        </footer>
    );
}

export default Footer;