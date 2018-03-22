
function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var id_token = googleUser.getAuthResponse().id_token;
    var csrftoken = $("#csrf_token").text();

    $("#account_fullname").text(profile.getName());
    $("#account_image").attr('src', profile.getImageUrl());
    $("#sign-in").hide();
    $("#signed-in-menu").show();

    data = {
        'token': id_token
    }

    headers = {
        'X-CSRFToken': csrftoken
    }

    $.ajax({
        type: "POST",
        url: "/google_account_logged_in",
        data: data,
        headers: headers,
        dataType: "json"
    });
}

function signOut() {
var auth2 = gapi.auth2.getAuthInstance();
auth2.signOut().then(function () {
  $("#sign-in").show();
  $("#signed-in-menu").hide();
  console.log('User signed out.');
});
}
