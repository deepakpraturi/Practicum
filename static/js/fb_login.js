window.fbAsyncInit = function() {
    FB.init({
      appId      : '1815162415209496',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.8'
    });

    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
};

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "//connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function statusChangeCallback(response){
    if(response.status === 'connected'){
        console.log('Logged in and authenticated');
        // testAPI();
    } else {
        console.log('Not authenticated');
    }
}


function checkLoginState() {
    FB.getLoginStatus(function(response) {
    // statusChangeCallback(response);
        console.log(response.status);
        if (response.status === 'connected'){
            testAPI();
        }
    });
}

function testAPI(){
FB.api('/me?fields=name,email', function(response){
  if(response && !response.error){
    console.log(response);
    console.log(response.name);
    console.log(response.email);
    let data = {
        name : response.name,
        email : response.email
    };
    $.ajax({
        type: 'POST',
        url: '/fb-user-management',
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8'
    }).done(function (data) {
        if (data==='exists'){
            window.location = '/user-home';
        }
        else if(data === 'new_user'){
            window.location = '/signup-interested';
        }
    });
  }
  FB.api('/me/feed', function(response){
    if(response && !response.error){
    }
  });
})
}

function logout(){
FB.logout(function(response){
    window.location = '/'
});
}
