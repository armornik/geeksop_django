// если страница загружена, в basket_list сработал click в input, то вызываем функцию
window.onload = function(){
    $('.basket_list').on('click', 'input[type="number"]', function() {
        let t_href = event.target;
        console.log(t_href.name); // basket.id
        console.log(t_href.value); // basket.quantity

//        отправить данные на сервер
        $.ajax({
            url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
//          если всё успешно, выполнить функцию
            success: function(data) {
                $('.basket_list').html(data.result);
            },
        });
        event.preventDefault();
    })
}