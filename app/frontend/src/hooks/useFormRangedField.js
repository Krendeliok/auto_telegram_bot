import { useState, useCallback } from "react";

const useFormRangedField = (min, max, step) => {
    const [minValue, setMinValue] = useState(min);
    const [maxValue, setMaxValue] = useState(max);

    const minData = {
        min: min,
        max: max,
        value: minValue,
        onChange: useCallback((event) => {
            const value = Math.min(Number(event.target.value), maxValue - step);
            setMinValue(value);
        }, [maxValue])
    }

    const maxData = {
        min: min,
        max: max,
        value: maxValue,
        onChange: useCallback((event) => {
            const value = Math.max(Number(event.target.value), minValue + step);
            setMaxValue(value);
        }, [minValue])
    }

    const getValues = useCallback(() => {
        return { min: minValue, max: maxValue }
    }, [minValue, maxValue]);

    return [getValues, { minData, maxData }];
};

export default useFormRangedField;