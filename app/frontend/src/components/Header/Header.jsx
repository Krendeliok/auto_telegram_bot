import React, { useRef } from 'react';
import LogoLink from '../Links/LogoLink';

import Menu from './Menu';
import InstagramLink from '../Links/InstagramLink';
import TelegramLink from '../Links/TelegramLink';
import ViberLink from '../Links/ViberLink';
import FacebookLink from '../Links/FacebookLink';
import TikTokLink from '../Links/TikTokLink';

import PercentSVG from "../../assets/percent.svg"

import styles from './Header.module.css';


function Header() {

    const burgerRef = useRef();
    const menuRef = useRef();

    const openMenu = () => {
        burgerRef.current.classList.toggle(styles.active);
        menuRef.current.classList.toggle(styles.active);
        document.querySelector("body").classList.toggle("lock");
    };

    const now = new Date();
    const current = new Date(now.getFullYear(), now.getMonth() + 1, 1);

    return (
        <header className={styles.header}>
            <div className="container">
                <div className={styles.promotion}>
                    <div className={styles.promotion__text}> <img src={PercentSVG} alt="" /> Розмісти безкоштовно автомобіль на майданчику! Поспішай! Акція діє до 01.{ ("0" + (current.getMonth() + 1)).slice(-2) }</div>
                </div>
                <div className={styles.header__body}>
                    <LogoLink/>
                    <div className={styles.header__burger} ref={burgerRef} onClick={openMenu}><span></span></div>
                    <nav className={styles.header__menu} ref={menuRef}>
                        <Menu />
                        <div className={styles.menu__phone}>+38 (097) 62 00 777</div>
                        <div className={styles.menu__social}>
                            <InstagramLink className={styles.social__link} />
                            <TelegramLink className={styles.social__link} />
                            <ViberLink className={styles.social__link} />
                            <FacebookLink className={styles.social__link} />
                            <TikTokLink className={styles.social__link} />
                        </div>
                    </nav>
                </div>
            </div>
        </header>
    );
}

export default Header;