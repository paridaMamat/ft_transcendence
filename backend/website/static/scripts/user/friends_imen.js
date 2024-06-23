
console.log('friends.js');

getMenuInfos();

async function getFriendByName(csrftoken, username) {
        try {            
            const response = await fetch('api/users/');
           if (!response.ok) {
                throw new Error('Network response was not ok');
                }
            const data = await response.json();
            console.log('data in getFriend = ', response)
            if (Array.isArray(data)) {
                // Check if the username exists in the data
                const user = data.find(user => user.username === username);
                console.log('user = ', user);
                // Return the user if found, otherwise return null
                return user || null;
            } else {
                console.error('Fetched data is not an array:', data);
                return null;
            }
        } catch (error) {
            console.error("Error fetching users", error);
            return null;
        }
    };

/*Swal.fire c'est une bibliotheque pour alerte doc pour biblio lien(https://sweetalert.js.org/docs/)*/
function inviteFriend() {
    Swal.fire({
        title: 'Inviter un ami',
        input: 'text',
        inputLabel: 'Nom d\'utilisateur de l\'ami',
        inputPlaceholder: 'Entrez le nom d\'utilisateur',
        showCancelButton: true,
        confirmButtonText: 'Envoyer l\'invitation',
        cancelButtonText: 'Annuler',
    }).then((result) => {
        if (result.isConfirmed) {
            const username = result.value;
            const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            if (!csrftoken)
                console.log('no csrf token generated');
            else {
                console.log('csrf token', csrftoken);
            }
            if (username) {
                userId = getUserId();
                friend = getFriendByName(csrftoken, username);
                const response = sendInvitationToBackend(userId, friend, csrftoken);
            } 
        }
        else {
                Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
        }
    }).then ((response) =>   {
        if (response) {
            addFriendToUI(friend);
        }
        else
            console.error('error: could not send invite', error);
    })
}

async function sendInvitationToBackend(userId, friend, csrftoken) {
   //api
    const friendsToAdd = friend.id;
   await fetch(`api/users/add_friends/${userId}/`, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ add_friends: friendsToAdd })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Swal.fire('Invitation envoyée!', `${username} a été invité.`, 'success');
            a
        } else {
            Swal.fire('Erreur', data.message, 'error');
        }
    })
    .catch(error => {
        Swal.fire('Erreur', 'Une erreur est survenue', 'error');
    });
}

async function addFriendToUI(friend, csrftoken) {
    try {
        const data = await retrieveUserData(csrfToken);
        const friends = data.friends;
        console.log('in displayFriends = ', friends);
        if (friends && Array.isArray(friends)){
            const circlesContainer = document.getElementById('circlesContainer');
            const newFriendDiv = document.createElement('div');
            newFriendDiv.className = 'friend-circle';
            avatarUrl = friend.avatar;
            // Détermination de la couleur en fonction du statut
            let statusColor;
            switch (friend.status) {
                case 'waiting': statusColor = 'yellow'; break;
                case 'online': statusColor = 'green'; break;
                case 'playing': statusColor = 'orange'; break;
                case 'offline': statusColor = 'red'; break;
                default: statusColor = 'gray';
            }

            // Structure HTML pour chaque ami
            newFriendDiv.innerHTML = `
            <div class="friend-avatar" style="background-image: url('${avatarUrl}');">
                <div class="friend-status" style="background-color: ${statusColor};"></div>
            </div>
            <div class="friend-name">${username}</div>
            `;

            circlesContainer.appendChild(newFriendDiv);
        }
    } catch (error) {
        console.error('Error: cannot display friends', error);
        Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
    }
};

// Exemple d'utilisation c'est just une teste mais il faut enlever apres en va rajouter de base de donne***/


/*******************************fin de test**************************/

function promptDeleteFriend() {
    Swal.fire({
        title: 'Supprimer un ami',
        input: 'text',
        inputLabel: 'Nom d\'utilisateur de l\'ami',
        inputPlaceholder: 'Entrez le nom d\'utilisateur',
        showCancelButton: true,
        confirmButtonText: 'Supprimer',
        cancelButtonText: 'Annuler',
    }).then((result) => {
        if (result.isConfirmed) {
            const username = result.value;
            if (username) {
                deleteFriend(username);
            } else {
                Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
            }
        }
    });
}

function deleteFriend(username) {
    const circlesContainer = document.getElementById('circlesContainer');
    const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(username));

    if (friendDiv) {
        Swal.fire({
            title: 'Êtes-vous sûr?',
            text: `Voulez-vous vraiment supprimer ${username} de votre liste d'amis?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Oui, supprimer!',
            cancelButtonText: 'Annuler'
        }).then((result) => {
            if (result.isConfirmed) {
                // Simulate sending delete request to the backend
                fetch(`api/users/add_friends/${userId}/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify({ remove_friends: friendsToDelete })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        circlesContainer.removeChild(friendDiv);
                        Swal.fire('Supprimé!', `${username} a été supprimé de votre liste d'amis.`, 'success');
                    } else {
                        Swal.fire('Erreur', data.message, 'error');
                    }
                })
                .catch(error => {
                    Swal.fire('Erreur', 'Une erreur est survenue', 'error');
                });
            }
        });
    } else {
        Swal.fire('Erreur', 'Ami non trouvé', 'error');
    }
}

