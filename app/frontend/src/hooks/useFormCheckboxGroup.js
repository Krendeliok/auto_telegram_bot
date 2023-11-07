import { useState, useCallback } from "react";

const checkCheckboxes = (id, list) => {
    const newlist = list.map((el) => {
        if (el.id == id) {
            return { ...el, checked: !el.checked };
        }
        return el;
    })
    return newlist;
}

const useFormCheckboxGroup = (initialValue = []) => {
    const [checkboxList, setCheckboxList] = useState(initialValue);
    const onClick = useCallback((id) => setCheckboxList((prev) => checkCheckboxes(id, prev)), []);
    const getChecked = useCallback(() => checkboxList.filter((val) => val.checked), [checkboxList]);
    return [setCheckboxList, { checkboxList, onClick }, getChecked ];
};

export default useFormCheckboxGroup;