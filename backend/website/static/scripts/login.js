console.log('login.js');

const loadjQuery = () => {
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
                        console.log('Access Token:', response.access);
                        console.log('Refresh Token:', response.refresh);

                        // Save tokens in local storage or cookies
                        localStorage.setItem('access', response.access);
                        localStorage.setItem('refresh', response.refresh);
                        // Redirect to a protected page or handle success as needed
                        window.location.href = '#accueil';
                    },
                    error: function(xhr, status, error){
                        console.error(xhr.responseText);
                        $('#error-message').text('Username or password is incorrect. Please try again.').show();
                    }
                });
            });
        });
    }
)