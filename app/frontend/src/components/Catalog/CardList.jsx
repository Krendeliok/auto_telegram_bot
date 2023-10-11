import React, { useState, useEffect } from 'react';
import Card from './Card/Card';

import AboutCarPopup from '../Popup/AboutCarPopup';

function CardList({ lockBody }) {
    const [ cards, setCards ] = useState([])
    
    const url = "/advertisements"

    useEffect(() => {
        fetch(url).then(response => {
            if (response.status == 200) {
                return response.json()
            }
        }).then(data => setCards(data))
    }, [])
    
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
            <AboutCarPopup {...popupData} setVisible={(v) => setAboutCarModalVisible(v, popupData.advertisement_id) } />
            {
                cards.map((card_data, index) => 
                    <>
                        <Card card_data={card_data} key={card_data.id} openPopup={setAboutCarModalVisible} />
                        {index !== cards.length - 1 ? <hr/> : ""}
                    </>
                )
            }
        </div>
    );
}

export default CardList;