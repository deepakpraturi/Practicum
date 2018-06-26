$("#signup-button").prop('disabled', true);

let email_boolean = false;
let password_boolean = false;
let retype_boolean = false;
let full_boolean = false;

$('#email-signup').keyup(function () {
    console.log('Email signup validation started');
    signup_email_validation();
    console.log('email result = '+email_boolean);
    check();
});

$('#pwd-signup').keyup(function () {
    console.log('Password validation started');
    signup_pwd_validation();
    console.log('password = '+password_boolean);
    check();
});

$('#re-pwd-signup').keyup(function () {
    console.log('Retyped password validation started');
    signup_retype_validation();
    console.log('retype = '+retype_boolean);
    check();
});

$("#full_name-signup").keyup(function () {
    console.log('Full name validation started');
    signup_full_name_validation();
    console.log('full name = '+full_boolean);
    check();
});

$("#mobile_number-signup").keyup(function(){
    console.log('Mobile number validation started');
    signup_mobile_validation();
    check();
});


function signup_email_validation() {
    let email = $('#email-signup').val();
    let pattern = /^[\S]+@[\S]+\.[\S]+$/;

    // $("#email-changed").text(email);

    if(pattern.test(email) && email!=='')
    {
        $("#invalid-email-signup").hide();
        $.ajax({
            data: {
                email : email
            },
            type: 'POST',
            url: '/ajax-email-check'
        }).done(function (data) {
                if(data.result){
                    console.log('in if');
                    $("#email-signup").css("border-bottom","2px solid #F90A0A");
                    $("#email-exists-signup").show();
                    $("#email-not-exists-signup").hide();
                }
                else {
                    console.log('in else');
                    $("#email-exists-signup").hide();
                    $("#email-not-exists-signup").show();
                }
            });
        $("#email-signup").css("border-bottom","2px solid #34F458");
        email_boolean = true;
    }
    else
    {
        email_boolean = false;
        $("#email-not-exists-signup").hide();
        $("#invalid-email-signup").show();
        $("#email-signup").css("border-bottom","2px solid #F90A0A");
    }
}

function signup_pwd_validation() {

    let pattern = /^.{3,20}$/;
    let password = $("#pwd-signup").val();
    console.log(password);
    console.log(pattern.test(password));
    if(!pattern.test(password) || password==='')
    {
        password_boolean = false;
        $("#invalid-pwd-signup").show();
        $("#pwd-signup").css("border-bottom","2px solid #F90A0A");
    }
    else
    {
        password_boolean = true;
        $("#invalid-pwd-signup").hide();
        $("#pwd-signup").css("border-bottom","2px solid #34F458")
    }
}

function signup_retype_validation() {
    let password = $("#pwd-signup").val();
    let retype = $("#re-pwd-signup").val();

    if (password !== retype || retype===""){
        retype_boolean = false;
        $("#invalid-retype-signup").show();
        $("#re-pwd-signup").css("border-bottom","2px solid #F90A0A");
    }

    else{
        retype_boolean = true;
        $("#invalid-retype-signup").hide();
        $("#re-pwd-signup").css("border-bottom","2px solid #34F458")
    }
}

function signup_full_name_validation() {
    let full_name = $("#full_name-signup").val();
    let pattern = /^.{3,20}$/;

    if (!pattern.test(full_name)){
        full_boolean = false;
        $("#invalid-full-name-signup").show();
        $("#full_name-signup").css("border-bottom","2px solid #F90A0A");
    }

    else {
        full_boolean = true;
        $("#invalid-full-name-signup").hide();
        $("#full_name-signup").css("border-bottom","2px solid #34F458");
    }
}

function signup_mobile_validation() {
    let mobile = $("#mobile_number-signup").val();
    let pattern = /[0-9]*|([0-9]+){10,13}/;

    if (!pattern.test(mobile)){
        $("#invalid-mobile-signup").show();
        $("#mobile_number-signup").css("border-bottom","2px solid #F90A0A");
    }

    else{
        $("#invalid-mobile-signup").hide();
        $("#mobile_number-signup").css("border-bottom","2px solid #34F458")
    }
}

function check() {
    if (email_boolean && password_boolean && retype_boolean && full_boolean) $("#signup-button").prop('disabled', false);
    else $("#signup-button").prop('disabled', true);
}