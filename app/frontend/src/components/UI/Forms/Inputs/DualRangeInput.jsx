import React, { useCallback, useEffect, useRef } from 'react';
import styles from './Inputs.module.css';

function DualRangeInput({ minData, maxData, isFloat = false }) {
    const range = useRef(null);
    const step = isFloat ? 0.1 : 1;

    const getPercent = useCallback(
        (value) => Math.round(((value - minData.min) / (minData.max - minData.min)) * 100),
        [minData.min, minData.max]
    );

    useEffect(() => {
        const minPercent = getPercent(minData.value);
        const maxPercent = getPercent(maxData.value);

        if (range.current) {
            range.current.style.left = `${minPercent}%`;
            range.current.style.width = `${maxPercent - minPercent}%`;
        }
    }, [minData.value, maxData.value, getPercent]);

    return (
        <div className="dual-range">
            <input
                type="range"
                {...minData}
                step={step}
                className={styles.thumbLeft}
                style={{ zIndex: minData.value > minData.max - 100 && "5" }}
            />
            <input
                type="range"
                {...maxData}
                step={step}
                className={styles.thumbRight}
            />
            <div className={styles.slider}>
                <div className={styles.slider__track} />
                <div ref={range} className={styles.slider__range} />
            </div>
        </div>
    );
}

export default DualRangeInput;