import React from 'react';

import PrimaryButton from '../../UI/PrimaryButton';
import CardAlbum from './CardAlbum';

function Card({ card_data, openPopup }) {
    return (
        <div className="content__card">
            <CardAlbum images={ card_data.images } />
            <div className="card__data">
                <div className="data__title">{card_data.producer} {card_data.model}</div>
                <div className="data__info">
                    <div className="info__item _icon-calendar">{card_data.year} рік</div>
                    <div className="info__item _icon-oil">{card_data.engine_type} {card_data.engine_volume}</div>
                    <div className="info__item _icon-transmission">{card_data.gearbox_type}</div>
                    <div className="info__item _icon-fwd">Повний</div>
                    <div className="info__item _icon-road">{card_data.range} тис. км</div>
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