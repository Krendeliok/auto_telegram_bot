import React, { useState, useEffect, useCallback } from 'react';

import SecondaryButton from '../UI/SecondaryButton';
import CardList from './CardList';
import Filter from './Filter/Filter';

import { useFetching } from '../../hooks/useFetching';
import AdvertisementService from '../../API/AdvertisementService';
import FilterObject from './Filter/FilterObject';
import styles from "./Catalog.module.css";

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
        <div id="catalog">
            <div className="container">
                <div className={styles.catalog__body}>
                    <div className={styles.catalog__header}>
                        <div className={[styles.catalog__title, "block-title"].join(" ")}>Авто в наявності</div>
                        <Filter countChecked={countChecked} setFilter={setFilter} setSort={setSort} sort={sort} />
                    </div>
                    <div className={styles.catalog__content}>
                        <CardList lockBody={lockBody} cards={cards} cardsLoading={cardsLoading} />
                        <div className={styles.catalog__buttons}>
                            <SecondaryButton onClick={handleMoreCars} additionalClasses={[styles.moreCars__button]}>Більше авто<span>{'>>'}</span></SecondaryButton>
                            {page >= 2 &&
                                <>
                                    <div className={styles.hide__last} onClick={() => setPage((prev) => prev - 1)}>Приховати</div>
                                    <div className={styles.hide__all} onClick={() => setPage(1)}>Приховати усі авто</div>
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