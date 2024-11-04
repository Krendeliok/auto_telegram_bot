import React from 'react';
import styles from "./Contacts.module.css";

function Contact({ contact_data }) {
    return (  
        <div className={styles.text__contact}>
            <div className={styles.contact__title}>
                <img src={ contact_data.image } alt="" />
                {contact_data.title}
            </div>
            <div className={styles.contact__subtitle} dangerouslySetInnerHTML={{ __html: contact_data.body }}/>
        </div>
    );
}

export default Contact;