import React, { useState } from 'react';
import Card from './Card/Card';

import autoImage from '../../assets/avto.png';
import secondCar from '../../assets/second_car.png';
import AboutCarPopup from '../Popup/AboutCarPopup';

function CardList({ lockBody }) {
    const cards = [
        {
            id: 1,
            producer: "BMW",
            model: "M3",
            year: 2003,
            engine_type: "Дизель",
            engine_volume: 1.9,
            gearbox_type: "Механіка",
            range: 100,
            based_country: "Закарпатська",
            description: "Авто із Чехії, приведене до ладу. Перебрана ходова, питань по мотору та коробці нема, масло не бере, повторний окрас капоту, є комплект шин, нюанс по лобовому склу.",
            price: 200000,
            images: [
                { id: 3, source: secondCar },
                { id: 4, source: autoImage },
                { id: 5, source: autoImage },
            ]
        },
        {
            id: 2,
            producer: "BMW",
            model: "M3",
            year: 2003,
            engine_type: "Дизель",
            engine_volume: 1.9,
            gearbox_type: "Механіка",
            range: 100,
            based_country: "Закарпатська",
            description: "Авто із Чехії, приведене до ладу. Перебрана ходова, питань по мотору та коробці нема, масло не бере, повторний окрас капоту, є комплект шин, нюанс по лобовому склу.",
            price: 200000,
            images: [
                { id: 6, source: secondCar },
                { id: 7, source: autoImage },
                { id: 8, source: autoImage },
            ]
        }
    ]
    
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