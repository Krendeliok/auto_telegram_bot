import React from 'react';

import SecondaryButton from '../UI/SecondaryButton';

function CatalogFilter() {
    return (
        <div className="catalog__filter">
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
            <SecondaryButton additionalClasses={["filter__button", "_icon-filter"]}>Фільтр</SecondaryButton>
        </div>
    );
}

export default CatalogFilter;