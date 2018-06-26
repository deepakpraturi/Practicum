$('.search').keyup(function (event) {
    console.log('in search function');
    let key_code = event.keyCode;
    if (key_code === 37 || key_code === 38 || key_code === 39 || key_code === 40){
        return
    }
    let $search_field = $(this);
    let search_query = $(this).val();
    let data = {
        data : search_query
    };
    console.log(search_query);
    $.ajax({
        type: 'POST',
        url: '/search',
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8'
    }).done(function (data) {
        let $search_results = $('#search-results');
        $search_results.children().remove();
        console.log(data);
        data.forEach(function (item) {
            $search_results.append('<div class="results"><a href="/post-page?post_id='+item[2]+'">'+item[0]+'</a></div>');
        });
    });
});