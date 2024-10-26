import React, { useRef, useState } from 'react';

function CardAlbum({ images }) {

    const mainImageRef = useRef()
    const [currentImage, setCurrentImage] = useState(0);

    const setAsMain = (e) => {
        let mainImageSrc = mainImageRef.current.src; 
        mainImageRef.current.src = e.target.src;
        e.target.src = mainImageSrc;
    }

    const onLeftArrowClick = (e) => {
        mainImageRef.current.src = images[(currentImage - 1 + images.length) % images.length].source;
        setCurrentImage((prev) => (prev - 1 + images.length) % images.length)
    }

    const onRightArrowClick = (e) => {
        mainImageRef.current.src = images[(currentImage + 1) % images.length].source;
        setCurrentImage((prev) => (currentImage + 1) % images.length)
    }


    return (
        <div className="card__album">
            {
                <div className="album__images">
                    <div className="album__image">
                        <img src={images[0]?.source} alt="" ref={mainImageRef}/>
                    </div>
                    {images.length > 1
                        ? images.slice(1).map(image =>
                            <div className="album__image" key={image.id}>
                                <img src={image.source} alt="" onClick={setAsMain}/>
                            </div>
                        )
                        : ""
                    }
                    <div className="allcards__fogging"></div>
                    <div className="carousel">
                        <div className="carousel__arrow" onClick={onLeftArrowClick}></div>
                        <div className="carousel__arrow right" onClick={onRightArrowClick}></div>
                        <div className="breadcrumbs">
                            {images.map((image, index) => <div key={image.id}
                                                          className={index === currentImage ? "active" : ""}></div>)}
                        </div>
                    </div>
                </div>
            }
            <div className="fogging"></div>
        </div>
    );
}

export default CardAlbum;