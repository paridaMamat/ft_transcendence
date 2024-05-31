console.log('accueil.js chargé');

document.addEventListener('DOMContentLoaded', function() {
  // Simuler un utilisateur connecté
  const loggedIn = true; // Vous devrez adapter cette partie à votre gestion d'état de connexion
  const userAvatar = 'setting.jpg'; // Chemin de l'avatar de l'utilisateur
  const userLogin = 'NomUtilisateur'; // Login de l'utilisateur

  if (loggedIn) {
      document.getElementById('userAvatar').src = userAvatar;
      document.getElementById('userLogin').textContent = userLogin;
  }
  else {
    window.location.href = 'error_404/';
  }

});
