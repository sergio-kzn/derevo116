document.addEventListener('DOMContentLoaded', function () {
    // Показать Корзину
    window.init_basket_modal = function (show = false) {
        let basket_modal = new bootstrap.Modal(document.querySelector('#basket-modal'), {})
        let cart = document.getElementById('cart')
        cart.addEventListener('click', function () {
            basket_modal.show();
        })
        if (show === true) {
            document.querySelector('.modal-backdrop').remove();
            basket_modal.show();
        }
    }
    init_basket_modal();
})