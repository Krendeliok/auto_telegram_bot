import React from 'react';
import headerStyles from '../Header/Header.module.css';

function LogoLink() {
    return (  
        <a href="/" className={headerStyles.header__logo}>
            <img src={require('../../assets/logo.svg').default} alt="" />
        </a>
    );
}

export default LogoLink;