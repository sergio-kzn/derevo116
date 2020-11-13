document.addEventListener('DOMContentLoaded', function () {

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
            location.reload();
        }
    };

    const collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
    const collapseList = collapseElementList.map(function (collapseEl) {
        return new bootstrap.Collapse(collapseEl, {
            toggle: false
        })
    })

    radioPickup.onchange = function () { // я сам заберу заказ
        let radio = document.querySelectorAll('#collapsePickup input');
        radio[0].checked = true;

        collapseList[0].show();
        collapseList[1].hide();
        collapseList[2].hide();
        radioPickup.scrollIntoView({
            block: "start",
            behavior: "smooth",
        })
    }
    radioDelivery.onchange = function () { // Мне нужна доставка
        let radio = document.querySelectorAll('#collapseDelivery input');
        radio[0].checked = true;

        collapseList[0].hide();
        collapseList[1].show();
        collapseList[2].hide();
        radioPickup.scrollIntoView({
            block: "start",
            behavior: "smooth",
        })
    }

    // функция составляет варианты оплаты, в зависимости от доставки
    let payment_view = async function () {
        let orderDeliveryWay = document.querySelector('input[name=deliveryWay]:checked').getAttribute('data-api')
        let response = await fetch('/cart/select_payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify({'orderDeliveryWay': orderDeliveryWay})
        });
        if (response.ok) {
            document.querySelector('#collapsePickupPayment').innerHTML = await response.text()
            collapseList[2].show();
            collapseList[1].hide();
            collapseList[0].hide();
            radioPickup.scrollIntoView({
                block: "start",
                behavior: "smooth",
            })
        }

    }

    collapsePickupPaymentButton.onclick = function () { // я сам заберу заказ - Перейти к оплате
        payment_view()
    }
    collapseDeliveryPaymentButton.onclick = function () {  // Мне нужна доставка - Перейти к оплате
        payment_view()
    }


    // Подтверждение заказа
    window.confirmOrder = async function (link) {
        let orderComment = comment.value;
        let orderDelivery = document.querySelector('input[name=deliveryRadio]:checked').labels[0].textContent.trim();
        let orderDeliveryWay = document.querySelector('input[name=deliveryWay]:checked').getAttribute('data-api');
        let orderDeliveryWayText = document.querySelector('#delivery-other-text').value;

        let orderPay = document.querySelector('input[name=payment]:checked').getAttribute('data-api');

        let orderDeliveryCountryAndCity;
        let orderDeliveryAddress;
        let orderDeliveryContact;
        let orderDeliveryContactPhone;
        if (document.querySelector('input[name=deliveryRadio]:checked').id === 'radioDelivery') {
            orderDeliveryCountryAndCity = delivery_country.value + ', ' + delivery_city.value + ', ' + delivery_index.value;
            orderDeliveryAddress = delivery_street.value;
            orderDeliveryContact = delivery_fio.value;
            orderDeliveryContactPhone = delivery_phone.value;
        }

        let data = {
            'orderComment': orderComment,
            'orderDelivery': orderDelivery,
            'orderDeliveryWay': orderDeliveryWay,
            'orderDeliveryWayText': orderDeliveryWayText,
            'orderPay': orderPay,
            'orderDeliveryCountryAndCity': orderDeliveryCountryAndCity,
            'orderDeliveryAddress': orderDeliveryAddress,
            'orderDeliveryContact': orderDeliveryContact,
            'orderDeliveryContactPhone': orderDeliveryContactPhone,
        }

        let response = await fetch(link, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            location.href = link
        }

    }
})