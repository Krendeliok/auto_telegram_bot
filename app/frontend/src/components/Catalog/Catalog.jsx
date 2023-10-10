import React from 'react';

import SecondaryButton from '../UI/SecondaryButton';
import CardList from './CardList';
import CatalogFilter from './CatalogFilter';

function Catalog({ lockBody }) {
    return (
        <div className="catalog" id="catalog">
            <div className="container">
                <div className="catalog__body">
                    <div className="catalog__header">
                        <div className="catalog__title block-title">Авто в наявності</div>
                        <CatalogFilter />
                    </div>
                    <div className="catalog__content">
                        <CardList lockBody={lockBody} />
                        <SecondaryButton additionalClasses={["more-cars__button"]}>Більше авто<span>{'>>'}</span></SecondaryButton>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Catalog;