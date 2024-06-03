console.log('accueil.js chargé');

console.log('protected.js loaded')
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
      $('#username').text(data.username);
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

  fetchData(); // Call fetchData when the document is ready
});

//document.addEventListener('DOMContentLoaded', function() {
//  // Simuler un utilisateur connecté
//  const loggedIn = true; // Vous devrez adapter cette partie à votre gestion d'état de connexion
//  const userAvatar = 'setting.jpg'; // Chemin de l'avatar de l'utilisateur
//  const userLogin = 'NomUtilisateur'; // Login de l'utilisateur

//  if (loggedIn) {
//      document.getElementById('userAvatar').src = userAvatar;
//      document.getElementById('userLogin').textContent = userLogin;
//  }
//  else {
//    window.location.href = 'error_404/';
//  }

//});
