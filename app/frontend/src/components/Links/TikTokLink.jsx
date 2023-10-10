import React from 'react';


function TikTokLink(props) {
    return (  
        <a {...props} target="_blank" rel="noreferrer" href="https://www.tiktok.com/@autofair_ua"><img src={require('../../assets/tiktok.svg').default} alt="" /></a>
    );
}

export default TikTokLink;