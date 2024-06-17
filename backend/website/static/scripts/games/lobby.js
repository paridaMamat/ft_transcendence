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
                // Afficher les détails de l'adversaire
                $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
                $('.username').text(response.opponent.username);
                $('#start-game').show();  // Afficher le bouton de démarrage du jeu
            } else if (response.status === 'waiting') {
                // Afficher un indicateur d'attente
                $('.waiting-indicator p').text('Recherche d\'un adversaire...');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la requête fetch :', error);
        });
    }

    // Appel de la fonction pour lancer la recherche d'adversaire
    findOpponent();
});

// $(document).ready(function() {
//     // Fonction pour lancer la recherche d'adversaire
//     function findOpponent() {
//         console.log('function findOpponent()');
//         fetch('lobby/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()  // Ajout du token CSRF
//             },
//             body: JSON.stringify({
//                 id: '2'
//             })
//         })
//         console.log('after fetch lobby/')
//         .then(response => response.json())
//         .then(response => {
//             if (response.status === 'matched') {
//                 // Afficher les détails de l'adversaire
//                 $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
//                 $('.username').text(response.opponent.username);
//                 $('#start-game').show();  // Afficher le bouton de démarrage du jeu
//             } else if (response.status === 'waiting') {
//                 // Afficher un indicateur d'attente
//                 $('.waiting-indicator p').text('Recherche d\'un adversaire...');
//             }
//         })
//         .catch(error => {
//             console.error('Erreur lors de la requête fetch :', error);
//         });
//     }

//     // Appel de la fonction pour lancer la recherche d'adversaire
//     findOpponent();
//  });


// $(document).ready(function() {
//     // Fonction pour lancer la recherche d'adversaire
//     function findOpponent() {
//         console.log('function findOpponent() here');
//         $.ajax({
//             type: 'POST',
//             url: 'lobby/',  // URL de la vue pour trouver un adversaire
//             data: JSON.stringify({
//                 id: '2',
//                 csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
//             }),
//             contentType: 'application/json',
//             success: function(response) {
//                 console.log('after success')
//                 if (response.status === 'matched') {
//                     // Afficher les détails de l'adversaire
//                     $('.lobby-opponent-avatar img').attr('src', response.opponent.avatar);
//                     $('.username').text(response.opponent.username);
//                     $('#start-game').show();  // Afficher le bouton de démarrage du jeu
//                 } else if (response.status === 'waiting') {
//                     // Afficher un indicateur d'attente
//                     $('.waiting-indicator p').text('Recherche d\'un adversaire...');
//                 }
//             },
//             error: function(error) {
//                 console.error('Erreur lors de la requête AJAX :', error);
//             }
//         });
//     }

//     // Appeler la fonction pour trouver un adversaire lors du chargement de la page
//     findOpponent();

//     // Événement si l'utilisateur clique pour démarrer le jeu
//     $('#start-game').click(function() {
//         // Mettez ici le code pour démarrer le jeu avec l'adversaire trouvé
//         alert('Démarrage du jeu avec ' + $('.username').text());
//     });
// });





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
