import React from 'react';

function FacebookLink(props) {
    return (  
        <a {...props} target="_blank" rel="noreferrer" href="https://www.facebook.com/profile.php?id=100079376305648"><img src={require('../../assets/facebook.svg').default} alt="" /></a>
    );
}

export default FacebookLink;