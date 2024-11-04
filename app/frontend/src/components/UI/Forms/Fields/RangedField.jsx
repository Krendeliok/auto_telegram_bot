import React from 'react';
import DualRangeInput from '../Inputs/DualRangeInput';
import styles from './Fields.module.css';

function RangedField({ name, labelText, measurement, minData, maxData, isFloat }) {
    const step = isFloat ? 0.1 : 1;
    return (  
        <div className={styles.ranged__field}>
            <div className={styles.ranged__fieldLabel}>{labelText}</div>
            <div className={styles.ranged__fieldValues}>
                <input
                    type="number"
                    name={name + '_min_value'}
                    {...minData}
                    step={step}
                />
                <span></span>
                <input
                    type="number"
                    name={name + '_max_value'}
                    {...maxData}
                    step={step}
                />
                <div className={styles.measuring__points}>{measurement}</div>
            </div>
            <DualRangeInput
                minData={minData}
                maxData={maxData}
                isFloat={isFloat}
            />
        </div>
    );
}

export default RangedField;