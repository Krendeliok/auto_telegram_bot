import React, { useRef } from 'react';

function CardAlbum({ images }) {

    const mainImageRef = useRef()

    const setAsMain = (e) => {
        let mainImageSrc = mainImageRef.current.src; 
        mainImageRef.current.src = e.target.src;
        e.target.src = mainImageSrc;
    }


    return (  
        <div className="card__album">
            {
                <div className="album__main-image">
                    <img src={images[0]?.source} alt="" ref={mainImageRef}/>
                </div>
            }
            <div className="fogging"></div>
            {images.length > 1
                ? <div className="album__all-images">
                    {images.slice(1).map(image => 
                        <div className="album__image" key={image.id}>
                            <img src={image.source} alt="" onClick={setAsMain}/>
                        </div>
                    )}
                </div>
                : ""
            }
        </div>
    );
}

export default CardAlbum;