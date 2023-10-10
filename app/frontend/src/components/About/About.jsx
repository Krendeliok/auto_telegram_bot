import React, { useState } from 'react';

import AboutImage from '../../assets/image2.png';
import AboutList from './AboutList';
import PrimaryButton from '../UI/PrimaryButton';
import FeedbackPopup from '../Popup/FeedbackPopup';

function About({ lockBody }) {
    const [feedbackModal, setFeedbackModal] = useState(false);
    const setFeedbackModalVisible = (v) => {
        setFeedbackModal(v);
        lockBody(v);
    }

    return (
        <div className="about" id="about">
            <FeedbackPopup visible={feedbackModal} setVisible={setFeedbackModalVisible} />

            <div className="container">
                <div className="about__body">
                    <div className="about__content">
                        <div className="about__content-title block-title">Про нас</div>
                        <div className="about__content-subtitle">
                            <div className="content-subtitle__text block-subtitle">Ми – компанія з продажу та оренди авто. Наша команда
                                професіоналів надасть Вам усю необхідну допомогу і підтримку в
                                процесі продажу. Вам необхідно просто привезти свій автомобіль на майданчик за адресою вул.
                                Фізкультурна, 2а
                                (Закарпатська обл., с. Кінчеш) та скористатися нашими послугами:
                            </div>
                            <AboutList/>
                        </div>
                        <PrimaryButton additionalClasses={["more-info__button"]} onClick={() => { setFeedbackModalVisible(true) }}>Забронювати місце</PrimaryButton>
                    </div>
                    <div className="about__image"><img src={AboutImage} alt="" /></div>
                </div>
            </div>
        </div>
    );
}

export default About;