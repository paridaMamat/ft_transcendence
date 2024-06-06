console.log('enable_2fact.js');

loadjQuery()
    .then(() => {
		$(document).ready(function(){
            $('#verifyOtpForm').submit(function(event){
                event.preventDefault(); // Prevent the default form submission

                var formData = $(this).serialize(); // Serialize the form data

                $.ajax({
                    url: '/verify_otp/', // URL for OTP verification
                    method: 'POST',
                    data: formData,
                    success: function(response){
                        alert('2FA Enabled Successfully!');
                        window.location.href = '#login';
                    },
                    error: function(xhr, status, error){
                        console.error(xhr.responseText);
                        // Handle error case
                        alert('Invalid OTP or Session Expired. Please try again.');
                    }
                });
            });
        });
	}
);
