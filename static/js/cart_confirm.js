document.addEventListener('DOMContentLoaded', function () {
    // Подтверждение заказа
    window.sendOrder = async function (link) {
        let call_me = 0;
        if (order_call_me.checked)
            call_me = 1;

        let notification = 0;
        if (order_notification.checked)
            notification = 1;

        let email = order_email.value;

        let data = {
            'order_call_me': call_me,
            'order_notification': notification,
            'order_email': email,
        }
        console.log(data)
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