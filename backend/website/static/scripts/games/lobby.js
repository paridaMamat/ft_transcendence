console.log('lobby.js loaded'); // Log pour confirmer le chargement du script

getMenuInfos();

$(document).ready(function() {
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
    // Fonction pour lancer la recherche d'adversaire
    function findOpponent() {
        // Récupérer le token CSRF
        const csrfToken = getCSRFToken();

        // Assurez-vous que le token CSRF est présent
        if (!csrfToken) {
            console.error('CSRF token is missing');
            return;
        }

        fetch('/lobby/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Ajout du token CSRF
            },
            body: JSON.stringify({
                id: '2'
            })
        })
        .then(response => {
            // Vérifier si la réponse est OK
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(response => {
            if (response.status === 'matched') {
                console.log('response.status === matched');
                // Afficher les détails de l'adversaire
                $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
                //$('.lobby-opponent-avatar img').attr(src=="{% static 'img/default-avatar.jpg", response.opponent.avatar);
                $('#opponent-username').text(response.opponent.username);
                $('.waiting-indicator').hide();  // Masquer l'indicateur d'attente
                setTimeout(() => { // Rediriger vers la page du jeu après 3 secondes
                    window.location.href = '#pong3D';
                }   , 3000);
            } else if (response.status === 'waiting') {
                console.log('response.status === waiting');
                setTimeout(findOpponent, 5000); // Vérifier à nouveau dans 5 secondes
                // Afficher un indicateur d'attente
                // $('.waiting-indicator p').text('Recherche d\'un adversaire...');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la requête fetch :', error);
        });
    }

    function initialDelay() {
        console.log('Initial delay before starting to find opponent');
        setTimeout(findOpponent, 2000); // Délai initial de 3 secondes avant de commencer la recherche
    }

    initialDelay();

    // Appel de la fonction pour lancer la recherche d'adversaire
    //findOpponent();
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
