let categories;

$(document).ready(function() {
    $.ajax({
        type: 'POST',
        url: '/categories',
        contentType: 'application/json;charset=UTF-8'
    }).done(function (data) {
        // console.log(data);
        categories = data;
    });
});

function filter(current) {
    console.log(current);
    hide_classes(current);
}

function hide_classes(current) {
    $('.'+current).show();
    categories.forEach(function (element) {
        console.log(element);
        if (element!==current){
            let hidden_class = '.'+element;
            $(hidden_class).fadeOut(300, function () {
                $(hidden_class).hide();
            });
        }
    })
}