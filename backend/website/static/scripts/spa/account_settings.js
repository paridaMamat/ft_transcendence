console.log('accout_settings.js');

	async function getUserInfo() {
	  const response = await fetch('/api/user-info/'); // Replace with your API endpoint
	
	  if (response.ok) {
		const data = await response.json();
		document.getElementById('username').placeholder = data.username;
		document.getElementById('first_name').placeholder = data.first_name;
		document.getElementById('last_name').placeholder = data.last_name;
		document.getElementById('email').placeholder = data.email; // Include if you want to expose email
	  } else {
		console.error('Error fetching user info:', response.statusText);
	  }
	}
	
	// Call the function on window load (or after successful login)
	window.onload = getUserInfo;

fetch('/api/users/me')
  .then(response => {
    if (!response.ok) {
       throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Vérifier si l'utilisateur est authentifié
    if (data.username) {
      // Mettre à jour le contenu du span avec le nom d'utilisateur
      document.getElementById('userLogin').textContent = data.username;
      document.getElementById('avatar').textContent = data.avatar;
    } else {
      console.error('User not authenticated');
    }
  })  
  .catch(error => {
     console.error('There was a problem with the fetch operation:', error);
  });