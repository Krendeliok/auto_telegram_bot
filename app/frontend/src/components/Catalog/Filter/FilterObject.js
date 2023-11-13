export class FilterList {
    constructor(list, name) {
        this.list = list;
        this.name = name;
    }

    asDict() {
        let obj = {};
        obj[this.name] = this.list.map((v) => v.id).join(",");
        return obj
    }
}

export class FilterRange {
    constructor(range, name) {
        this.range = range;
        this.name = name;
    }

    asDict() {
        let obj = {}
        obj[`${this.name}_min`] = this.range.min;
        obj[`${this.name}_max`] = this.range.max;
        return obj
    }
}

class FilterObject {
    constructor(
            producers = [],
            gearboxes = [],
            fuels = [],
            price = { min: 0, max: 0 },
            year = { min: 0, max: 0 },
            range = { min: 0, max: 0 },
            engine_volume = { min: 0, max: 0 },
            sort_by = "default"
    ) {
        this.fields = [
            new FilterList(producers, '_producers'),
            new FilterList(fuels, '_fuels'),
            new FilterList(gearboxes, '_gearboxes'),
            new FilterRange(price, "_price"),
            new FilterRange(year, "_year"),
            new FilterRange(range, "_range"),
            new FilterRange(engine_volume, "_engine_volume"),
        ]
        this.sort_by = sort_by;
    }

    asDict() {
        let res = {};
        this.fields.forEach(val => Object.assign(res, val.asDict()));
        res._sort_by = this.sort_by;
        return res;
    }
}

export default FilterObject;