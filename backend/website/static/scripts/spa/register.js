//import { loadjQuery } from "../utils.js";

console.log('register.js');
const loadjQuery2 = () => {
    return new Promise((resolve, reject) => {
        if (typeof window.jQuery !== 'undefined') {
			console.log('jQuery already loaded in login.js');
            resolve(); // jQuery already loaded
        } else {
            const script = document.createElement('script');
            script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        }
    });
};

loadjQuery2()
    .then(() => {
        $(document).ready(function(){
            $('#signupForm').submit(function(event){
                event.preventDefault(); // Prevent default form submission
                var formData = $(this).serialize(); // Serialize form data
        
                $.ajax({
                    url: 'register/',
                    method: 'POST',
                    data: formData,
                    success: function(response) {
                        // Open a new window for 2FA
                        var is2faEnabled = $('#two_factor_enabled').is(':checked'); // Check if 2FA checkbox is checked
                        console.log("Checkbox value:", is2faEnabled);
                        if (is2faEnabled) {
                            var twoFaWindow = window.open('enable-2fa/', '_blank');
                            // Handle 2FA communication and redirect on success
                            twoFaWindow.addEventListener('message', function(event) {
                            if (event.data === '2fa_success') {
                                twoFaWindow.close();
                                 window.location.href = '#login';
                                 }
                            });
                        }
                        else {
                            window.location.href = '#login';
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        // Handle error response
                        console.log(xhr.status + ": " + xhr.responseText);
                        // Display the error message at the top of the page
                        var errorMessage = xhr.responseText; // Assuming the server sends back a simple error message
                        $('#error-message').text(errorMessage).show();
                    }
                });
            });
        });
    }
);   