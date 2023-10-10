import React from 'react';

import PrimaryButton from '../UI/PrimaryButton';
import ContentGoods from './ContentGoods';

function Content() {
    return (
        <div className="content">
            <div className="container">
                <div className="content__body">
                    <div className="content__info">
                        <div className="info__title">
                            <div className="title__head">АвтоЯрмарок</div>
                            <div className="title__subtitle">ПРОДАЖ ТА ПІДБІР АВТО ШВИДКО ТА ВИГІДНО</div>
                        </div>
                        <div className="info__body block-subtitle">
                            Ми - твій шлях до автомобільних мрій! Зустріньмося на нашому автомайданчику, де реалізуються автопобажання та здійснюються угоди з посмішкою!
                        </div>
                        <div className="info__image">
                            <img src={require('../../assets/avto.svg').default} alt="" />
                            <div className="info__image-blur"></div>
                        </div>
                    </div>
                    <div className="content__data">
                        <ContentGoods/>
                        <a href="#catalog">
                            <PrimaryButton additionalClasses={["cars__button"]}> Автомобілі у наявності </PrimaryButton>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Content;