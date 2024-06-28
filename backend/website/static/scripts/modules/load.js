console.log('load.js loaded');

function getMenuInfos(){
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

  // function logout(){
    
  //   document.getElementById('logout-btn').addEventListener('click', function(event) {
  //     // Send an AJAX request to the logout view
  //     fetch(/logout/, {
  //         method: 'POST',
  //         headers: {
  //             'X-CSRFToken': '{{ csrf_token }}'
  //         }
  //     })
  //    .then(response => response.json())
  //    .then(data => {
  //         // Redirect the user to the login page, for example
  //         window.location.hash = '#login';
  //     })
  //    .catch(error => console.error(error));
  // });
  // }