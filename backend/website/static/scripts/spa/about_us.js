console.log('about_us.js chargé');

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function setLanguage(language) {
  fetch('/set_language/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCSRFToken()  // Assurez-vous d'inclure le jeton CSRF
      },
      body: `language=${language}`
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      location.reload();
  });
}
