console.log('welcome.js');
async function getUserInfo() {
	const response = await fetch('/api/user_info/'); 
	if (response.ok) {
	const data = await response.json();
	document.getElementById('user_info').innerHTML = `
		<p>Hello, ${data.username}</p>
		<p>Your First Name is ${data.first_name}</p>
		<p>Your Last Name is ${data.last_name}</p>
		<p>Your Email is ${data.email}</p>
			   
	`;
	} else {
	console.error('Error fetching user info:', response.statusText);
	}
}

getUserInfo();