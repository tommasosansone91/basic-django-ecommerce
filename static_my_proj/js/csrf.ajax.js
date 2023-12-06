
https://docs.djangoproject.com/it/4.2/howto/csrf/

$(document).ready(function(){

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');


    //  s4et ajax
    // #################

    //  recommended by django 4 docs
     // ----------------------------------

    // const request = new Request(
    //     /* URL */,
    //     {
    //         method: 'POST',
    //         headers: {'X-CSRFToken': csrftoken},
    //         mode: 'same-origin' // Do not send CSRF token to another domain.
    //     }
    // );
    // fetch(request).then(function(response) {
    //     // ...
    // });


    // justin verison - djajngo 1.0
    // ----------------------------------
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


})