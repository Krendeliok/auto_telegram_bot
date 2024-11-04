import React from 'react';

import DoneSVG from "../../assets/done.svg"
import styles from "./About.module.css";

function AboutList() {
    const items = [
        "Продаж авто",
        "Підбір авто",
        "Оренда авто",
        "Кредит",
        "Лізінг",
        "Передпродажне ТО",
        "Регулярне ТО",
        "Оформлення договору куплі-продажу",
        "Перевірка ЛКП",
        "Малярно-рехтовочні роботи",
        "Підбір автозапчастин",
        "Доставка авто в будь-який регіон Ураїни",
        "Пригон авто під замовлення з Європи, США, Канади, Китаю",
    ]

    return ( 
        <div className={styles.contentSubtitle__list}>
            <ul>
                {items.map((item, index) =>  
                    <li key={index}>
                        <img src={DoneSVG} alt="" />
                        {item}
                    </li>
                )}
            </ul>
        </div>
     );
}

export default AboutList;