console.log('register.js');

loadjQuery()
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
                        
                        if (response.success) {  
                            window.location.href = response.redirect_url;
                        } else {
                            $('#error-message').text(response.error).show();
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