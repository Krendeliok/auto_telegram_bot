import React, { useEffect, useRef, useState } from 'react';

import ArrowSVG from "../../../../assets/arrow.svg"
import SelectedFieldOption from './SelectedFieldOption';
import SortSVG from "../../../../assets/sort.svg";

import styles from './Fields.module.css';

function SelectField({ selected, options, placeholder, onChange, onClose }) {
    const [isOpen, setIsOpen] = useState(false);
    const rootRef = useRef(null);
    const placeholderRef = useRef(null);
    const arrowRef = useRef(null);

    useEffect(() => {
        if (isOpen) {
            arrowRef.current.classList.add("active");
        }
        else {
            arrowRef.current.classList.remove("active");
        }
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
        <div ref={rootRef} data-is-active={isOpen} className={styles.select__root}>
            <div
                className={styles.select__placeholder}
                data-selected={!!selected?.value}
                onClick={handlePlaceHolderClick}
                role='button'
                tabIndex={0}
                ref={placeholderRef}
            >
                {selected?.title || placeholder}
                <div className={styles.select__arrow} ref={arrowRef}><img src={ArrowSVG} alt="" /></div>
            </div>
            <div
                className={styles.select__placeholder__icon}
                data-selected={!!selected?.value}
                onClick={handlePlaceHolderClick}
                role='button'
                tabIndex={0}
                ref={placeholderRef}
            >
                <img src={SortSVG} alt="filter-icon"/>
            </div>
            
            {isOpen && (
                <ul className="select__options">
                    <div className={styles.select__delimiter}></div>
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