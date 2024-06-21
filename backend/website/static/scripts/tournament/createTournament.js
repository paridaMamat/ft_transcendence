$(document).ready(function () {
    const tournoiForm = $('#tournoiForm');

    tournoiForm.on('submit', async function (event) {
        event.preventDefault();  // Empêche l'envoi par défaut du formulaire
        console.log("Form submitted");

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const gameId = getGameIdFromUrl();

        if (!csrfToken || !gameId) {
            console.error('CSRF token or Game ID is missing');
            return;
        }

        const nomTournoi = $('#tournoie').val();
        const alias = $('#Pseudo').val();

        if (!nomTournoi || !alias) {
            console.error('Missing form values');
            return;
        }

        try {
            const userData = await getCurrentUser(csrfToken);
            const userId = userData.id;

            const tournamentData = await createTournament(csrfToken, gameId, nomTournoi, userId);
            console.log("Tournament created:", tournamentData);

            const updatedUserData = await updateUserAlias(csrfToken, userId, alias);
            console.log("User alias updated:", updatedUserData);

            window.location.href = `#lobby_tournoi?id=${gameId}`;
        } catch (error) {
            console.error('Error:', error);
        }
    });

    async function getCurrentUser(csrfToken) {
        const response = await fetch('/api/users/me/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch current user');
        }

        return await response.json();
    }

    async function createTournament(csrfToken, gameId, nomTournoi, tourCreatorId) {
        const response = await fetch('/api/tournament/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                tour_name: nomTournoi,
                nb_players: 4,
                nb_rounds: 6,
                tour_game: gameId,
                tour_creator: tourCreatorId,
                current_round: 0,
                status: 'waiting',
                remaining_players: 4,
                tour_winner: null,
            })
        });

        if (!response.ok) {
            throw new Error('Failed to create tournament');
        }

        return await response.json();
    }

    async function updateUserAlias(csrfToken, userId, alias) {
        console.log(`Attempting to update alias for user with ID: ${userId}`);
        const response = await fetch(`/api/users/update_alias/${userId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                alias: alias,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to update user alias');
        }

        return await response.json();
    }

    function getGameIdFromUrl() {
        const hash = window.location.hash;
        return hash.includes('?') ? new URLSearchParams(hash.substring(hash.indexOf('?'))).get('id') : null;
    }
});





// console.log("createTournament.js loaded");

// $(document).ready(function () {
//     console.log("Document ready");

//     const tournoiForm = $('#tournoiForm');

//     tournoiForm.on('submit', function (event) {
//         event.preventDefault();  // Empêche l'envoi par défaut du formulaire
//         console.log("Form submitted");

//         // Fonction pour récupérer le token CSRF
//         function getCSRFToken() {
//             return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//         }

//         // Fonction pour récupérer l'ID du jeu depuis l'URL
//         function getGameIdFromUrl() {
//             const hash = window.location.hash; // Obtient la partie de hachage complète de l'URL
//             console.log(`Hash: ${hash}`); // Log pour confirmer le hachage
//             if (!hash.includes('?')) {
//                 return null;
//             } else {
//                 const hashParams = new URLSearchParams(hash.substring(hash.indexOf('?'))); // Extrait et analyse les paramètres de requête du hachage
//                 return hashParams.get('id'); // Obtient la valeur du paramètre 'id'
//             }
//         }

//         const csrfToken = getCSRFToken(); // Récupère le token CSRF
//         const gameId = getGameIdFromUrl(); // Récupère l'ID du jeu depuis l'URL

//         console.log(`CSRF token: ${csrfToken}`); // Log pour confirmer le token CSRF
//         console.log(`Game ID: ${gameId}`); // Log pour confirmer l'ID du jeu

//         if (!csrfToken) {
//             console.error('CSRF token is missing');
//             return;
//         }

//         if (!gameId) {
//             console.error('Game ID is missing');
//             return;
//         }

//         const nomTournoi = $('#tournoie').val(); // Récupère le nom du tournoi depuis le formulaire
//         const alias = $('#Pseudo').val(); // Récupère l'alias depuis le formulaire

//         console.log('Tournament ID:', gameId);
//         console.log('Nom du Tournoi:', nomTournoi);
//         console.log('Alias:', alias);

//         if (!nomTournoi || !alias) {
//             console.error('Missing form values');
//             return;
//         }

//         // Requête POST pour créer un tournoi
//         fetch('/api/tournament/', {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": csrfToken // Assure que le token CSRF est inclus
//                 },
//                 body: JSON.stringify({
//                     tour_name: nomTournoi,
//                     nb_players: 4,
//                     nb_rounds: 6,
//                     tour_game: gameId,
//                     tour_creator: null, // Laissez le serveur Django définir ceci
//                     current_round: 0,
//                     status: 'waiting',
//                     remaining_players: 4,
//                     tour_winner: null,
//                 })
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Network response was not ok');
//                 }
//                 return response.json();
//             })
//             .then(tournamentData => {
//                 console.log("Tournament created:", tournamentData);

//                 // Récupère l'utilisateur actuel pour obtenir son ID
//                 return fetch('/api/users/me/', {
//                     method: 'GET',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': csrfToken,
//                     }
//                 });
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch current user');
//                 }
//                 return response.json();
//             })
//             .then(userData => {
//                 const userId = userData.id; // Récupère l'ID de l'utilisateur
//                 console.log("Current user ID:", userId);

//                 // Requête PUT pour mettre à jour l'alias de l'utilisateur
//                 return fetch(`/api/users/${userId}/update_alias/`, {
//                     method: 'PUT',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': csrfToken,
//                     },
//                     body: JSON.stringify({
//                         alias: alias,
//                     }),
//                 });
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error('Failed to update user alias');
//                 }
//                 return response.json();
//             })
//             .then(updatedUserData => {
//                 console.log("User alias updated:", updatedUserData);
//                 window.location.href = `lobby-tournament?id=${gameId}`; // Redirige vers le lobby du tournoi
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//     });
// });

            


// // Capture de l'événement submit du formulaire
// 	document.getElementById("tournoiForm").addEventListener("submit", function(event) {
// 		event.preventDefault(); // Empêche le comportement par défaut du formulaire

//         console.log("Form submitted");

// 		function getCSRFToken() {
// 			return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// 		}
// 		function getGameIdFromUrl() {
// 			const hash = window.location.hash; // Get the full hash part of the URL
// 			console.log(`Hash: ${hash}`); // Log to confirm the hash
// 			if (!hash.includes('?')) {
// 				return null;
// 			} else {
// 			const hashParams = new URLSearchParams(hash.substring(hash.indexOf('?'))); // Extract and parse the query parameters from the hash
// 			return hashParams.get('id'); // Get the 'id' parameter value
// 			}
// 		}

// 		const csrfToken = getCSRFToken();
//         const gameId = getGameIdFromUrl();

//         console.log(`CSRF token: ${csrfToken}`); // Log to confirm CSRF token
//         console.log(`Game ID: ${gameId}`); // Log to confirm game ID

//         if (!csrfToken) {
//             console.error('CSRF token is missing');
//             return;
//         }

//         if (!gameId) {
//             console.error('Game ID is missing');
//             return;
//         }

// 		// Récupération des valeurs des champs
// 		const nomTournoi = document.getElementById("tournoie").value;
// 		const pseudo = document.getElementById("Pseudo").value;
//         const tournament_id =  document.getElementById("tournament_id").value;
//         const tournamentElement = document.getElementById('tournament');
//         const tournamentId = tournamentElement.getAttribute('data-tournament-id');
//         console.log("nomTournoi", nomTournoi);
//         console.log("pseudo", pseudo);
//         console.log("tournament_id", tournament_id);
		

// 		// Envoi des données vers le backend Django
//     // Send the data to the backend
//     fetch('api/tournament/', {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             "X-CSRFToken": csrfToken // Ensure the CSRF token is included
//         },
//         body: JSON.stringify({
//             tour_name: nomTournoi,
//             nb_players: 4,
//             nb_rounds: 6,
//             tour_game: gameId
//         })
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(data => {
//         console.log("Tournament created:", data);
//         return fetch('api/users/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrfToken,
//             },
//             body: JSON.stringify({
//                 alias: pseudo,
//             }),
//         });
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.json();
//     })
//     .then(userData => {
//         console.log("User created:", userData);
//         window.location.href = `lobby-tournament?id=${gameId}`;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });


// 		.then(response => response.json())
// 		.then(data => {
// 			if (data.id) {
// 				console.log("Tournament created with ID:", data.id);
// 				// Store the ID for future updates if necessary
// 				window.location.href = `lobby-tournament?id=${gameId}`;

// 			} else {
// 				console.error("Error creating tournament:", data);
// 			}
// 		})
// 		.catch(error => {
// 				console.error("Erreur:", error);
// 		});
// });
