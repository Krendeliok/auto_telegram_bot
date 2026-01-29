import React, { useState } from 'react';
import PhoneInput from 'react-phone-number-input/input'
import 'react-phone-number-input/style.css'

import { useFetching } from '../../../hooks/useFetching';
import FeedbackService from '../../../API/FeedbackService';

function FeedbackForm({ setVisiblePopup }) {
    const [formData, setFormData] = useState({ name: "", phone: "" });
    const [fetchFeedback] = useFetching(async () => {
        await FeedbackService.create({...formData});
    })
    const sendNeedFeedback = (e) => {
        e.preventDefault();
        fetchFeedback();
        setFormData({ name: "", phone: "" });
        setVisiblePopup(false);
    };

    return (  
        <form>
            <div className="inputs">
                <div className="input__group">
                    <label htmlFor="name">Ім’я</label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        placeholder="Олексій"
                        value={formData.name}
                        required
                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                    />
                </div>
                <div className="input__group">
                    <label htmlFor="phone">Телефон</label>
                    <PhoneInput
                        id="phone"
                        name="phone"
                        country="UA"
                        international={true}
                        withCountryCallingCode={true}
                        value={formData.phone}
                        required
                        onChange={v => setFormData({ ...formData, phone: v })}
                    />
                </div>
            </div>
            <button type="submit" className="popup__button secondary__button" onClick={sendNeedFeedback}>Надіслати</button>
        </form>
    );
}

export default FeedbackForm;