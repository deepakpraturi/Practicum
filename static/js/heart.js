$(function() {
  $(".heart").on("click", function() {
      let $like_count = $(this);
    $(this).toggleClass("heart-blast");
    let id = $(this).attr('id');
    console.log(id);
    id = id.substring(5);
    console.log(id);
    let status = $(this).hasClass('heart-blast');
    console.log('status = '+status);
    let data = {
        id : id,
        status : status
    };
    $.ajax({
        type : "POST",
        url : "/like-post",
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8'
        }).done(function (result) {
            console.log(result);
            $($like_count).find("h6").replaceWith("<h6 class=\"right valign-wrapper\" style=\"padding-top: 26%; font-size: 26px\">"+result[1]+"</h6>");
    })
  });
});