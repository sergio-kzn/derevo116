document.addEventListener('DOMContentLoaded', function () {

    // плюс и минус для количества товаров
    let button_minus = document.getElementById('number-of-goods-minus');
    let button_plus = document.getElementById('number-of-goods-plus');
    let input = document.getElementById('number-of-goods-input');
    let button_add_to_basket = document.getElementById('add-to-basket')

    let edit_button_data = function () {
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
    input.addEventListener('change', function () {
        edit_button_data();
    });

    // скрипт отвечает за выделение Цвета в модальном окне и за Сброс цвета
    let color_blocks = document.querySelectorAll(".color-target");
    let color_span = document.getElementById('selected-color')

    window.clear_color = function () {
        for (let j = 0; j < color_blocks.length; j++) {
            color_blocks[j].classList.remove("active");
        }
        color_span.textContent = '';
        button_add_to_basket.removeAttribute('data-color');
    }

    let add_color = function (selected_color) {
        button_add_to_basket.setAttribute('data-color', selected_color);
        color_span.innerHTML = (selected_color +
            '<span class="ml-3 text-decoration-none text-danger" style="cursor: pointer" onclick="clear_color();">x</span>');
    }

    for (let i = 0; i < color_blocks.length; i++) {
        color_blocks[i].addEventListener("click", function () {
            clear_color();
            this.classList.add("active");
            add_color(this.lastChild.textContent)
        }, false);
    }


    // скрипт отвечает за смену дополнительных изображений товара
    let image_title = document.getElementById('image-title');
    let main_image_img = document.getElementById('main-image');
    let thumb_images_img = document.querySelectorAll('.additional-images');
    let index = 0;

    for (let i = 0; i < thumb_images_img.length; i++) {
        thumb_images_img[i].addEventListener('click', function () {
            let thumb_active_img = this;

            // меняем большое изображение
            main_image_img.src = thumb_active_img.src;
            main_image_img.alt = thumb_active_img.alt
            image_title.textContent = main_image_img.alt;

            // убираем рамки у всех
            for (let j = 0; j < thumb_images_img.length; j++) {
                thumb_images_img[j].classList.remove("active")
            }
            // добавляем рамку
            this.classList.add("active");

            index = i;

        });
    }
    // создаем fancybox, открывая ее с определенной картинки
    main_image_img.addEventListener('click', function () {
        $.fancybox.open(
            $('.thumb-images'), {
                loop: true,
                index: index,
            });
        });


// скрипт отвечает за выбор опций в ценах
        window.select_input = function (price_id, option_id) {
            let input_price = document.getElementById(price_id)
            input_price.checked = true;

            let title_option = input_price.getAttribute('data-title-option-' + option_id);
            let option = input_price.getAttribute('data-option-' + option_id);
            let price_option = input_price.getAttribute('data-price-option-' + option_id);
            button_add_to_basket.setAttribute('data-title-option-' + option_id, title_option);
            button_add_to_basket.setAttribute('data-option-' + option_id, option);
            button_add_to_basket.setAttribute('data-price-option-' + option_id, price_option);
        }
    })
    ;
