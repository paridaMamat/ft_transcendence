$.ajax({
  url: '/api/users/me',  // je ne sais pas c'est qu'elle api mais moi j'ai appelle comme sa
  method: 'GET',
  
  success: function(data) {
      if (data.length > 0) {
          //  user
          $('#userLogin').text((user.username));
          // avatar par default
          $('#avatar').attr('src', userAvatarURL);
      }           
  },
  error: function(xhr, status, error) {
      console.error("Erreur lors de la récupération des données: ", error);
  }
});

getMenuInfos();

// document.getElementById('joinLobbyButton').addEventListener('click', function() {
//     fetch('/api/matchmaking/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': '{{ csrf_token }}'
//         },
//         credentials: 'include'
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('lobbyStatus').innerText = data.message;
//     })
//     .catch(error => console.error('Error:', error));
// });

// document.getElementById('leaveLobbyButton').addEventListener('click', function() {
//     fetch('/api/matchmaking/', {
//         method: 'DELETE',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': '{{ csrf_token }}'
//         },
//         credentials: 'include'
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('lobbyStatus').innerText = data.message;
//     })
//     .catch(error => console.error('Error:', error));
// });

// Supposons que vous ayez besoin d'envoyer des informations sur le joueur, comme son ID ou ses préférences de jeu
const playerInfo = {
    playerId: "12345",
    preferredGameMode: "battle Royale",
  };
  
  // Utilisez l'API Fetch pour envoyer une requête POST avec les informations du joueur
  fetch('/api/matchmaking', {
    method: 'POST', // Spécifiez la méthode HTTP à utiliser
    headers: {
      'Content-Type': 'application/json', // Indiquez que le corps de la requête est au format JSON
    },
    body: JSON.stringify(playerInfo), // Convertissez les données du joueur en chaîne JSON
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error status: ${response.status}`);
    }
    return response.json(); // Parsez la réponse en JSON
  })
  .then(data => {
    console.log('Success:', data);
    // Traitez ici les données de réponse selon vos besoins
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  

getMenuInfos();