console.log('fetch_friends.js loaded');

function getfriends(){
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
}
   