
console.log('password_change.js loaded');


    function new_pasword(){
    const passwordForm = document.getElementById('password-form');
    
    if (passwordForm) {
        console.log('Password form found');
        
        // Log the CSRF token immediately (for debugging purposes)
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log('CSRF Token:', csrfToken);

        passwordForm.addEventListener('submit', function(event) {
            console.log('Form submit event triggered');
            event.preventDefault();
            
            const formData = new FormData(this);
            
            console.log('CSRF Token in form submission:', formData.get('csrfmiddlewaretoken'));
            console.log('Sending AJAX request to /password_change/');
            
            fetch('/password_change/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                console.log('Response received', response);
                return response.json();
            })
            .then(data => {
                console.log('Data received', data);
                if (data.success) {
                    alert('Password changed successfully!');
                    window.location.href = '#account_settings';
                } else {
                    alert('Error changing password: ' + JSON.stringify(data.error));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while changing the password.');
            });
        });
    } else {
        console.error('Password form not found');
    }
}

    new_pasword();

