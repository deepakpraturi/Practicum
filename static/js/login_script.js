$("#form_email").keyup(function() {
    console.log('Email validation');
    check_email();
});

$("#form_pwd").keyup(function () {
    console.log('Password validation');
    check_pwd()
});

$("#login-form").on('submit', function (event) {
    console.log('Authentication in process');
    sleep(10000);
    $.ajax({
        data : {
            email : $("#form_email").val(),
            password : $("#form_pwd").val()
        },
        type : 'POST',
        url : '/ajax-login-check'
    }).done(function (data) {
        console.log('IN Done');
        sleep(1000);
            if (data.result){
                console.log('in login sucess');
                $("#login-failed").hide();
                $("#login-success").show();
                redirect_homepage()
            }
            else{
                console.log('in login fail');
                $("#login-failed").show();
                $("#login-success").hide();
            }
        }
    );
    event.preventDefault();
});

function check_email(){

    let pattern = /^[\S]+@[\S]+\.[\S]+$/;
    let email = $("#form_email").val();

    if(pattern.test(email) && email!=='')
    {
        $("#error-email").hide();
        $("#form_email").css("border-bottom","2px solid #34F458")
    }
    else
    {
        $("#error-email").show();
        $("#form_email").css("border-bottom","2px solid #F90A0A");
    }
}

function check_pwd(){

    let pattern = /^.{3,20}$/;
    let password = $("#form_pwd").val();
    console.log(password);
    console.log(pattern.test(password));
    if(!pattern.test(password) || password==='')
    {
        $("#error-pwd").show();
        $("#form_pwd").css("border-bottom","2px solid #F90A0A");
    }
    else
    {
        $("#error-pwd").hide();
        $("#form_pwd").css("border-bottom","2px solid #34F458")
    }
}

function redirect_homepage(){
    sleep(1000);
    window.location = "/";
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}