$(".searchbox").autocomplete({
    source: function(request, response) {
        console.log(request.term);
        $.ajax({
            url: "https://en.wikipedia.org/w/api.php",
            dataType: "jsonp",
            data: {
                'action': "opensearch",
                'format': "json",
                'search': request.term
            },
            success: function(data) {
                response(data[1]);
            }
        });
    }
});

$(".searchbox").on("keydown", function (event) {
    if (event.key == "Enter") event.preventDefault();
});