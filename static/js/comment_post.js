let delete_comment;

$('#post-comment').on('submit', function(event) {
    console.log('posting comment');
    let id = $(this).find('div').attr("id");
    id = id.substring(3);
    console.log(id);
    let data = {
        id : id,
        comment : $('#input_comment').val(),
        posted_by : $('#posted_by').val()
    };
    $.ajax({
        type : 'POST',
        url : '/comment-post',
        data : JSON.stringify(data),
        contentType : 'application/json;charset=UTF-8'
    }).done(function (result) {
       if (result[0]){
           console.log(result);
           $('#input_comment').val('');
           $('#input_comment').blur();
           $('#comments').append('<li class="collection-item avatar" style="display: none"><i class="material-icons circle">face</i><span class="title"><b>'+result[1]+'</b></span><p>'+result[2]+'<br></p><div class="secondary-content btn-flat"><i class="material-icons delete-comment" id="id-'+result[3]+'" style="color: red; font-weight: bold">close</i></div></li>');
           let $latest_comment = $('#comments li').last();
           $("#comments").animate({ scrollTop: $('#comments').prop("scrollHeight")}, 1000);
           $($latest_comment).fadeIn(1000);
           $($latest_comment).find("i.delete-comment").on('click', delete_comment);
       }
    });
    event.preventDefault();
});


$('.delete-comment').on('click',delete_comment = function() {
    let $close = $(this);
    let comment_id = $(this).attr('id');
    comment_id = comment_id.substring(3);
    console.log(comment_id);
    let data = {
        comment_id: comment_id
    };
    $.ajax({
        type: 'POST',
        url: '/delete-comment',
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8'
    }).done(function (result) {
        if (result) {
            $close.parent().parent().replaceWith('<li class="collection-item avatar center red lighten-3" id="deleted-comment"><i class="material-icons circle">mood_bad</i><span class="title"><b>Comment deleted</b></span><p>Mischief Managed!!!<br></p><div class="secondary-content btn-flat"></div></li>');
            $('#deleted-comment').fadeOut(1000, function () {
                $(this).remove();
            });
        }
    });
});

