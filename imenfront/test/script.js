document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêche l'envoi du formulaire par défaut
  
    // Récupération des valeurs des champs de saisie
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var message = document.getElementById("message").value;
  
    // Création d'un objet JavaScript avec les valeurs saisies
    var data = {
      "name": name,
      "email": email,
      "message": message
    };
  
    // Envoi des données au serveur
    fetch('/enregistrer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Erreur lors de la requête');
      }
      return response.text();
    })
    .then(data => {
      console.log(data); // Affiche la réponse du serveur dans la console
    })
    .catch(error => {
      console.error('Erreur :', error);
    });
  });
  
