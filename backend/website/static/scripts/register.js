console.log('register.js');


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
		console.log('register.JS IS LOAD');

		async function submitSignupForm(event) {
		// Get form elements
		const firstNameInput = document.getElementById('first_name');
		const lastNameInput = document.getElementById('last_name');
		const userNameInput = document.getElementById('username');
		const emailInput = document.getElementById('email');

		// Validate last_name and first_name (basic example)
		let isValid = true;
		let errorMessage = '';

		if (!firstNameInput.value.trim()) {
			isValid = false;
			errorMessage += 'First name is required. ';
		}

		if (!lastNameInput.value.trim()) {
			isValid = false;
			errorMessage += 'Last name is required. ';
		}

		if (!userNameInput.value.trim()) {
			isValid = false;
			errorMessage += 'Username is required. ';
		}

		if (!emailInput.value.trim()) {
			isValid = false;
			errorMessage += 'Email is required. ';
		}

		// You can add more validation rules here (e.g., minimum length, format)

		// Submit form if validation passes
		if (isValid) {
			const formData = new FormData(document.getElementById('signupForm')); // Get form data

			try {
				const response = await fetch($(this).attr('action'), { // Use form's action URL
				method: 'POST',
				body: formData
				});

			if (response.ok) {
				const data = await response.json();
				if (data.success) {
				// Redirect to login page (replace with desired URL)
				window.location.href = 'connection/';
				} else {
				// Display error message (from server)
				const errorMessage = document.getElementById('error-message');
				errorMessage.textContent = data.error;
				errorMessage.style.display = 'block'; // Show error message
				}
			} else {
				console.error('Network error:', response.statusText);
				// Handle network errors appropriately (e.g., display generic error message)
			}
			} catch (error) {
			console.error('Error submitting form:', error);
			// Handle other errors (e.g., form validation errors)
			}
		} else {
			// Display validation error message
			const errorMessageElement = document.getElementById('error-message'); // Assuming you have an element for displaying errors
			errorMessageElement.textContent = errorMessage;
			errorMessageElement.style.display = 'block'; // Show error message
		}
	}
		  
	document.getElementById('signupForm').addEventListener('submit', submitSignupForm);
	})
    .catch(error => {
        console.error("Error loading jQuery:", error);
 });
