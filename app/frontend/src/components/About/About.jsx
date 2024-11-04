import React, { useEffect, useState } from 'react';

import AboutImage from '../../assets/image2.png';
import AboutList from './AboutList';
import PrimaryButton from '../UI/PrimaryButton';
import FeedbackPopup from '../Popup/FeedbackPopup';

import bodySetLock from '../../utils/lockBody'

import styles from './About.module.css';

function About() {
    const [feedbackModal, setFeedbackModalVisible] = useState(false);

    useEffect(() => {
        bodySetLock(feedbackModal)
    }, [feedbackModal])

    return (
        <div id="about">
            <FeedbackPopup visible={feedbackModal} setVisible={setFeedbackModalVisible} />

            <div className="container">
                <div className={styles.about__body}>
                    <div className={styles.about__content}>
                        <div className="block-title">Про нас</div>
                        <div className={styles.about__contentSubtitle}>
                            <div className="block-subtitle">Ми – компанія з продажу та оренди авто. Наша команда
                                професіоналів надасть Вам усю необхідну допомогу і підтримку в
                                процесі продажу. Вам необхідно просто привезти свій автомобіль на майданчик за адресою вул.
                                Фізкультурна, 2а
                                (Закарпатська обл., с. Кінчеш) та скористатися нашими послугами:
                            </div>
                            <AboutList/>
                        </div>
                        <PrimaryButton onClick={() => { setFeedbackModalVisible(true) }}>Забронювати місце</PrimaryButton>
                    </div>
                    <div className={styles.about__image}><img src={AboutImage} alt="" /></div>
                </div>
            </div>
        </div>
    );
}

export default About;