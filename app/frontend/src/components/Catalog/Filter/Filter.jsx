import React, { useEffect, useState } from 'react';

import FilterPopup from '../../Popup/FilterPopup'
import SecondaryButton from '../../UI/SecondaryButton';

import bodySetLock from '../../../utils/lockBody';

import FilterSVG from "../../../assets/filter.svg"
import SelectField from '../../UI/Forms/Fields/SelectField';

import styles from './Filter.module.css';

const sortOptions = [
        {
            value: "default",
            title: "За замовчуванням"
        },
        {
            value: "cheapest",
            title: "Від дешевих до дорогих"
        },
        {
            value: "expensive",
            title: "Від дорогих до дешевих"
        },
        {
            value: "new",
            title: "Спочатку нові"
        }
    ]

function Filter({ countChecked, setFilter, sort, setSort }) {
    const count = countChecked();
    const selectedSort = sortOptions.find((item) => item.value === sort);
    const [filterVisible, setFilterVisible] = useState(false);
    useEffect(() => {
        bodySetLock(filterVisible);
    }, [filterVisible])

    const updateFilter = (filter) => {
        setFilterVisible(false);
        setFilter(filter);
    }

    const handleSortSelect = (value) => {
        setSort(value);
    };

    return (
        <div className={styles.catalog__filter}>
            <FilterPopup visible={filterVisible} setVisible={setFilterVisible} countChecked={countChecked} updateFilter={updateFilter} />
            <div className={styles.filter__order}>
                <div className={styles.order__select}>
                    <SelectField
                        options={sortOptions}
                        placeholder={"За замовчуванням"}
                        onChange={handleSortSelect}
                        selected={selectedSort || null}
                    />
                </div>
            </div>
            <SecondaryButton
                onClick={() => setFilterVisible(true)}
                additionalClasses={[styles.filter__button]}
            >
                <img src={FilterSVG} alt="" />
                {count > 0 ? `Фільтр (${count})` : "Фільтр"}
            </SecondaryButton>
        </div>
    );
}

export default Filter;