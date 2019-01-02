

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            csrf_token = $("#csrf_middleware input").attr("value")
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});
