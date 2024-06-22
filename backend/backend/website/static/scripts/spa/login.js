console.log('login.js');

loadjQuery()
    .then(() => {
        $(document).ready(function(){
            $('#loginForm').submit(function(event){
                event.preventDefault(); // Prevent the default form submission
    
                var formData = $(this).serialize(); // Serialize the form data
    
                $.ajax({
                    url: 'login/', // Use the URL of your LoginView
                    method: 'POST',
                    data: formData,
                    success: function(response){
                        if (response.redirect) {
                            console.log('Redirect URL:', response.url);
                            // Redirect to the OTP verification page
                            window.location.href = response.url;
                        } else {
                            console.log('Access Token:', response.access);
                            console.log('Refresh Token:', response.refresh);
    
                            // Save tokens in local storage or cookies
                            localStorage.setItem('access', response.access);
                            localStorage.setItem('refresh', response.refresh);
                            // Redirect to a protected page or handle success as needed
                            window.location.href = '#accueil';
                        }
                    },
                    error: function(xhr, status, error){
                        console.error(xhr.responseText);
                        $('#error-message').text('Username or password is incorrect. Please try again.').show();
                    }
                });
            });
        });

    });

async function auth42API(){
    document.getElementById('intra42Login').addEventListener('click', function() {
        fetch('auth42/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            window.location.href = data.authUrl;
        })
        .catch(error => {
            console.error('Error fetching auth URL:', error);
        });
    });
};

auth42API();