console.log('lobby.js loaded'); // Log pour confirmer le chargement du script

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


$(document).ready(function() {
    // Fonction pour lancer la recherche d'adversaire
    function findOpponent() {
        $.ajax({
            type: 'POST',
            url: '/api/lobbies/',  // URL de votre API Django
            data: {
                id: '2',
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()  // Utilisation correcte du token CSRF
            },
            success: function(response) {
                if (response.status === 'matched') {
                    // Afficher les détails de l'adversaire
                    $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
                    $('.username').text(response.opponent.username);
                    $('#start-game').show();  // Afficher le bouton de démarrage du jeu
                } else if (response.status === 'waiting') {
                    // Afficher un indicateur d'attente
                    $('.waiting-indicator p').text('Recherche d\'un adversaire...');
                }
            },
            error: function(error) {
                console.error('Erreur lors de la requête AJAX :', error);
            }
        });
    }

    // Appeler la fonction pour trouver un adversaire lors du chargement de la page
    findOpponent();

    // Événement si l'utilisateur clique pour démarrer le jeu
    $('#start-game').click(function() {
        // Mettez ici le code pour démarrer le jeu avec l'adversaire trouvé
        alert('Démarrage du jeu avec ' + $('.username').text());
    });
});





  // console.log('Tentative de sélection des éléments HTML...');
  // const opponentInfo = document.querySelector('.opponent-info');
  // const waitingIndicator = document.querySelector('.waiting-indicator');
  // const startGameButton = document.getElementById('start-game');

  // console.log('Page du lobby chargée');

  // // il faut que ce soit un api
  // function checkForOpponent() {
  //   console.log('Vérification de l\'adversaire...');
  //   fetch('/check-opponent/', {
  //     method: 'GET',
  //     headers: {
  //       'X-Requested-With': 'XMLHttpRequest',
  //     },
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log('Réponse de la vérification de l\'adversaire :', data);
  //     if (data.opponent) {
  //       opponentInfo.innerHTML = `
  //         <img src="${data.opponent.avatar}" alt="${data.opponent.username}">
  //         <p>${data.opponent.username}</p>
  //       `;
  //       opponentInfo.style.display = 'flex';
  //       waitingIndicator.style.display = 'none';
  //       startGameButton.style.display = 'block';
  //       console.log('Adversaire trouvé :', data.opponent);
  //     } else {
  //       setTimeout(checkForOpponent, 5000); // Vérifier à nouveau dans 5 secondes
  //       console.log('Aucun adversaire trouvé, nouvelle vérification dans 5 secondes...');
  //     }
  //   })
  //   .catch(error => {
  //     console.error('Erreur lors de la vérification de l\'adversaire :', error);
  //   });
  // }

  // checkForOpponent();

  // startGameButton.addEventListener('click', function() {
  //   // Rediriger vers la page du jeu
  //   window.location.href = '/game/';

  // });
