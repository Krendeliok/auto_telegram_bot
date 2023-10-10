import React, { useState } from 'react';
import PhoneInput from 'react-phone-number-input/input'
import 'react-phone-number-input/style.css'

function AboutCarForm({ advertisement_id, setVisiblePopup }) {
    const [formData, setFormData] = useState({ name: "", phone: "" });
    const sendNeedFeedback = (e) => {
        e.preventDefault();
        console.log(formData);
        setFormData({ name: "", phone: "" });
        setVisiblePopup(false);
    };

    return (  
        <form action="">
            <div className="inputs">
                <div className="input__group">
                    <label htmlFor="name">Ім’я</label>
                    <input
                        id="name"
                        name="name"
                        type="text"
                        placeholder="Олексій"
                        value={formData.name}
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
                        defaultCountry="UA"
                        value={formData.phone}
                        onChange={v => setFormData({ ...formData, phone: v })}
                    />
                </div>
            </div>
            <input type="hidden" name='advertisement_id' value={advertisement_id}/>
            <button type="submit" className="popup__button secondary__button" onClick={sendNeedFeedback}>Надіслати</button>
        </form>
    );
}

export default AboutCarForm;