import React from 'react';

import PrimaryButton from '../UI/PrimaryButton';
import ContentGoods from './ContentGoods';
import styles from "./Content.module.css";

function Content() {
    return (
        <div>
            <div className="container">
                <div className={styles.content__body}>
                    <div className={styles.content__info}>
                        <div className={styles.info__title}>
                            <div className={styles.title__head}>АвтоЯрмарок</div>
                            <div className={styles.title__subtitle}>ПРОДАЖ ТА ПІДБІР АВТО ШВИДКО ТА ВИГІДНО</div>
                        </div>
                        <div className={[styles.info__body, "block-subtitle"].join(" ")}>
                            Ми - твій шлях до автомобільних мрій! Зустріньмося на нашому автомайданчику, де реалізуються автопобажання та здійснюються угоди з посмішкою!
                        </div>
                        <div className={styles.info__image}>
                            <img src={require('../../assets/avto.svg').default} alt="" />
                            <div className={styles.info__imageBlur}></div>
                        </div>
                    </div>
                    <div className={styles.content__data}>
                        <ContentGoods/>
                        <a href="#catalog">
                            <PrimaryButton> Автомобілі у наявності </PrimaryButton>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Content;