
const loadjQuery = () => {
    return new Promise((resolve, reject) => {
        if (typeof window.jQuery !== 'undefined') {
			console.log('lOGIN.JS already loaded');
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
        console.log("jQuery loaded dynamically");
        $(document).ready(function(){
			$('#loginForm').submit(function(event){
				event.preventDefault(); // Prevent the default form submission
		
				// Serialize the form data
				var formData = $(this).serialize();
		
				// Send an AJAX request to the login URL
				$.ajax({
					url: $(this).attr('action'),
					method: 'POST',
					data: formData,
					success: function(response){
						if (response.success) {
							// Redirect to the game welcome page on successful login
							console.log('je suis a success login');
							window.location.href = '#welcome/'; // --> changer pour une redir spa
						} else {
							// Display the error message
							$('#error-message').text(response.error).show();
						}
					},
					error: function(xhr, status, error){
						// Handle the error response here
						console.error(xhr.responseText);
						// Display the error message
						$('#error-message').text('Username or password is incorrect. Please try again.').show();
					}
				});
			});
		});
    })
    .catch(error => {
        console.error("Error loading jQuery:", error);
 });