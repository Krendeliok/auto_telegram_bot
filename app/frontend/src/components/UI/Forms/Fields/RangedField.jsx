import React from 'react';
import DualRangeInput from '../Inputs/DualRangeInput';

function RangedField({ name, labelText, measurement, minData, maxData, isFloat }) {
    const step = isFloat ? 0.1 : 1;
    return (  
        <div className='ranged__field'> 
            <div className='ranged__field-label'>{labelText}</div>
            <div className='ranged__field-values'>
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
                <div className="measuring__points">{measurement}</div>
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