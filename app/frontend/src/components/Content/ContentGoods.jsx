import React from 'react';
import Good from './Good';
import styles from "./Content.module.css";

function ContentGoods() {
    const cards = [
        { number: "01", title: "Купівля", body: "Підбір якісного авто без зайвих ризиків та трати Вашого часу" },
        { number: "02", title: "Продаж", body: "Миттєвий продаж або викуп авто за найкращою ціною" },
        { number: "03", title: "Оренда", body: "Відчуй свободу у пересуванні вже сьогодні" },
        { number: "04", title: "Кредит", body: "Все просто: купуй сьогодні – плати завтра" },
    ]

    return ( 
        <div className={styles.content__goods}>
            {cards.map(good_data => 
                <Good good_data={good_data} key={good_data.number} />
            )}
        </div>
     );
}

export default ContentGoods;