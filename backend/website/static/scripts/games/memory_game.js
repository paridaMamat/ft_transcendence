console.log("test memory_game.js avant chargement anime.js");

$(document).ready(function(){

function loadScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

loadScript('https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js')

.then(() => {
    console.log('anime.js loaded');
    // Code à exécuter après le chargement de anime.js
    
var currentPlayer = 1;
var canPick = true;
var flippedCards = [];
var playerScores = [0, 0];
var totalPairs = 8;
//var totalPairs = 2;
var emojis = ["🐱", "🐶", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"];
//var emojis = ["🐱", "🐶"];
function createBoard() {
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

function displayPlayer() {
    var player1Element = document.querySelector(".user1");
    var player2Element = document.querySelector(".user2");

    if (currentPlayer === 1) {
        console.log("player 1 il joue");
        player1Element.classList.add("winner");
        player2Element.classList.remove("winner");
    } else {
        console.log("player 2 il joue");
        player1Element.classList.remove("winner");
        player2Element.classList.add("winner");
    }
}

function displayScores() {
    var messageElement = document.getElementById("scores");
    messageElement.innerHTML = playerScores[0]  + "-" + playerScores[1]  ;
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
        console.log("total",totalPairs);
        console.log("score===",playerScores[0] + playerScores[1]);
        if ((playerScores[0] + playerScores[1]) == totalPairs) {
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
    console.log("je suis fin de jeux");
    var cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.removeEventListener("click", flipCard);
    });
    canPick = false;
    //sendScoresToBackend() ;
    setTimeout(window.location.href = "pagefinal.html", 5000); // Reset the game after 5 seconds
}

window.onload = function () {
    createBoard();
    displayPlayer();
};
})

.catch(() => {
    console.error('Failed to load anime.js');
});
    
    });



// function sendScoresToBackend() {
//     fetch('/api/party/<pk>', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },

//         body: JSON.stringify({
//             scorePlayer1: scorePlayer1,
//             scorePlayer2: scorePlayer2,
//         }),
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log('Scores envoyés avec succès au backend:', data);
//     })
//     .catch(error => {
//         console.error('Erreur lors de l\'envoi des scores au backend:', error);
//     });
// }
