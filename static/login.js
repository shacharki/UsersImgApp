$(document).ready(function() {
    $('#toggle-password').click(function(){
        $(this).toggleClass('active');
        var type = $(this).hasClass('active') ? 'text' : 'password';
        $('#password').attr('type', type);
    });

    $('#login-form').submit(function(event) {
        event.preventDefault();
        
        var username = $('#username').val();
        var password = $('#password').val();
        
        if (!username || !password) {
            showError("Please fill in all fields.");
            return;
        }
        
        $(this)[0].submit();
    });

    function showError(message) {
        var alertDiv = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                       message +
                       '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                       '<span aria-hidden="true">&times;</span>' +
                       '</button>' +
                       '</div>';
        $('.container-login').prepend(alertDiv);
    }

    setTimeout(function() {
        $('.alert-success').alert('close');
    }, 100);
});
