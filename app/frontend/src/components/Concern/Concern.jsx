import React from 'react';
import ConcernItem from './ConcernItem';

function Concern() {
    const items = [
        {
            id: 1,
            title: "Відмінне місце розташування",
            body: "Майданчик розташований на місці, де понад 30 років знаходився автобазар на окружній дорозі в с.Кінчеш."
        },
        {
            id: 2,
            title: "Швидкий продаж автомобіля",
            body: "Завдяки широкому потоку потенційних покупців, зацікавлених у придбанні автомобілей різних марок."
        },
        {
            id: 3,
            title: "Цілодобова охорона та відеонагляд",
            body: "Впевненість у безпеці Вашої автівки для нас є найвищим пріоритетом."
        },
        {
            id: 4,
            title: "Безкоштовна реклама для авто",
            body: "Публікація оголешення про продаж Вашого автомобіля у наших соціальніх мережах та на сайті."
        },
    ]

    return (
        <div className="concern">
            <div className="container">
                <div className="concern__title block-title">До нас варто заїхати, якщо Вас цікавить:</div>
                <div className="concern__content">
                    {items.map(item => 
                        <ConcernItem item_data={item} key={item.id}/> 
                    )}
                </div>
            </div>
        </div>
    );
}

export default Concern;