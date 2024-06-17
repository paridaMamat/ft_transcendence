//  remplace login.js sans utiliser ajax

loadjQuery()
    .then(() => {
        $(document).ready(function(){
            $('#loginForm').submit(function(event){
                event.preventDefault(); // Prevent the default form submission

                var formData = new FormData(this); // Create a FormData object with the form data
                
                // Convert FormData to JSON
                var object = {};
                formData.forEach((value, key) => {
                    object[key] = value;
                });
                var jsonData = JSON.stringify(object); //jsonData est concerti en chaîne JSON pour être envoyée dans le corps de la requête.

                fetch('login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Ensure you send the CSRF token if needed
                    },
                    body: jsonData
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(error => {
                            throw new Error(error);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.redirect) {
                        // Redirect to the OTP verification page
                        window.location.href = data.url;
                    } else {
                        console.log('Access Token:', data.access);
                        console.log('Refresh Token:', data.refresh);

                        // Save tokens in local storage or cookies
                        localStorage.setItem('access', data.access);
                        localStorage.setItem('refresh', data.refresh);
                        // Redirect to a protected page or handle success as needed
                        window.location.href = '#accueil';
                    }
                })
                .catch(error => {
                    console.error(error);
                    $('#error-message').text('Username or password is incorrect. Please try again.').show();
                });
            });
        });
    });

// Helper function to get CSRF token from cookies
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