// async function displayFriends() {
//     try{
//         const data = retrieveUserData();
//         const friends = data.friends;
//         console.log('in displayFriends = ', friends);
//         if (friends && Array.isArray(friends)){
//             const circlesContainer = document.getElementById('circlesContainer');
//             circlesContainer.innerHTML = ''; // Clear previous friends if any
//             friends.forEach(friend => {
//                 const newFriendDiv = document.createElement('div');
//                 newFriendDiv.className = 'friend-circle';

//                 // Détermination de la couleur en fonction du statut
//                 let statusColor;
//                 switch (friend.status) {
//                     // case 'en attente': statusColor = 'yellow'; break;
//                     case 'en ligne': statusColor = 'green'; break;
//                     case 'en partie': statusColor = 'orange'; break;
//                     case 'hors ligne': statusColor = 'red'; break;
//                     default: statusColor = 'gray';
//                 }
//                 const username = friend.username;
//                 const avatarUrl = friend.avatar;
//                 // Structure HTML pour chaque ami
//                 newFriendDiv.innerHTML = `
//                     <div class="friend-avatar" style="background-image: url('${avatarUrl}');">
//                     <div class="friend-status" style="background-color: ${statusColor};"></div>
//                     </div>
//                     <div class="friend-name">${username}</div>
//                     `;
//                 circlesContainer.appendChild(newFriendDiv);
//                 window.location.href = '#friends';
//             });
//         } else {
//             console.error('Error: Friends list is not available or not an array', error);
//         }
//     } catch (error) {
//         console.error('Error: cannot display friends', error);
//         Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
//     }
// }

// /*Swal.fire c'est une bibliotheque pour alerte doc pour biblio lien(https://sweetalert.js.org/docs/)*/
// function inviteFriend() {
//     Swal.fire({
//         title: 'Inviter un ami',
//         input: 'text',
//         inputLabel: 'Nom d\'utilisateur de l\'ami',
//         inputPlaceholder: 'Entrez le nom d\'utilisateur',
//         showCancelButton: true,
//         confirmButtonText: 'Envoyer l\'invitation',
//         cancelButtonText: 'Annuler',
//     }).then((result) => {
//         if (result.isConfirmed) {
//             const username = result.value;
//             if (username) {
//                 sendInvitationToBackend(friend);
//             } else {
//                 Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//             } 
//         }
//     });
// }

// async function sendInvitationToBackend(friend, csrftoken, userId) {
//    //api
//    const friendsToAdd = [friend.id];

//    await fetch(`api/users/add_friends/${userId}/`, {
//     method: 'PUT',
//     headers: {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': csrftoken
//     },
//     body: JSON.stringify({ add_friends: friendsToAdd })
// })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             Swal.fire('Invitation envoyée!', `${username} a été invité.`, 'success');
//             sentInvitations.push({ id: data.id, username: username });
//         } else {
//             Swal.fire('Erreur', data.message, 'error');
//         }
//     })
//     .catch(error => {
//         Swal.fire('Erreur', 'Une erreur est survenue', 'error');
//     });
// }

// /*******************************fin de test**************************/

// function promptDeleteFriend() {
//     Swal.fire({
//         title: 'Supprimer un ami',
//         input: 'text',
//         inputLabel: 'Nom d\'utilisateur de l\'ami',
//         inputPlaceholder: 'Entrez le nom d\'utilisateur',
//         showCancelButton: true,
//         confirmButtonText: 'Supprimer',
//         cancelButtonText: 'Annuler',
//     }).then((result) => {
//         if (result.isConfirmed) {
//             const username = result.value;
//             if (username) {
//                 deleteFriend(username);
//             } else {
//                 Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//             }
//         }
//     });
// }

// function deleteFriend(username) {
//     const circlesContainer = document.getElementById('circlesContainer');
//     const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(username));

//     if (friendDiv) {
//         Swal.fire({
//             title: 'Êtes-vous sûr?',
//             text: `Voulez-vous vraiment supprimer ${username} de votre liste d'amis?`,
//             icon: 'warning',
//             showCancelButton: true,
//             confirmButtonText: 'Oui, supprimer!',
//             cancelButtonText: 'Annuler'
//         }).then((result) => {
//             if (result.isConfirmed) {
//                 // Simulate sending delete request to the backend
//                 fetch('/delete_friend/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': getCookie('csrftoken')
//                     },
//                     body: JSON.stringify({ username: username })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         circlesContainer.removeChild(friendDiv);
//                         Swal.fire('Supprimé!', `${username} a été supprimé de votre liste d'amis.`, 'success');
//                     } else {
//                         Swal.fire('Erreur', data.message, 'error');
//                     }
//                 })
//                 .catch(error => {
//                     Swal.fire('Erreur', 'Une erreur est survenue', 'error');
//                 });
//             }
//         });
//     } else {
//         Swal.fire('Erreur', 'Ami non trouvé', 'error');
//     }
// }

// displayFriends();