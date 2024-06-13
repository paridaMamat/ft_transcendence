
// $.ajax({
//   url: '/api/users/me',  // je ne sais pas c'est qu'elle api mais moi j'ai appelle comme sa
//   method: 'GET',
  
//   success: function(data) {
//       if (data.length > 0) {
//           //  user
//           $('#userLogin').text((user.username));
//           // avatar par default
//           $('#avatar').attr('src', userAvatarURL);
//       }           
//   },
//   error: function(xhr, status, error) {
//       console.error("Erreur lors de la récupération des données: ", error);
//   }
// });

getMenuInfos();

console.log('lobby.js loaded'); // Log pour confirmer le chargement du script


  console.log('Tentative de sélection des éléments HTML...');
  const opponentInfo = document.querySelector('.opponent-info');
  const waitingIndicator = document.querySelector('.waiting-indicator');
  const startGameButton = document.getElementById('start-game');

  console.log('Page du lobby chargée');

  // il faut que ce soit un api
  function checkForOpponent() {
    console.log('Vérification de l\'adversaire...');
    fetch('/check-opponent/', {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
    .then(response => response.json())
    .then(data => {
      console.log('Réponse de la vérification de l\'adversaire :', data);
      if (data.opponent) {
        opponentInfo.innerHTML = `
          <img src="${data.opponent.avatar}" alt="${data.opponent.username}">
          <p>${data.opponent.username}</p>
        `;
        opponentInfo.style.display = 'flex';
        waitingIndicator.style.display = 'none';
        startGameButton.style.display = 'block';
        console.log('Adversaire trouvé :', data.opponent);
      } else {
        setTimeout(checkForOpponent, 5000); // Vérifier à nouveau dans 5 secondes
        console.log('Aucun adversaire trouvé, nouvelle vérification dans 5 secondes...');
      }
    })
    .catch(error => {
      console.error('Erreur lors de la vérification de l\'adversaire :', error);
    });
  }

  checkForOpponent();

  startGameButton.addEventListener('click', function() {
    // Rediriger vers la page du jeu
    window.location.href = '/game/';

  });
