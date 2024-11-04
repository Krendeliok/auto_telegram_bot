import React, { useRef, useState } from 'react';
import styles from "./Card.module.css";

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
        <div className={styles.card__album}>
            {
                <div className={styles.album__images}>
                    <div className={styles.album__image}>
                        <img src={images[0]?.source} alt="" ref={mainImageRef}/>
                    </div>
                    {images.length > 1
                        ? images.slice(1).map(image =>
                            <div className={styles.album__image} key={image.id}>
                                <img src={image.source} alt="" onClick={setAsMain}/>
                            </div>
                        )
                        : ""
                    }
                    <div className={styles.allcards__fogging}></div>
                    <div className={styles.carousel}>
                        <div className={styles.carousel__arrow} onClick={onLeftArrowClick}></div>
                        <div className={[styles.carousel__arrow, styles.right].join(" ")} onClick={onRightArrowClick}></div>
                        <div className={styles.breadcrumbs}>
                            {images.map((image, index) => <div key={image.id}
                                                          className={index === currentImage ? styles.active : ""}></div>)}
                        </div>
                    </div>
                </div>
            }
            <div className={styles.fogging}></div>
        </div>
    );
}

export default CardAlbum;