import React, { useState } from 'react';

import styles from './FilterItem.module.css';

function FilterItem({ title, children }) {
    const [isOpen, setIsOpen] = useState(true);
    return (
        <div className={styles.filterItem}>
            <div className={styles.header} onClick={() => setIsOpen(!isOpen)}>
                <div className={styles.header__title}>{title}</div>
                <span>{isOpen ? 'Скрыть' : 'Показать'}</span>
            </div>
            <div className={[styles.item__container, isOpen ? 'active' : ''].join(" ")}>
                {children}
            </div>
        </div>
    )
}

export default FilterItem;