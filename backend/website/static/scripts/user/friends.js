console.log('friends.js');

getMenuInfos();

//verifier que le username existe bien dans le fetch de data
async function getFriendByName(username) {
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

async function addFriendToBackend(user) {
    try {
        const csrftoken = getCookie('csrftoken');
        console.log('friend.username = ', user.username);
        console.log('csrf = ', csrftoken);
        const response = await fetch('friends/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username: user.username})
        })
        if (response.success) {
            console.log('in addFriend bp 3');
            Swal.fire('Ajout effectué!', `${user.username} a été ajouté.`, 'success');
        } else {
            Swal.fire('Erreur', response.message, 'error');
            return null;
        }
        if (response.redirect) {  // Corrected this line
            console.log('in addFriend bp 4');
            window.location.href = response.url;  // Corrected this line
        }
    } catch (error) {
        Swal.fire('Erreur', 'Une erreur est survenue', 'error');
        return null;
    }
}

// function ok
async function displayFriends() {
    try{
        const data = retrieveUserData();
        const friends = data.friends;
        console.log('in displayFriends = ', friends);
        if (friends && Array.isArray(friends)){
            const circlesContainer = document.getElementById('circlesContainer');
            circlesContainer.innerHTML = ''; // Clear previous friends if any
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
                window.location.href = '#friends';
            });
        } else {
            console.error('Error: Friends list is not available or not an array', error);
        }
    } catch (error) {
        console.error('Error: cannot display friends', error);
        Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
    }
}

/*Swal.fire c'est une function pour alerte doc pour biblio lien(https://sweetalert.js.org/docs/)*/
async function inviteFriend() {
    const result = await Swal.fire({
        title: 'Ajouter un ami',
        input: 'text',
        inputLabel: 'Nom d\'utilisateur de l\'ami',
        inputPlaceholder: 'Entrez le nom d\'utilisateur',
        showCancelButton: true,
        confirmButtonText: 'Confirmer l\'ajout',
        cancelButtonText: 'Annuler',
    });

    if (result.isConfirmed) {
        const username = result.value;
        if (username) {
            try {
                const user = await getFriendByName(username);
                console.log('in inviteFriend,  user = ', user);
                if (user) {
                    const data = await addFriendToBackend(user);
                    if (data.error){
                        console.error('data is null', error);
                    }
                    else {
                        console.log('bp 1');
                        displayFriends();
                        // Swal.fire('Succès', 'Ami ajouté avec succès', 'success');
                    }
                } else {
                    Swal.fire('Erreur', 'Utilisateur non trouvé', 'error');
                }
            } catch (error) {
                Swal.fire('Erreur', 'Une erreur est survenue lors de l\'ajout de l\'ami', 'error');
            }
        } else {
            Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
        }
    }
};

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
                fetch('friends/', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        // 'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ username: username })
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

// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// };