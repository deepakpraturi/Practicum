$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.carousel').carousel();
    setInterval(function () {
       $('.carousel').carousel('next');
    }, 2000);
    $('select').formSelect();
    $('.tooltipped').tooltip();
    $(".dropdown-trigger").dropdown({hover : true});
    $(".dropdown-trigger-touch").dropdown({hover : false});

    // let search_results;
    // $.ajax({
    //     type : "POST",
    //     url : "/search",
    //     contentType: 'application/json;charset=UTF-8'
    // }).done(function (data) {
    //     console.log(data);
    //     search_results = data;
    //     $('input.search').autocomplete({
    //         data : search_results,
    //     });
    // });

    $('.autocomplete').keyup(function(event){
        let code = event.keyCode;
        if(code === 37 || code === 38 || code === 39 || code === 40) {
        return;
        }
        let $input_field = $(this);
        let search = $(this).val();
        console.log(search);
        $.ajax({
            url: "https://en.wikipedia.org/w/api.php",
            dataType: "jsonp",
            data: {
                'action': "opensearch",
                'format': "json",
                'search': search
            },
            success: function(data) {
                console.log(data);
                console.log(data[1]);
                let json_array = data;
                let suggestions = {};
                for (let i=0; i<json_array.length; i++){
                    suggestions[data[1][i]] = null;
                }
                console.log(suggestions);
                $('input.autocomplete').autocomplete({
                    data: suggestions,
                    limit : 10,
                    minLength : 0
                });
                $input_field.blur();
                $input_field.focus();
            }
        });
    });
});

$(".autocomplete").on("keydown", function (event) {
    if (event.key == "Enter") event.preventDefault();
});