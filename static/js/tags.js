$(document).ready(function() {
    let search_results;
    $.ajax({
        type : "POST",
        url : "/search-tags",
        contentType: 'application/json;charset=UTF-8'
    }).done(function (data) {
        console.log(data);
        search_results = data;
        $('.chips-autocomplete').chips({
            autocompleteOptions: {
                data: search_results,
                limit: Infinity,
                minLength: 1
            }
        });
    });
});

$('#details').on('click', function () {
    let top10 = [];
    $("input[name='list']").each(function() {
        top10.push($(this).val());
    });
    let tags = $('.chip').text();
    let data = {
        post_title : $('#post_title').val(),
        category : $('#selection :selected').text(),
        description : $('#post_description').val(),
        top10 : top10,
        tags : tags
    };
    console.log(data);
});

$('#create_post').on('submit', function (event) {
    event.preventDefault();
    let top10 = [];
    $("input[name='list']").each(function() {
        top10.push($(this).val());
    });
    let tags = $('.chip').text();
    let data = {
        post_title : $('#post_title').val(),
        category : $('#selection :selected').text(),
        description : $('#post_description').val(),
        top10 : top10,
        tags : tags
    };
    $.ajax({
        url : '/create-post',
        type : 'POST',
        data : JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8'
    }).done(function (data) {
        console.log(data);
        setTimeout(function () {
            let post_page = "/post-page?post_id="+data;
            window.location = post_page
        }, 1000)
    });
});