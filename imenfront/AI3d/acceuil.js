$.ajax({
    url: '/api/users/',  // je ne sais pas c'est qu'elle api mais moi j'ai appelle comme sa
    method: 'GET',
    
    success: function(data) {
        if (data.length > 0) {
            //  user
            $('#userLogin').text((user.username));
            // avatar par default <script>
        document.addEventListener("DOMContentLoaded", function() {
            // Remplacer l'URL par celle de votre API
            const apiUrl = 'https://votre-api.com/scores';

            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    const avatar1 = data[0];
                    const avatar2 = data[1];

                    // Mettre à jour le DOM avec les données reçues
                    document.getElementById('avatar-user1').src = avatar1.avatar_url;
                    document.getElementById('username1').innerText = avatar1.username;
                    document.getElementById('score1').innerText = avatar1.score;

                    document.getElementById('avatar-user2').src = avatar2.avatar_url;
                    document.getElementById('username2').innerText = avatar2.username;
                    document.getElementById('score2').innerText = avatar2.score;

                    // Comparer les scores et ajouter des classes pour le style
                    if (avatar1.score > avatar2.score) {
                        document.querySelector(".user1").classList.add("winner");
                    } else if (avatar2.score > avatar1.score) {
                        document.querySelector(".user2").classList.add("winner");
                    }
                })
                .catch(error => console.error('Erreur:', error));
        });
    </script>
        }           
    },
    error: function(xhr, status, error) {
        console.error("Erreur lors de la récupération des données: ", error);
    }
});