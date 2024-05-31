
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