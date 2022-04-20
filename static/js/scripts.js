function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {   //выстраиваем заголовок
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json()) // полученный ответ от сервера преобразуем в json
        .then(json => render(json))         // json передаем в функцию render
        .catch(error => console.error(error))  // если произойдет ошибка выведем в консоль
}

// Filter movies
const forms = document.querySelector('form[name=filter]');  // ищем форму с именем filter

forms.addEventListener('submit', function (e) {  // когда будет запущен submit выполняем функцию
    // Получаем данные из формы
    e.preventDefault();      // блокируем дефолтное поведение формы по отправке данных
    let url = this.action;      // переменной url присваиваем значение параметра action нашей формы
    let params = new URLSearchParams(new FormData(this)).toString();  // берем все данные формы и преобразовываем в строку
    ajaxSend(url, params);  // передаем параметры в ajaxSend
});

function render(data) {     //принимает json
    // Рендер шаблона
    let template = Hogan.compile(html);  // с помощью библиотеки Hogan компилируем html, html это переменная ниже
    let output = template.render(data);  // Рендерим полученный шаблон со всей вставленной информацией

    const div = document.querySelector('.left-ads-display>.row');  // находим див в который вставляются блоки с фильмами
    div.innerHTML = output;  // и вставляем в него полученный результат
}
// в цикл {{#movies}} вставлен кусок html кода для отображения одного фильма
let html = '\
{{#movies}}\
    <div class="col-md-4 product-men">\
        <div class="product-shoe-info editContent text-center mt-lg-4">\
            <div class="men-thumb-item">\
                <img src="media/{{ poster }}" class="img-fluid" alt="">\
            </div>\
            <div class="item-info-product">\
                <h4 class="">\
                    <a href="/{{ url }}" class="editContent">{{ title }}</a>\
                </h4>\
                <div class="product_price">\
                    <div class="grid-price">\
                        <span class="money editContent">{{ tagline }}</span>\
                    </div>\
                </div>\
                <ul class="stars">\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-half-o" aria-hidden="true"></span></a></li>\
                    <li><a href="#"><span class="fa fa-star-o" aria-hidden="true"></span></a></li>\
                </ul>\
            </div>\
        </div>\
    </div>\
{{/movies}}'


// Add star rating
const rating = document.querySelector('form[name=rating]');

rating.addEventListener("change", function (e) {
    // Получаем данные из формы
    let data = new FormData(this);
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
        .then(response => alert("Рейтинг установлен"))
        .catch(error => alert("Ошибка"))
});