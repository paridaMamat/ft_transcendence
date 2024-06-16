console.log('friends.js');

getMenuInfos();


console.log('friends.js');

let friendCounter = 1;
let sentInvitations = [];
let receivedInvitations = [];
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
            if (username) {
                sendInvitationToBackend(username);
            } else {
                Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
            }
        }
    });
}

function sendInvitationToBackend(username) {
   //api
    fetch('/friends/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Swal.fire('Invitation envoyée!', `${username} a été invité.`, 'success');
            sentInvitations.push({ id: data.id, username: username });
        } else {
            Swal.fire('Erreur', data.message, 'error');
        }
    })
    .catch(error => {
        Swal.fire('Erreur', 'Une erreur est survenue', 'error');
    });
}

// function receiveInvitation(id, username) {
//     Swal.fire({
//         title: `${username} vous a envoyé une invitation`,
//         showDenyButton: true,
//         showCancelButton: false,
//         confirmButtonText: `Accepter`,
//         denyButtonText: `Décliner`,
//     }).then((result) => {
//     if (result.isConfirmed) {
//         acceptInvitation(id, username);
//     } else if (result.isDenied) {
//         declineInvitation(id, username);
//     }
// });

// receivedInvitations.push({ id: id, username: username });
// }


function acceptInvitation(id, username) {
    // Simulate sending acceptance to the backend
    fetch('/accept_invitation/', {
        method: 'POST',
        headers:                    {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ id: id, username: username })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire('Invitation acceptée!', `${username} a été ajouté à votre liste d'amis.`, 'success');
                addFriendToUI(username, 'en ligne');
            } else {
                Swal.fire('Erreur', data.message, 'error');
          }
        })
        .catch(error => {
            Swal.fire('Erreur', 'Une erreur est survenue', 'error');
        });
}

function declineInvitation(id, username) {
    // Simulate sending decline to the backend
    fetch('/decline_invitation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ id: id, username: username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Swal.fire('Invitation déclinée', `${username} n'a pas été ajouté à votre liste d'amis.`, 'info');
        } else {addFriendToUI('imraoui', 'en ligne', 'avatar.jpg');

            Swal.fire('Erreur', data.message, 'error');
        }
    })
    .catch(error => {
        Swal.fire('Erreur', 'Une erreur est survenue', 'error');
    });
}

async function addFriendToUI() {
    const data = getUserData();
    const friends = data.friends;
    if (friends && Array.isArray(friends)){
        const circlesContainer = document.getElementById('circlesContainer');
        friends.forEach(friend => {
            const newFriendDiv = document.createElement('div');
            newFriendDiv.className = 'friend-circle';

            // Détermination de la couleur en fonction du statut
            let statusColor;
            switch (friend.status) {
                // case 'en attente': statusColor = 'yellow'; break;
                case 'en ligne': statusColor = 'green'; break;
                case 'en partie': statusColor = 'orange'; break;
                case 'hors ligne': statusColor = 'red'; break;
                default: statusColor = 'gray';
            }
            const username = friend.username;
            const avatarUrl = friend.avatar;
            // Structure HTML pour chaque ami
            newFriendDiv.innerHTML = `
                <div class="friend-avatar" style="background-image: url('${avatarUrl}');">
                <div class="friend-status" style="background-color: ${statusColor};"></div>
                </div>
                <div class="friend-name">${username}</div>
                `;
            circlesContainer.appendChild(newFriendDiv);
        });
    }
}


// Exemple d'utilisation c'est just une teste mais il faut enlever apres en va rajouter de base de donne***/
// addFriendToUI('imraoui', 'en ligne', 'avatar.jpg');
// addFriendToUI('hfergani', 'en partie', 'avatar.jpg');
// addFriendToUI('Mvicedo', 'en attente', 'avatar.jpg');
// addFriendToUI('Pmaimait', 'hors ligne', 'avatar.jpg');
// addFriendToUI('Hferjani', 'en partie', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');
// addFriendToUI('Blefebvr', 'en attente', 'avatar.jpg');

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
                fetch('/friends/', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    // body: JSON.stringify({ username: username })
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

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
