import React from 'react';

import InstagramLink from '../Links/InstagramLink';
import TelegramLink from '../Links/TelegramLink';
import ViberLink from '../Links/ViberLink';
import TikTokLink from '../Links/TikTokLink';
import FacebookLink from '../Links/FacebookLink';

import mapImage from '../../assets/map.png';
import Contact from './Contact';

function Contacts() {
    const contacts = [
        {
            id: 1,
            title: "Адреса",
            body: "Закарпаття, с. Кінчеш (околиця Ужгороду) Фізкультурна вул., 2а – територія авторинку",
            icon_class: "_icon-location"
        },
        {
            id: 2,
            title: "Графік роботи",
            body: "Щодня 09:00 – 17:00",
            icon_class: "_icon-calendar"
        },
        {
            id: 3,
            title: "Телефони",
            body: "+38 (097) 62 00 777 <br/>+38(050) 62 00 777",
            icon_class: "_icon-phone"
        },
        {
            id: 4,
            title: "Пошта",
            body: "autoyarmarok@gmail.com",
            icon_class: "_icon-mail"
        },
    ]

    return (
        <div className="contacts" id="contacts">
            <div className="container">
                <div className="contacts__body">
                    <div className="contacts__data">
                        <div className="contacts__title block-title">Де нас знайти?</div>
                        <div className="contacts__text">
                            {contacts.map(contact =>
                                <Contact contact_data={contact} key={contact.id} />
                            )}
                            <div className="text__media">
                                <div className="media__item"><InstagramLink /></div>
                                <div className="media__item"><TelegramLink /></div>
                                <div className="media__item"><ViberLink /></div>
                                <div className="media__item"><FacebookLink /></div>
                                <div className="media__item"><TikTokLink /></div>
                            </div>
                        </div>
                    </div>
                    <div className="contacts__map"><img src={mapImage} alt="map" /></div>
                </div>
            </div>
        </div>
    );
}

export default Contacts;