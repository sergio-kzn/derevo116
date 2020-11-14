document.addEventListener('DOMContentLoaded', function () {
    // маска для ввода телефона
    function setCursorPosition(pos, elem) {
        elem.focus();
        if (elem.setSelectionRange) elem.setSelectionRange(pos, pos);
        else if (elem.createTextRange) {
            var range = elem.createTextRange();
            range.collapse(true);
            range.moveEnd("character", pos);
            range.moveStart("character", pos);
            range.select()
        }
    }

    function mask(event) {
        var matrix = "+7 (___) ___ ____",
            i = 0,
            def = matrix.replace(/\D/g, ""),
            val = this.value.replace(/\D/g, "");
        if (def.length >= val.length) val = def;
        this.value = matrix.replace(/./g, function (a) {
            return /[_\d]/.test(a) && i < val.length ? val.charAt(i++) : i >= val.length ? "" : a
        });
        if (event.type === "blur") {
            if (this.value.length === 2) this.value = ""
        } else setCursorPosition(this.value.length, this)
    }

    var input = document.querySelector("#delivery_phone");
    var input2 = document.querySelector("#pickup_phone");
    input.addEventListener("input", mask, false);
    input.addEventListener("focus", mask, false);
    input.addEventListener("blur", mask, false);
    input2.addEventListener("input", mask, false);
    input2.addEventListener("focus", mask, false);
    input2.addEventListener("blur", mask, false);


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
        if ((document.querySelector('input[name=deliveryRadio]:checked').id === 'radioDelivery' && delivery_phone.value.length > 7) ||
        (document.querySelector('input[name=deliveryRadio]:checked').id === 'radioPickup' && pickup_phone.value.length > 7))

        {
            document.querySelector('#delivery_phone').classList.remove('border-danger')
            document.querySelector('#pickup_phone').classList.remove('border-danger')

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
        } else {
            document.querySelector('#delivery_phone').classList.add('border-danger')
            document.querySelector('#pickup_phone').classList.add('border-danger')
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

        let orderDeliveryCountryAndCity = "";
        let orderDeliveryAddress = "";
        let orderDeliveryContact = "";
        let orderDeliveryContactPhone;
        if (document.querySelector('input[name=deliveryRadio]:checked').id === 'radioDelivery') {
            orderDeliveryCountryAndCity = delivery_country.value + ', ' + delivery_city.value + ', ' + delivery_index.value;
            orderDeliveryAddress = delivery_street.value;
            orderDeliveryContact = delivery_fio.value;
            orderDeliveryContactPhone = delivery_phone.value;
        } else {
            orderDeliveryContact = pickup_fio.value;
            orderDeliveryContactPhone = pickup_phone.value;
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