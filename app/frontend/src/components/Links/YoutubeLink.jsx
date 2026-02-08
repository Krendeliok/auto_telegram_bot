import React from 'react';


function YoutubeLink(props) {
    return (
        <a {...props} target="_blank" rel="noreferrer" href="https://www.youtube.com/@Autoyarmarok_com"><img src={require('../../assets/youtube.svg').default} alt="" /></a>
    );
}

export default YoutubeLink;