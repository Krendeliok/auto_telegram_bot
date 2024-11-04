import React from 'react';
import BasePopup from "./BasePopup";

import FilterForm from '../UI/Forms/FilterForm'
import styles from "./Popup.module.css";

function FilterPopup(props) {
    const count = props.countChecked();
    return ( 
        <BasePopup visible={props.visible} setVisible={props.setVisible}>
            <div className={styles.popup__text}>
                <div className={styles.popup__title}>{count > 0 ? `Фільтр (${count})` : "Фільтр" }</div>
            </div>
            <div className={styles.popup__form}>
                <FilterForm sendFilter={props.updateFilter} />
            </div>
        </BasePopup>
     );
}

export default FilterPopup;