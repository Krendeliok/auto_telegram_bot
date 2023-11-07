export default function addCheckedFieldToObject(obj, defaultChecked = false) {
    const newObj = obj.map((val) => {
        const obj = { ...val, checked: defaultChecked }
        return obj;
    })
    return newObj;
};
