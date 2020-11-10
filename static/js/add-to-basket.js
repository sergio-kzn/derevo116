document.addEventListener('DOMContentLoaded', function () {
    // всплывающие окна при нажатии Добавить в корзину
    let toastElList = [].slice.call(document.querySelectorAll('.toast'))
    let toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    })

    // Добавляем товар в корзину при нажатии кнопки
    let button = document.getElementById('add-to-basket');
    button.addEventListener('click', async function () {
        // проверка выбор цвета
        if (button.hasAttribute('data-color-check') && !button.hasAttribute('data-color'))
            toastList[1].show();
        else {
            // отправляем ПОСТ на серевер, что бы обновить сессию //
            let color = "";
            let options_in_item = '';
            let price = 0;

            if (button.hasAttribute('data-color')) {
                color = button.getAttribute('data-color');
            }
            for (let i = 1; i <= button.getAttribute('data-max-options'); i++)
                if (button.hasAttribute('data-price-option-' + i)) {
                    let title_option = button.getAttribute('data-title-option-' + i)
                    let option = button.getAttribute('data-option-' + i)
                    options_in_item += title_option + ': ' + option + '<br>';
                    price += parseInt(button.getAttribute('data-price-option-' + i).replace(/\s+/g, ''), 10);
                }
            if (button.hasAttribute('data-price-product')) {
                price += parseInt(button.getAttribute('data-price-product').replace(/\s+/g, ''), 10);
            }
            let data = {
                'id': button.getAttribute("data-product-id"),
                'title': button.getAttribute("data-title"),
                'title_href': button.getAttribute('data-url'),
                'color': button.getAttribute('data-color'),
                'options': options_in_item,
                'count': button.getAttribute("data-count"),
                'price': price,
            };
            let response = await fetch('/cart/addtocart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                document.querySelector('#basket').innerHTML = await response.text();
                init_basket_modal();

                document.querySelector('.toast-body').innerHTML =
                    '<span class="font-weight-bolder mb-1" style="font-size: large">' + button.getAttribute("data-title") + '</span>' + '<br>'
                    + button.getAttribute("data-count") + ' шт. <br>'
                    + color + options_in_item + 'Цена: <b>' + price + ' &#x20bd;</b>';
                toastList[0].show();
            } else
                toastList[2].show();
        }
    })

    // функция удалить товар из корзины
    window.delete_item_from_basket = async function (key) {
        let response = await fetch('/cart/deletefromcart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({'key': key})
        });
        if (response.ok) {
            document.querySelector('#basket').innerHTML = await response.text();
            init_basket_modal(true);
        }
    };
})