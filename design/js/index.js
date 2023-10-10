$(document).ready(function () {
    var body = $("body");

    $(".header__burger").click(function (event) {
        $(".header__burger,.header__menu").toggleClass("active");
        body.toggleClass("lock");
    });

    $(".more-info__button").click(function (event) {
        body.append(getPopup("Залишилися питання?", "Напишіть нам свій номер телефону і ми Вам зателефонуємо протягом 30 хвилин."));
        body.addClass("lock");
        $(".popup__close").click(function (event) {
            closePopup($(".popup__wrapper"));
        })
        document.addEventListener('click', (e) => { // Вешаем обработчик на весь документ
            if (e.target === document.querySelector(".popup__wrapper")) { // Если цель клика - фот, то:
                closePopup($(".popup__wrapper"));
            }
        })
    });

    function closePopup(popup) {
        popup.remove();
        body.removeClass("lock");
    }

    $("")
});


function getPopup(title, subtitle) {
    return `<div class="popup__wrapper">
        <div class="popup__container">
            <div class="popup__body">
                <div class="popup__text">
                    <div class="popup__title">${title}</div>
                    <div class="popup__subtitle">${subtitle}</div>
                </div>
                <div class="popup__form">
                    <form action="">
                        <div class="inputs">
                            <div class="input__group">
                                <label for="name">Ім’я</label>
                                <input id="name" name="name" type="text" placeholder="Олексій">
                            </div>

                            <div class="input__group">
                                <label for="phone">Телефон</label>
                                <input id="phone" name="phone" type="tel" pattern="+38 [0][0-9]{2} [0-9]{3}-[0-9]{2}-[0-9]{2}" placeholder="+38 (000) 000-00-00">
                            </div>
                        </div>
                        <button type="submit" class="popup__button secondary__button">Надіслати</button>
                    </form>
                </div>
            </div>
            <div class="popup__close _icon-close"></div>
        </div>
    </div>`
}