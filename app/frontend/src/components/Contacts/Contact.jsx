import React from 'react';

function Contact({ contact_data }) {
    return (  
        <div className="text__contact">
            <div className={["contact__title", contact_data.icon_class].join(" ")}>{contact_data.title}</div>
            <div className="contact__subtitle" dangerouslySetInnerHTML={{ __html: contact_data.body }}/>
        </div>
    );
}

export default Contact;