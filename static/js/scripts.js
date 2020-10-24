document.addEventListener('DOMContentLoaded', function(){
    // плюс и минус для количества товаров
    let button_minus = document.getElementById('number-of-goods-minus');
    let button_plus = document.getElementById('number-of-goods-plus');
    let input = document.getElementById('number-of-goods-input');

    button_minus.addEventListener('click', function (){input.stepDown(1)});
    button_plus.addEventListener('click', function (){input.stepUp(1)});
});
