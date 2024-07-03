console.log('friends.js');

getMenuInfos();

displayFriends();

//verifier que le username existe bien dans le fetch de data
async function getFriendByName(username) {
    try {
        const response = await fetch('api/users/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('data in getFriend = ', data);
        if (Array.isArray(data)) {
            const user = data.find(user => user.username === username);
            console.log('user = ', user);
            return user || null;
        } else {
            console.error('Fetched data is not an array:', data);
            return null;
        }
    } catch (error) {
        console.error("Error fetching users", error);
        throw error;
    }
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

async function addFriendToBackend(friend) {
    const data = await retrieveUserData();
    const userId = data.id;
    const csrfToken = getCSRFToken();
    if (!csrfToken) {
        throw new Error('No CSRF token generated');
    }
    console.log('csrf token', csrfToken);

    console.log('friend.username = ', friend.username);
    console.log('friend.status = ', friend.status);
    console.log('data= ', data);

    const response = await fetch(`api/users/add_friends/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ friendId: friend.id })
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Network response was not ok: ${response.status} ${response.statusText}\n${errorText}`);
    }
    return await response.json();
}

async function inviteFriend(){
    try {
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
            if (!username) {
                throw new Error('Veuillez entrer un nom d\'utilisateur');
            }

            const user = await getFriendByName(username);
            if (!user) {
                throw new Error('Utilisateur non trouvé');
            }

            await addFriendToBackend(user);
            Swal.fire('Ajout effectué!', `${user.username} a été ajouté.`, 'success');
            window.location.href = '#friends';
        }
    } catch (error) {
        console.error('Error in inviteFriend:', error);
        Swal.fire('Erreur', error.message || 'Une erreur est survenue', 'error');
    }
}

async function displayFriends() {
    try {
        const circlesContainer = document.getElementById('circlesContainer');
        if (!circlesContainer) {
            throw new Error('Circles container not found');
        }
        circlesContainer.innerHTML = ''; // Clear previous friends if any

        const result = await getFriendData();
        console.log('Friend data result:', result); // Debug: log the result

        if (!result) {
            throw new Error('Friends data is not confirmed or empty');
        }

        const friends = result;
        if (!Array.isArray(friends)) {
            throw new Error('Friends list is not available or not an array');
        }

        friends.forEach(friend => {
            const newFriendDiv = document.createElement('div');
            newFriendDiv.className = 'friend-circle';

            // Debug: log each friend's data
            console.log('Friend:', friend);

            // Détermination de la couleur en fonction du statut
            let statusColor;
            switch (friend.status) {
                case 'online': statusColor = 'green'; break;
                case 'playing': statusColor = 'orange'; break;
                case 'offline': statusColor = 'red'; break;
                default: statusColor = 'gray';
            }

            // Structure HTML pour chaque ami
            newFriendDiv.innerHTML = `
                <div class="friend-avatar" style="background-image: url('${friend.avatar}');">
                    <div class="friend-status" style="background-color: ${statusColor};"></div>
                </div>
                <div class="friend-name">${friend.username}</div>
            `;
            circlesContainer.appendChild(newFriendDiv);
        });

    } catch (error) {
        console.error('Error: cannot display friends', error);
        // Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
    }
}

async function promptDeleteFriend() {
    try {
        const result = await Swal.fire({
            title: 'Supprimer un ami',
            input: 'text',
            inputLabel: 'Nom d\'utilisateur de l\'ami',
            inputPlaceholder: 'Entrez le nom d\'utilisateur',
            showCancelButton: true,
            confirmButtonText: 'Supprimer',
            cancelButtonText: 'Annuler',
        });

        if (result.isConfirmed) {
            const username = result.value;
            console.log('in prompt-delete, username: ', username);
            if (!username) {
                throw new Error('Veuillez entrer un nom d\'utilisateur');
            }
            const response = await deleteFriend(username);
            if (response.success) {
                Swal.fire('Suppression effectuée !', `${username} a été supprimé de votre liste d'amis.`, 'success');
                window.location.href = '#friends';
            }
        }
    } catch (error) {
        console.error('Error in prompt delete:', error);
        Swal.fire('Utlisateur inconnu' || 'Une erreur est survenue', 'error');
    }
}

async function deleteFriend(friendName) {
    const circlesContainer = document.getElementById('circlesContainer');
    const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(friendName));
    if (friendDiv) {
       try {
            const result = await Swal.fire({
            title: 'Êtes-vous sûr?',
            text: `Voulez-vous vraiment supprimer ${friendName} de votre liste d'amis?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Oui, supprimer!',
            cancelButtonText: 'Annuler'
            })

            if (result.isConfirmed) {
                if (result.isConfirmed) {
                    const username = result.value;
                    if (!username) {
                        throw new Error('Veuillez entrer un nom d\'utilisateur');
                    }
        
                    const friend = await getFriendByName(friendName);
                    if (!friend) {
                        throw new Error('Utilisateur non trouvé');
                    }
                    const data = await retrieveUserData();
                    const userId = data.id;
                    const csrfToken = getCSRFToken();
                    if (!csrfToken) {
                        throw new Error('No CSRF token generated');
                    }

                // Simulate sending delete request to the backend
                const response = await fetch(`api/users/remove_friends/${userId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ friendId: friend.id })
                })
            
                if (!response.ok){
                    const errorText = await response.text();
                    throw new Error(`Network response was not ok: ${response.status} ${response.statusText}\n${errorText}`);
                }  
                circlesContainer.removeChild(friendDiv);
                Swal.fire('Supprimé!', `${friend.username} a été supprimé de votre liste d'amis.`, 'success');
                return await response.json();
                }  
            } 
        }
        catch (error) {
            console.error('Error in deleteFriend:', error);
            Swal.fire('Erreur in deleteFriend', error.message || 'Une erreur est survenue', 'error');
        }
    }
};
