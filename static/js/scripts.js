document.addEventListener('DOMContentLoaded', function(){

    // плюс и минус для количества товаров
    let button_minus = document.getElementById('number-of-goods-minus');
    let button_plus = document.getElementById('number-of-goods-plus');
    let input = document.getElementById('number-of-goods-input');
    let button_add_to_basket = document.getElementById('add-to-basket')

    edit_button_data = function () {
        button_add_to_basket.setAttribute('data-count', input.value);
    }
    button_minus.addEventListener('click', function () {
        input.stepDown(1);
        edit_button_data();
    });
    button_plus.addEventListener('click', function () {
        input.stepUp(1)
        edit_button_data();

    });
    input.addEventListener('change',function (e) {
        edit_button_data();
    });

    // скрипт отвечает за выделение Цвета в модальном окне и за Сброс цвета
    var color_blocks = document.querySelectorAll(".color-target");
    let color_span = document.getElementById('selected-color')
    let selected_color;

    clear_color = function () {
        for (var j = 0; j < color_blocks.length; j++) {
                color_blocks[j].classList.remove("active");
            }
        color_span.textContent = '';
        button_add_to_basket.removeAttribute('data-color');
    }

    add_color = function (selected_color) {
            button_add_to_basket.setAttribute('data-color', selected_color);
            color_span.innerHTML = (selected_color + '<a class="ml-3 text-decoration-none text-danger" href="javascript:clear_color();">x</a>');
    }

    for (var i = 0; i < color_blocks.length; i++) {
        color_blocks[i].addEventListener("click", function () {
            clear_color();
            this.classList.add("active");
            add_color(this.lastChild.textContent)
        }, false);
    }


    // скрипт отвечает за смену изображений товара
    var main_image_link = document.getElementById('main-image').parentElement;
    var main_image = document.getElementById('main-image');
    var image_title = document.getElementById('image-title');
    var thumb_main_image = document.getElementById('thumb-main-image');

    var additional_images = document.querySelectorAll('.additional-images');
    for (var i = 0; i < additional_images.length; i++) {
        additional_images[i].addEventListener('click', function () {
            // меняем ссылки главной картинки
            var additional_images_link = this.parentElement
            main_image_link.href = additional_images_link.href;
            main_image_link.setAttribute("data-caption", additional_images_link.getAttribute("data-caption"))

            // добавляем в галерею главное изображение
            additional_images_link.classList.remove("big-additional-images");
            document.getElementById('thumb-main-image').parentElement.classList.add("big-additional-images");

            // меняем главную картинку
            main_image.src = this.src;
            image_title.textContent = this.alt;

            // убираем рамки у всех
            for (var j = 0; j < additional_images.length; j++) {
                additional_images[j].classList.remove("active")
            }

            // добавляем рамку
            this.classList.add("active");
        });
    }


    // скрипт отвечает за выбор опций в ценах
    select_input = function (price_id) {
        let input_price = document.getElementById(price_id)
        input_price.checked=true;
        let options_price = input_price.getAttribute('value');
        let price = input_price.getAttribute('data-price');
        button_add_to_basket.setAttribute('data-options-price', options_price);
        button_add_to_basket.setAttribute('data-price', price);
    }
});
