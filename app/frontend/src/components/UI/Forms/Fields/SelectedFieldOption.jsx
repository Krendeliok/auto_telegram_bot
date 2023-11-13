import React, { useRef, useEffect } from 'react';

function SelectedFieldOption({option, onClick}) {
    const optionRef = useRef(null);
    const { value, title } = option;
    useEffect(() => {
        const option = optionRef.current;
        if (!option) return;

        const handleEnterPress = (event) => {
            if ((document.activeElement === option) && event.key === 'Enter') {
                onClick(value);
            }
        }

        option.addEventListener('keydown', handleEnterPress);

        return () => {
            option.removeEventListener('keydown', handleEnterPress);
        };
    }, [value, onClick]);

    const handleClick = (clickedValue) =>
            () => {
                onClick(clickedValue);
            };

    return (
        <li
            className="select__option"
            value={value}
            onClick={handleClick(value)}
            tabIndex={0}
            ref={optionRef}
        >
            {title}
        </li>
    );
}

export default SelectedFieldOption;