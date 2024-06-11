console.log('menu.js loaded');

async function getMenuInfos() {
  try {
    const response = await fetch('/api/users/me');
    const data = await response.json();

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
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
}

async function getUserID() {
  try {
    const response = await fetch('/api/users/me');
    const data = await response.json();
    // Vérifier si l'utilisateur est authentifié
    if (data.username) {
        console.log(data.id);
        return data.id; // Retourner l'ID de l'utilisateur
      } else {
        console.error('User not authenticated in getMenuData');
      }
    }
  catch (error) {
      console.error('There was a problem with the fetch operation:', error);
  }
}

// async function getUserID() {
//   try {
//     const response = await fetch('/api/user_stats/me');
//     const data = await response.json();
//     // Vérifier si l'utilisateur est authentifié
//     if (data.username) {
//         console.log(data.id);
//         return data.id; // Retourner l'ID de l'utilisateur
//       } else {
//         console.error('User not authenticated in getMenuData');
//       }
//     }
//   catch (error) {
//       console.error('There was a problem with the fetch operation:', error);
//   }
// }
