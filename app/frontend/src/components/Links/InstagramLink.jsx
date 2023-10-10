import React from 'react';

function InstagramLink(props) {
    return ( 
        <a {...props} target="_blank" rel="noreferrer" href="https://www.instagram.com/autoyarmarok/"><img src={require('../../assets/instagram.svg').default} alt="" /></a>
    );
}

export default InstagramLink;