import React from 'react';
import styles from './Header.module.css';

function Menu() {
    return ( 
        <ul className={styles.menu__list}>
            <li><a href="/" className={styles.menu__link}>Головна</a></li>
            <li><a href="#about" className={styles.menu__link}>Про компанію</a></li>
            <li><a href="#catalog" className={styles.menu__link}>Каталог</a></li>
            <li><a href="#contacts" className={styles.menu__link}>Контакти</a></li>
        </ul>
     );
}

export default Menu;