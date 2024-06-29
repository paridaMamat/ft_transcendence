console.log('verify_opt.js');

loadjQuery()
    .then(() => {
        $(document).ready(function(){
            $('#otpForm').submit(function(event){
                event.preventDefault(); // Prevent the default form submission

                var formData = $(this).serialize(); // Serialize the form data

                $.ajax({
                    url: 'verify_otp/', // URL for OTP verification
                    method: 'POST',
                    data: formData,
                    success: function(response){
                        alert('OTP Verified Successfully!');
                        // Save tokens in local storage or cookies
                        localStorage.setItem('access', response.access);
                        localStorage.setItem('refresh', response.refresh);
                        // Redirect to a protected page or handle success as needed
                        window.location.href = '#accueil';
                    },
                    error: function(xhr, status, error){
                        console.error(xhr.responseText);
                        // Handle error case
                        alert('Invalid OTP. Please try again.');
                    }
                });
            });
        });
	}
);
