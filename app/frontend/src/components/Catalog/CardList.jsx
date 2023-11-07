import React, { useState } from 'react';
import Card from './Card/Card';

import AboutCarPopup from '../Popup/AboutCarPopup';

function CardList({ lockBody, cards, cardsLoading }) {
    const [popupData, setAboutCarModal] = useState({
        visible: false,
        advertisement_id:0
    });
    const setAboutCarModalVisible = (visible, advertisement_id) => {
        setAboutCarModal({ visible: visible, advertisement_id: advertisement_id});
        lockBody(visible);
    }

    return (
        <div className="content__cards">
            {cards.length > 0 && !cardsLoading
                ? <>
                    <AboutCarPopup {...popupData} setVisible={(v) => setAboutCarModalVisible(v, popupData.advertisement_id)} />
                    {
                        cards.map((card_data, index) =>
                            <>
                                <Card card_data={card_data} key={card_data.id} openPopup={setAboutCarModalVisible} />
                                {index !== cards.length - 1 ? <hr /> : ""}
                            </>
                        )
                    }
                </>
                : <h1>Машин за вашим запитом немає</h1>
            }
            
        </div>
    );
}

export default CardList;