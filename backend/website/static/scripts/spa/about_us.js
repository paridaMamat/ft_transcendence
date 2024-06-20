console.log('about_us.js chargé');

function setLanguage(language) {
  fetch('/set_language/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCookie('csrftoken')  // Assurez-vous d'inclure le jeton CSRF
      },
      body: `language=${language}`
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      location.reload();
  });
}

// Fonction pour obtenir le jeton CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}