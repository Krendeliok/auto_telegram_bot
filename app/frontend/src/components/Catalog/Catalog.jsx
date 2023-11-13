import React, { useState, useEffect, useCallback } from 'react';

import SecondaryButton from '../UI/SecondaryButton';
import CardList from './CardList';
import CatalogFilter from './CatalogFilter';

import { useFetching } from '../../hooks/useFetching';
import AdvertisementService from '../../API/AdvertisementService';
import FilterObject from './Filter/FilterObject';

const limit = 3;
    

function Catalog({ lockBody }) {
    const [cards, setCards] = useState([])
    const [page, setPage] = useState(1);

    const [maxCards, setMaxCards] = useState(0)

    const [filter, setFilter] = useState(new FilterObject())
    const [sort, setSort] = useState('default');
    const [fetchCards, cardsLoading] = useFetching(async () => {
        const response = await AdvertisementService.getAll(filter, limit, page);
        setMaxCards(response.headers["x-total-count"])
        setCards([...response.data]);
    })

    const handleMoreCars = () => {
        if (limit * page < maxCards) {
            setPage((prev) => prev + 1)
        }
    }

    useEffect(() => {
        filter.sort_by = sort;
        fetchCards();
    }, [page, filter.fields, sort])

    const countChecked = useCallback(() => {
        let res = 0;
        filter.fields.forEach(val => {
            if (val.list) {
                res += val.list.length;
            }
        })
        return res;
    }, [filter.fields])

    return (
        <div className="catalog" id="catalog">
            <div className="container">
                <div className="catalog__body">
                    <div className="catalog__header">
                        <div className="catalog__title block-title">Авто в наявності</div>
                        <CatalogFilter countChecked={countChecked} setFilter={setFilter} setSort={setSort} sort={sort} />
                    </div>
                    <div className="catalog__content">
                        <CardList lockBody={lockBody} cards={cards} cardsLoading={cardsLoading} />
                        <div className="catalog__buttons">
                            <SecondaryButton onClick={handleMoreCars} additionalClasses={["more-cars__button"]}>Більше авто<span>{'>>'}</span></SecondaryButton>
                            {page >= 2 &&
                                <>
                                    <div className='hide__last' onClick={() => setPage((prev) => prev - 1)}>Приховати</div>
                                    <div className="hide__all" onClick={() => setPage(1)}>Приховати усі авто</div>
                                </>
                            }
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Catalog;