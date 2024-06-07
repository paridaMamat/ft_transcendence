console.log('menu.js loaded');

function getMenuInfos(){
  fetch('/api/users/me')
  .then(data => {
    // Vérifier si l'utilisateur est authentifié
    if (data.username) {
      // Mettre à jour le contenu du span avec le nom d'utilisateur
      document.getElementById('userLogin').textContent = data.username;
      document.getElementById('avatar').textContent = data.avatar;
      // Vérifier et mettre à jour l'avatar
      // const avatarUrl = data.avatar ? data.avatar : 'default-avatar.jpg';
      // document.getElementById('avatar').src = avatarUrl;
    } else {
      console.error('User not authenticated in getMenuData');
      // Vous pouvez ajouter un comportement pour les utilisateurs non authentifiés ici
    }
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}

async function getUserID() {
  return fetch('/api/users/me')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Vérifier si l'utilisateur est authentifié
      if (data.username) {
        return data.id; // Retourner l'ID de l'utilisateur
      } else {
        throw new Error('User not authenticated in getUserID');
      }
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
}