console.log("I am in auth42.html");

function authenticate42(){
        // Get tokens from Django template context
        const tokens = JSON.parse('{{ tokens|escapejs }}');
        console.log('Access Token:', tokens.access);
        console.log('Refresh Token:', tokens.refresh);

        // Save tokens in local storage or cookies
        localStorage.setItem('access', tokens.access);
        localStorage.setItem('refresh', tokens.refresh);
        // Redirect to a protected page or handle success as needed
        window.location.href = '#accueil';
};

authenticate42();