console.log('welcome.js');

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
	}
);

getUserInfo();