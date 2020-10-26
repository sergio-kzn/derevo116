document.addEventListener('DOMContentLoaded', function () {
    let button = document.getElementById('add-to-basket');
    let ul = document.getElementById('basket-list')
    let basket_count = 0;
    let basket_sum = 0;

    button.addEventListener('click', function () {
        let li = document.createElement('li');
        li.classList.add('list-group-item', 'list-group-item-action', 'px-1');

        let div_title = document.createElement('div');
        let title = button.getAttribute("data-title");
        let a_title = document.createElement('a');
        let a_url = button.getAttribute('data-url');
        div_title.classList.add('basket-list-title-item', 'd-flex', 'justify-content-between');
        a_title.classList.add('text-decoration-none', 'text-dark');
        a_title.href = a_url;
        a_title.textContent = title;

        let span_count = document.createElement('span');
        let count = button.getAttribute("data-count");
        span_count.classList.add('badge', 'bg-primary', 'rounded-pill', 'basket-list-count', 'h-25');
        span_count.textContent = count;

        let div_options = document.createElement('div');
        div_options.classList.add('basket-list-options', 'text-muted', 'small', 'd-flex', 'justify-content-between', 'align-items-center')

        let div_color = document.createElement('div');
        div_color.classList.add('basket-list-color');
        let color = "";
        let options_price = '';
        let price = '';
        if (button.hasAttribute('data-color')) {
            color = 'Цвет: ' + button.getAttribute('data-color') + '<br>';
        }
        if (button.hasAttribute('data-options-price')) {
            let options_price_title = button.getAttribute('data-option-name')
            options_price = options_price_title + ': ' + button.getAttribute('data-options-price') + '<br>';
        }
        if (button.hasAttribute('data-price')) {
            price = '<span><b>' + button.getAttribute('data-price') + ' &#x20bd;</b></span>';
        }
        div_color.innerHTML = color + options_price + price;

        a_delete = document.createElement("span");
        a_delete.classList.add('btn', 'btn-outline-danger', 'btn-sm', 'delete_from_basket');
        a_delete.setAttribute('role', 'button');
        a_delete.textContent = ' x ';

        div_title.appendChild(a_title);
        div_title.appendChild(span_count);
        div_options.appendChild(div_color);
        div_options.appendChild(a_delete);
        li.appendChild(div_title);
        li.appendChild(div_options);
        ul.appendChild(li);

        // кнопка удалить
        let delete_buttons = document.querySelectorAll('.delete_from_basket')
        for (var i = 0; i < delete_buttons.length; i++) {
            delete_buttons[i].addEventListener('click', function () {
                let current_li = this.parentElement.parentElement;
                let current_price = parseInt(this.previousSibling.lastChild.innerText.replace(/\s+/g, ''), 10)
                let current_count = parseInt(this.parentElement.previousSibling.lastChild.innerText, 10);

                current_li.classList.add('d-none');
                basket_count -= 1;
                basket_sum -= current_price * current_count;

                update_count_and_price(basket_count, basket_sum)
            });
        }

        //обновляем количество товаров и сумму всех товаров
        let li_empty = document.getElementById('empty-basket');
        update_count_and_price = function (count, sum) {
            let span_basket_count = document.getElementById("basket-count");
            let span_basket_sum = document.getElementById("basket-sum");
            let span_basket_sum_footer = document.getElementById("basket-sum-footer");

            if (count < 1) li_empty.classList.remove('d-none');
            span_basket_count.textContent = count;
            span_basket_sum.textContent = sum;
            span_basket_sum_footer.innerHTML = 'Сумма: ' + sum + ' &#x20bd;';
        }

        basket_count += 1;
        basket_sum += parseInt(button.getAttribute('data-price').replace(/\s+/g, ''), 10) * parseInt(count, 10);
        update_count_and_price(basket_count, basket_sum)

        li_empty.classList.add('d-none')
    })
})