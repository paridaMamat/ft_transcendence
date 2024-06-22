console.log('accueil.js');

$(document).ready(function(){
  function fetchData() {
    const token = localStorage.getItem('access');  // Ensure you're retrieving the 'access' token

    if (!token) {
      // Handle missing token gracefully
      displayError('Missing access token. Please login.');
      return;
    }

    console.log('Access Token:', token);

    fetch('/protected/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    .then(response => {
      if (!response.ok) {
        // Handle response errors
        return response.json().then(errorData => {
          displayError(errorData.detail || 'An error occurred.'); // Use specific error message if available
        });
      }
      return response.json();
    })
    .then(data => {
      console.log(data); // Log the response data
      // Update the HTML with the username
      $('#userLogin').text(data.username);
    })
    .catch(error => {
      console.error('Error:', error);
      displayError('An unexpected error occurred.');
    });
  }

  function displayError(errorMessage) {
    // Update the HTML to display the error message (e.g., using an alert or modal)
    $('#error-message').text(errorMessage); // Assuming you have an element with this ID
  }

  // fetchData(); // Call fetchData when the document is ready

  });

//getMenuInfos();

// async function logout(){
//   console.log('logout loaded');
//   {
//     // Send an AJAX request to the logout view
//     fetch('/logout/', {
//         method: 'POST',
//         headers: {
//             'X-CSRFToken': '{{ csrf-token }}'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Redirect the user to the login page, for example
//         window.location.hash = '#login';
//     })      
//     .catch(error => console.error(error));
//   };
// }

// logout();





