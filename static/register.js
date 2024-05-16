$(document).ready(function() {
    $('.toggle-password').click(function(){
        $(this).toggleClass('active');
        var input = $(this).closest('.input-group').find('input');
        var type = input.attr('type') === 'password' ? 'text' : 'password';
        input.attr('type', type);
    });

    $('#register-form').submit(function(event) {
        event.preventDefault();
        
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();
        
        if (!username || !password || !confirm_password || password !== confirm_password) {
            showError("Please fill in all fields and ensure that passwords match.");
            $('#register-button').prop('disabled', true);
            return;
        }
        
        $('#register-button').prop('disabled', false);
        $('#error-message').hide();
        
        $('#register-form')[0].submit();
        
        showSuccessMessage();
    });

    $('#username, #password, #confirm_password').on('input', function() {
        var username = $('#username').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();
        
        if (username || password || confirm_password) {
            $('#register-button').prop('disabled', false);
        } else {
            $('#register-button').prop('disabled', true);
        }
    });

    function showError(message) {
        $('#error-message').text(message).show();
    }

    function showSuccessMessage() {
            alert("Registration successful! You can now log in.");
            setTimeout(function() {
                window.location.href = "/login"; 
            }, 50000);
    }
});
