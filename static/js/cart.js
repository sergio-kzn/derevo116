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

    radioPickup.onchange = function () {
        collapseList[0].show();
        collapseList[1].hide();
        collapseList[2].hide();
        collapseList[3].hide();
    }
    radioDelivery.onchange = function () {
        collapseList[0].hide();
        collapseList[1].show();
        collapseList[2].hide();
        collapseList[3].hide();
    }
    collapsePickupPaymentButton.onclick = function () {
        collapseList[3].hide();
        collapseList[2].show();
        collapseList[1].hide();
        collapseList[0].hide();

    }
    collapseDeliveryPaymentButton.onclick = function () {
        collapseList[3].show();
        collapseList[2].hide();
        collapseList[1].hide();
        collapseList[0].hide();

    }
})