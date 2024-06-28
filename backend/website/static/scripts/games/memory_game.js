console.log("test memory_game.js avant chargement anime.js");



function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        console.log("memory_game.js src=", src);
        script.onload = () => {
            console.log("Script loaded successfully:", src);
            resolve();
        };
        script.onerror = (error) => {
            console.error("Failed to load script:", src, error);
            reject(error);
        };
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}


loadScript('https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js')

    .then(() => {
        console.log('anime.js loaded');
        
        const partyId = localStorage.getItem('partyId');
        if (partyId) {
            console.log("Récupération des données pour partyId:", partyId);
            function getCSRFToken() {
                console.log("getCSRFToken");
                return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            }
            async function fetchPartyAndPlayersData() {
                try {
                    const partyResponse = await fetch(`/api/party/${partyId}/`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        }
                    });
                    const partyData = await partyResponse.json();
                    console.log('Party data:', partyData);

                    const player2Response = await fetch(`/api/party/${partyId}/getPlayerUserInfo/`, {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCSRFToken()
                            }
                        });

                    const player2 = await player2Response.json();

                    $('#user2-username').text(player2.username);
                    $('#avatar-user2').attr('src', player2.avatar);

                    // Mise à jour des données des joueurs
                    if (partyData.type === 'Matchmaking') {
                        console.log('Matchmaking party');
                        $('#user1-username').text(partyData.player1.username);
                    } else if (partyData.type === 'Tournament') {
                        console.log('Tournament party');
                        $('#user1-username').text(partyData.player1.alias);
                    }

                } catch (error) {
                    console.error('Erreur lors de la récupération des données:', error);
                }

            }
            fetchPartyAndPlayersData();
        }




        // Code à exécuter après le chargement de anime.js
        var startTime, endTime,player1,player2,Time;
        var startTimes, endTimes,Times;
        var score1,score2;

        var currentPlayer = 1;
        var canPick = true;
        var flippedCards = [];
        var playerScores = [0, 0];
        //var totalPairs = 8;
        var totalPairs = 4;
        var player1Element = document.querySelector(".user1");
        var player2Element = document.querySelector(".user2");


        //var emojis = ["🐱", "🐶", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"];
        //c'est just pour test moin d'element il faut remettre emmogis avec 8 elemet et remet totalpaire a 8

        function afficherFinJeu() {
                   
            var message = score1 + "-" + score2;
            console.log("Je suis dans la fonction afficherFinJeu");
        
            // Utilisation de SweetAlert2 pour afficher l'alerte
            Swal.fire({
                title: 'Fin de jeu',
                text: message,
                icon: 'success',
                confirmButtonText: 'OK'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirection vers une autre page
                    window.location.href = "#page_finale";
                }
            });
        }
        // Fonction pour fermer l'alerte personnalisée
        function fermerAlerte() {
            document.getElementById('customAlert').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        }

        var emojis = ["🐱", "🐶", "🐹", "🐰"];
        function createBoard() {
            winner="";
            player1="player1";
            player2="player2"
            startTimes = new Date().toISOString(); // Enregistre le temps de début au format ISO

            var board = document.getElementById("board");
            board.innerHTML = ""; // Réinitialise le plateau de jeu

            var cards = emojis.concat(emojis);
            cards.sort(() => Math.random() - 0.5);

            var numCardsPerRow = 4;
            var numRows = Math.ceil(cards.length / numCardsPerRow);

            for (var i = 0; i < numRows; i++) {
                var row = document.createElement("div");
                row.className = "row";

                for (var j = 0; j < numCardsPerRow; j++) {
                    var index = i * numCardsPerRow + j;
                    if (index < cards.length) {
                        var card = document.createElement("div");
                        card.className = "card";
                        card.dataset.value = cards[index];
                        card.dataset.index = index;
                        card.addEventListener("click", flipCard);
                        row.appendChild(card);
                    }
                }

                board.appendChild(row);
            }
        }

        function flipCard() {
            var card = this;
            var value = card.dataset.value;
            var index = card.dataset.index;

            if (!canPick || card.classList.contains("flipped")) return;

            card.textContent = value;
            card.classList.add("flipped");
            flippedCards.push({ value, index });

            if (flippedCards.length === 2) {
                canPick = false;
                setTimeout(checkMatch, 1000);
            }
        }
        let nbrplayer1 = 0;
        let nbrplayer2 = 0;
        function displayPlayer() {


            if (currentPlayer === 1) {
                nbrplayer1++;
                console.log("nbr de jeux parti1", nbrplayer1);
                console.log("player 1 il joue");
                player1Element.classList.add("winner");
                player2Element.classList.remove("winner");
            }
            else {
                nbrplayer2++;
                console.log("player 2 il joue");
                console.log("nbr de jeux parti2", nbrplayer2);
                player1Element.classList.remove("winner");
                player2Element.classList.add("winner");
            }
        }

        function displayScores() {
            var messageElement = document.getElementById("scores");
            messageElement.innerHTML = playerScores[0] + "-" + playerScores[1];
            score1=playerScores[0];
            score2=playerScores[1];
        }

        function checkMatch() {
            var match = flippedCards[0].value === flippedCards[1].value;
            var cards = document.querySelectorAll(".card.flipped");
            if (match) {
                playerScores[currentPlayer - 1]++;
                cards.forEach(card => {
                    card.classList.add("matched");
                    card.textContent = ""; // Optionnel, supprime le contenu de la carte
                });
                console.log("total", totalPairs);
                console.log("score===", playerScores[0] + playerScores[1]);
                if ((playerScores[0] + playerScores[1]) == totalPairs) {
                    displayScores();
                    endGame();
                    return;
                }
            } else {
                setTimeout(() => {
                    cards.forEach(card => {
                        card.textContent = "";
                        card.classList.remove("flipped");
                    });
                    currentPlayer = currentPlayer === 1 ? 2 : 1;
                    displayPlayer();
                    flippedCards = [];
                    canPick = true;
                }, 1000);
                return;
            }

            flippedCards = [];
            canPick = true;
            displayScores(); // Mettre à jour les scores affichés
        }
        // /*******************alerte pour score ********************** */
        //Fonction pour afficher l'alerte personnalisée
    

      
        // /********************************************* */
        function resetGame() {
            createBoard();
            currentPlayer = 1;
            displayPlayer();
            var cards = document.querySelectorAll(".card");
            cards.forEach(card => {
                card.classList.remove("flipped", "matched");
                card.textContent = "";
            });
            flippedCards = [];
            canPick = true;
            playerScores = [0, 0];

        }
        function endGame() {
            endTimes = new Date().toISOString();
            endTime= new Date(endTimes).getTime();
            startTime= new Date(startTimes).getTime();

            var Time = Math.floor((endTime - startTime) / 1000);
            console.log("Durée totale de la partie:", Time);
            console.log("je suis fin de jeux");
            var cards = document.querySelectorAll(".card");
            cards.forEach(card => {
                card.removeEventListener("click", flipCard);
            });
            canPick = false;
            //sendScoresToBackend() ;
            // localStorage.removeItem('partyId'); // Supprime l'ID de la partie de localStorage
            if (playerScores[0] > playerScores[1]) {
                winner = player1;
            } else if (playerScores[1] > playerScores[0]) {
                winner = player2;
            }
            else if (playerScores[0] == playerScores[1]) {
                // En cas d'égalité de score
                if (nbrplayer1 > nbrplayer2) {
                    winner = player2;
                } else {
                    winner = player1;
                }
            }
		    console.log("Start Time: " ,startTimes);
            console.log("End Time: ",endTimes);
            console.log("Winner: " + winner);

		    console.log("Score: " + score1 + "-" + score2);
            console.log("Score1: ",score1);
            console.log("Score2: ",score2);
            //sendScores();
            console.log("personne qui a gagne", winner);
            afficherFinJeu();
        }

        createBoard();
        displayPlayer();


        function sendScores() {

            fetch(`/api/party/${partyId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },

                body: JSON.stringify({
                    game: 3,
                    score1: playerScores[0],
                    score2: playerScores[1],
                    status: 'finished',
                    winner_name: winner.textContent,
                    //winner_name: scorePlayer1 > scorePlayer2 ? 'player 1' : 'player 2'
                    //duration: a ajouter
                }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Scores envoyés avec succès au backend:', data);
                })
                .catch(error => {
                    console.error('Erreur lors de l\'envoi des scores au backend:', error);
                });
        }

    })

    .catch(() => {
        console.error('Failed to load anime.js');
    });
