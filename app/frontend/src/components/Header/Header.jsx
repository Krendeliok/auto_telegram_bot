import React, { useRef } from 'react';
import LogoLink from '../Links/LogoLink';

import Menu from './Menu';
import InstagramLink from '../Links/InstagramLink';
import TelegramLink from '../Links/TelegramLink';
import ViberLink from '../Links/ViberLink';
import FacebookLink from '../Links/FacebookLink';
import TikTokLink from '../Links/TikTokLink';

import PercentSVG from "../../assets/percent.svg"


function Header() {

    const burgerRef = useRef();
    const menuRef = useRef();

    const openMenu = () => {
        burgerRef.current.classList.toggle("active");
        menuRef.current.classList.toggle("active");
        document.querySelector("body").classList.toggle("lock");
    };

    const now = new Date();
    const current = new Date(now.getFullYear(), now.getMonth() + 1, 1);

    return (
        <header className="header">
            <div className="container">
                <div className="promotion">
                    <div className="promotion__text"> <img src={PercentSVG} alt="" /> Розмісти безкоштовно автомобіль на майданчику! Поспішай! Акція діє до 01.{ ("0" + (current.getMonth() + 1)).slice(-2) }</div>
                </div>
                <div className="header__body">
                    <LogoLink/>
                    <div className="header__burger" ref={burgerRef} onClick={openMenu}><span></span></div>
                    <nav className="header__menu" ref={menuRef}>
                        <Menu />
                        <div className="menu__phone">+38 (097) 62 00 777</div>
                        <div className="menu__social">
                            <InstagramLink className="social__link" />
                            <TelegramLink className="social__link" />
                            <ViberLink className="social__link" />
                            <FacebookLink className="social__link" />
                            <TikTokLink className="social__link" />
                        </div>
                    </nav>
                </div>
            </div>
        </header>
    );
}

export default Header;