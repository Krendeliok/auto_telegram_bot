import React, { useEffect, useRef, useState } from 'react';

import ArrowSVG from "../../../../assets/arrow.svg"
import SelectedFieldOption from './SelectedFieldOption';

function SelectField({ selected, options, placeholder, onChange, onClose }) {
    const [isOpen, setIsOpen] = useState(false);
    const rootRef = useRef(null);
    const placeholderRef = useRef(null);
    const arrowRef = useRef(null);

    useEffect(() => {
        arrowRef.current.classList.toggle("active");
    }, [isOpen])

    useEffect(() => {
        const placeholderEl = placeholderRef.current;
        if (!placeholderEl) return;

        const handleClick = (event) => {
            if (event.key === 'Enter') {
                setIsOpen((prev) => !prev);
            }
        };

        placeholderEl.addEventListener('keydown', handleClick);

        return () => {
            placeholderEl.removeEventListener('keydown', handleClick);
        };
    }, []);

    useEffect(() => {
        const handleClick = (event) => {
            const { target } = event;
            if (target instanceof Node && !rootRef.current?.contains(target)) {
                isOpen && onClose?.();
                setIsOpen(false);
            }
        };

        window.addEventListener('click', handleClick);

        return () => {
            window.removeEventListener('click', handleClick);
        };
    }, []);

    const handleOptionClick = (value) => {
        setIsOpen(false);
        onChange?.(value);
    };

    const handlePlaceHolderClick = () => {
        setIsOpen((prev) => !prev);
    };

    return (  
        <div ref={rootRef} data-is-active={isOpen} className='select__root'>
            <div
                className="select__placeholder"
                data-selected={!!selected?.value}
                onClick={handlePlaceHolderClick}
                role='button'
                tabIndex={0}
                ref={placeholderRef}
            >
                {selected?.title || placeholder}
                <div className="select__arrow active" ref={arrowRef}><img src={ArrowSVG} alt="" /></div>
            </div>
            
            {isOpen && (
                <ul className="select__options">
                    <div className='select__delimiter'></div>
                    {options.map((option) => (
                        <SelectedFieldOption
                            key={option.value}
                            option={option}
                            onClick={handleOptionClick}
                        />
                    ))}
                </ul>
            )}
            
        </div>
    );
}

export default SelectField;