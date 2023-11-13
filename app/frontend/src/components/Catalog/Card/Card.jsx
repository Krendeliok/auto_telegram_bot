import React from 'react';

import PrimaryButton from '../../UI/PrimaryButton';
import CardAlbum from './CardAlbum';

import CalendarSVG from "../../../assets/calendar.svg"
import OilSVG from "../../../assets/oil.svg"
import TransmissionSVG from "../../../assets/transmission.svg"
import RoadSVG from "../../../assets/road.svg"

function Card({ card_data, openPopup }) {
    return (
        <div className="content__card">
            <CardAlbum images={ card_data.images } />
            <div className="card__data">
                <div className="data__title">{card_data.producer} {card_data.model}</div>
                <div className="data__info">
                    <div className="info__item">
                        <div className="item__icon"><img src={CalendarSVG} alt="" /></div>
                        {card_data.year} рік
                    </div>
                    <div className="info__item">
                        <div className="item__icon"><img src={OilSVG} alt="" /></div>
                        {card_data.engine_type} {card_data.engine_volume}
                    </div>
                    <div className="info__item">
                        <div className="item__icon"><img src={TransmissionSVG} alt="" /></div>
                        {card_data.gearbox_type}
                    </div>
                    <div className="info__item">
                        <div className="item__icon"><img src={RoadSVG} alt="" /></div>
                        {card_data.range} тис. км
                    </div>
                </div>
                <div className="data__region">Область знаходження авто: {card_data.based_country}.</div>
                <div className="data__description">{card_data.description}</div>
                <div className="data__detail">
                    <div className="detail__price">{card_data.price} $</div>
                    <div className="detail__more-info">
                        <PrimaryButton additionalClasses={["more-info__button"]} onClick={() => openPopup(true, card_data.id)}>Дізнатися деталі</PrimaryButton>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Card;