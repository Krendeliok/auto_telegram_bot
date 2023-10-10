import React from 'react';

function LogoLink() {
    return (  
        <a href="/" className="header__logo">
            <img src={require('../../assets/logo.svg').default} alt="" />
        </a>
    );
}

export default LogoLink;