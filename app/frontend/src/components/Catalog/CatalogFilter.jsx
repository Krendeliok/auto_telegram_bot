import React, { useEffect, useState } from 'react';

import FilterPopup from '../Popup/FilterPopup'
import SecondaryButton from '../UI/SecondaryButton';

import bodySetLock from '../../utils/lockBody';

function CatalogFilter({ countChecked, setFilter }) {
    const count = countChecked();
    const [filterVisible, setFilterVisible] = useState(false);
    useEffect(() => {
        bodySetLock(filterVisible);
    }, [filterVisible])

    const updateFilter = (filter) => {
        setFilterVisible(false);
        setFilter(filter);
    }

    return (
        <div className="catalog__filter">
            <FilterPopup visible={filterVisible} setVisible={setFilterVisible} countChecked={countChecked} updateFilter={updateFilter} />
            <div className="filter__order">
                <button className="order__toogle-order _icon-sort"></button>
                <div className="order__select">
                    <select>
                        <option value="default">За замовчуванням</option>
                        <option value="cheapest">Від дешевих до дорогих</option>
                        <option value="expensive">Від дорогих до дешевих</option>
                        <option value="new">Спочатку нові</option>
                    </select>
                </div>
            </div>
            <SecondaryButton onClick={() => setFilterVisible(true)} additionalClasses={["filter__button", "_icon-filter"]}>{count > 0 ? `Фільтр (${count})` : "Фільтр" }</SecondaryButton>
        </div>
    );
}

export default CatalogFilter;