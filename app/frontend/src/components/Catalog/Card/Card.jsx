import React from 'react';

import PrimaryButton from '../../UI/PrimaryButton';
import CardAlbum from './CardAlbum';

import CalendarSVG from "../../../assets/calendar.svg"
import OilSVG from "../../../assets/oil.svg"
import TransmissionSVG from "../../../assets/transmission.svg"
import RoadSVG from "../../../assets/road.svg"
import styles from "./Card.module.css";

function Card({ card_data, openPopup }) {
    return (
        <div className={styles.content__card}>
            <CardAlbum images={ card_data.images } />
            <div className={styles.card__data}>
                <div className={styles.data__title}>{card_data.producer} {card_data.model}</div>
                <div className={styles.data__info}>
                    <div className={styles.info__item}>
                        <div className={styles.item__icon}><img src={CalendarSVG} alt="" /></div>
                        {card_data.year} рік
                    </div>
                    <div className={styles.info__item}>
                        <div className={styles.item__icon}><img src={OilSVG} alt="" /></div>
                        {card_data.engine_type} {card_data.engine_volume}
                    </div>
                    <div className={styles.info__item}>
                        <div className={styles.item__icon}><img src={TransmissionSVG} alt="" /></div>
                        {card_data.gearbox_type}
                    </div>
                    <div className={styles.info__item}>
                        <div className={styles.item__icon}><img src={RoadSVG} alt="" /></div>
                        {card_data.range} тис. км
                    </div>
                </div>
                <div>Область знаходження авто: {card_data.based_country}.</div>
                <div> {card_data.description}</div>
                <div className={styles.data__detail}>
                    <div className={styles.detail__price}>{card_data.price} $</div>
                    <div>
                        <PrimaryButton onClick={() => openPopup(true, card_data.id)}>Дізнатися деталі</PrimaryButton>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Card;