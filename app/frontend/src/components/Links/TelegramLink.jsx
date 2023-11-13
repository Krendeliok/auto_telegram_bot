import React from 'react';


function TelegramLink(props) {
    return ( 
        <a {...props} target="_blank" rel="noreferrer" href="https://t.me/AutoYarmarokUkraina"><img src={require('../../assets/telegram.svg').default} alt="" /></a>
    );
}

export default TelegramLink;