import React from 'react';

function Menu() {
    return ( 
        <ul className="menu__list">
            <li><a href="/" className="menu__link">Головна</a></li>
            <li><a href="#about" className="menu__link">Про компанію</a></li>
            <li><a href="#catalog" className="menu__link">Каталог</a></li>
            <li><a href="#contacts" className="menu__link">Контакти</a></li>
        </ul>
     );
}

export default Menu;