import React from 'react';
import { scrollToSection } from '../../utils/scroll';

function Menu() {
    const handleLinkClick = (e) => {
        const href = e.currentTarget.getAttribute('href');
        if (href?.startsWith('#')) {
          e.preventDefault();
          scrollToSection(href.slice(1), 'smooth');
        }
      };
    return ( 
        <ul className="menu__list">
            <li><a href="/" className="menu__link">Головна</a></li>
            <li><a href="#about" className="menu__link" onClick={handleLinkClick}>Про компанію</a></li>
            <li><a href="#catalog" className="menu__link" onClick={handleLinkClick}>Каталог</a></li>
            <li><a href="#contacts" className="menu__link" onClick={handleLinkClick}>Контакти</a></li>
        </ul>
     );
}

export default Menu;