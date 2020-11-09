document.addEventListener('DOMContentLoaded', function () {

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