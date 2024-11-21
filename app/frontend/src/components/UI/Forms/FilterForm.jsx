import React, { useEffect, useState } from 'react';
import { useFetching } from '../../../hooks/useFetching';

import ProducersService from '../../../API/ProducersService';
import FuelService from '../../../API/FuelService';
import GearboxService from '../../../API/GearboxService';

import RangedField from './Fields/RangedField';
import CheckBoxGroup from './Inputs/CheckBoxGroup'

import useFormCheckboxGroup from "../../../hooks/useFormCheckboxGroup";
import useFormRangedField from '../../../hooks/useFormRangedField';
import ChosenItems from './Fields/ChosenItems';
import FilterObject from '../../Catalog/Filter/FilterObject';
import AdvertisementService from '../../../API/AdvertisementService';

import styles from './Forms.module.css';
import SecondaryButton from "../SecondaryButton";
import FilterItem from "./Fields/FilterItem";


const addCheckedFieldToObject = (obj, defaultChecked = false) => {
    const newObj = obj.map((val) => {
        const obj = { ...val, checked: defaultChecked }
        return obj;
    })
    return newObj;
}

function FilterForm({ sendFilter }) {
    const [setProducers, producers, getCheckedProducers] = useFormCheckboxGroup();
    const [fetchProducers] = useFetching(async () => {
        const response = await ProducersService.getAll();
        setProducers(addCheckedFieldToObject(response.data));
    })

    const [setFuels, fuels, getCheckedFuels] = useFormCheckboxGroup();
    const [fetchFuels] = useFetching(async () => {
        const response = await FuelService.getAll();
        setFuels(addCheckedFieldToObject(response.data));
    })

    const [setGearboxes, gearboxes, getCheckedGearboxes] = useFormCheckboxGroup();
    const [fetchGearboxes] = useFetching(async () => {
        const response = await GearboxService.getAll();
        setGearboxes(addCheckedFieldToObject(response.data));
    })

    const [getPrice, price] = useFormRangedField(0, 1000000, 1);
    const [fetchMaxPrice] = useFetching(async () => {
        const response = await AdvertisementService.getMaxPrice();
    })
    const [getYear, year] = useFormRangedField(1975, 2023, 1);
    const [getRange, range] = useFormRangedField(0, 999, 1);
    const [getEngineVolume, engine_volume] = useFormRangedField(0.1, 250, 0.1);

    const createFilter = () => {
        return new FilterObject(
            getCheckedProducers(),
            getCheckedGearboxes(),
            getCheckedFuels(),
            getPrice(),
            getYear(),
            getRange(),
            getEngineVolume(),
        );
    }

    useEffect(() => {
        fetchProducers();
        fetchFuels();
        fetchGearboxes();
        fetchMaxPrice();
        sendFilter(createFilter());
    }, [])

    const onSubmit = (e) => {
        e.preventDefault();
        const filter = createFilter()
        sendFilter(filter);
    }

    return (
        <form onSubmit={onSubmit}>
            <div className={[styles.inputs, styles.row].join(" ")}>
                <div className={styles.form__checkboxes}>
                    <div className={styles.column}>
                        <FilterItem title={"Марка"}>
                            <CheckBoxGroup groupName={"producers"} {...producers} />
                        </FilterItem>
                    </div>
                    <div className={styles.column}>
                        <FilterItem title={"Паливо"}>
                            <CheckBoxGroup groupName={"fuels"} {...fuels} />
                        </FilterItem>
                        <FilterItem title={"Коробка передач"}>
                            <CheckBoxGroup groupName={"gearboxes"} {...gearboxes} />
                        </FilterItem>
                        </div>
                </div>
                <div className={styles.form__ranged}>
                    <FilterItem title={"Ціна"}>
                        <RangedField name={'price'} measurement={"$"} {...price} />
                    </FilterItem>
                    <FilterItem title={"Рік випуску"}>
                        <RangedField name={'year'} measurement={"рік"} {...year} />
                    </FilterItem>
                    <FilterItem title={"Пробіг"}>
                        <RangedField name={'range'} measurement={"т. км"} {...range} />
                    </FilterItem>
                    <FilterItem title={"Об'єм двигуна/Потужність"}>
                        <RangedField name={'engine_volume'} measurement={"л/кВт"} {...engine_volume} isFloat={true}/>
                    </FilterItem>
                </div>
            </div>
            <div className={styles.saveAndChosen}>
                <SecondaryButton type="submit" additionalClasses={[styles.popup__button]}>Зберегти</SecondaryButton>
                <ChosenItems items={[producers, fuels, gearboxes]} />
            </div>
            
        </form>
    );
}

export default FilterForm;