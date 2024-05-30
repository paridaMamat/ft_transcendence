console.log('register.js');


        $(document).ready(function(){
            $('#signupForm').submit(function(event){
                event.preventDefault(); // Prevent default form submission
                var formData = $(this).serialize(); // Serialize form data
                $.ajax({
                    url: 'register/',
                    method: 'POST',
                    //url: $(this).attr('action'), // Submit to the form's action URL
                    data: formData,
                    success: function(response) {
                        // // Handle successful response (e.g., redirect or display success message)
                        console.log("Registration successful");
                        window.location.href = '#login';                       
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
