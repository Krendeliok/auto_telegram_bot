import React from 'react';


function ViberLink(props) {
    return (  
        <a {...props} target="_blank" rel="noreferrer" href="https://invite.viber.com/?g2=AQAie76gL%2BHDQFFwXJZyQzmmK47hp5GuJqXYShaJItslqsiB1z%2B47vIcj%2FyKyaGG"><img src={require('../../assets/viber.svg').default} alt="" /></a>
    );
}

export default ViberLink;