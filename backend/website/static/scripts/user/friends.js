console.log('friends.js');

getMenuInfos();

displayFriends();

//verifier que le username existe bien dans le fetch de data
//function ok
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
        throw error; // Propagate the error instead of returning null
    }
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

//function ok
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

//function ok
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

//function ok
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
        if (!friends || !Array.isArray(friends)) {
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

        // Moved outside of the loop
        // window.location.href = '#friends';
    } catch (error) {
        console.error('Error: cannot display friends', error);
        // Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
    }
}

async function promptDeleteFriend() {
    console.log('in prompt delete:');
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
            console.log('in prompt-delete bp1');
            // const user = await getFriendByName(username);
            // if (!user) {
            //     throw new Error('Utilisateur non trouvé');
            // }
            // console.log('in prompt-delete friend_to_delete: ', user.username);
            await deleteFriend(username);
            Swal.fire('Suppression effectuée !', `${user.username} a été supprimé de votre liste d'amis.`, 'success');
            window.location.href = '#friends';
        }
    } catch (error) {
        console.error('Error in prompt delete:', error);
        Swal.fire('Erreur', error.message || 'Une erreur est survenue', 'error');
    }
}

async function deleteFriend(friendName) {
    const circlesContainer = document.getElementById('circlesContainer');
    const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(friendName));
    console.log('in delete firend_to_delete: ', friendName);
    console.log('in delete, frienddiv: ', friendDiv);
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
                    console.log('in delete, username: ', username);
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
                    console.log('csrf token', csrfToken);

                    console.log('friend.username = ', friend.username);
                    console.log('friend.status = ', friend.status);
                    console.log('data= ', data);
                                
                // Simulate sending delete request to the backend
                await fetch(`api/users/remove_friends/${userId}/`, {
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
        
                }  
            } 
        }
        catch (error) {
            console.error('Error in deleteFriend:', error);
            Swal.fire('Erreur', error.message || 'Une erreur est survenue', 'error');
        }
    }
};

// function setupInviteListeners() {
//     console.log('setup Invite');
//     displayFriends();
    
//     const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//     if (!csrftoken)
//         console.log('no csrf token generated');
//     else
//         console.log('csrf token', csrftoken);

//     const userId = getUserId(csrftoken);
//     const handleClick = (event) => {
// 		if (event.target.matches("#inviteFriend()")) {
//             const friend = inviteFriend(csrftoken);
//             if (friend)
//                 sendInvitationToBackend(userId, friend, csrftoken);
//         }        
//         else if (event.target.matches("#promptDeleteFriend()")) {
//             const unfriended = promptDeleteFriend();
//             deleteFriend(unfriended, userId, csrftoken);
//         }
//       };
//     displayFriends();
//     document.body.addEventListener("click", handleClick);
// 	return () => document.body.removeEventListener("click", handleClick);
// };

// setupInviteListeners();

// async function getFriendByName(csrftoken, username) {
//         try {            
//             const response = await fetch('api/users/');
//            if (!response.ok) {
//                 throw new Error('Network response was not ok');
//                 }
//             const data = await response.json();
//             console.log('data in getFriend = ', response)
//             if (Array.isArray(data)) {
//                 // Check if the username exists in the data
//                 const user = data.find(user => user.username === username);
//                 console.log('user = ', user);
//                 // Return the user if found, otherwise return null
//                 return user || null;
//             } else {
//                 console.error('Fetched data is not an array:', data);
//                 return null;
//             }
//         } catch (error) {
//             console.error("Error fetching users", error);
//             return null;
//         }
//     };

// /*Swal.fire c'est une bibliotheque pour alerte doc pour biblio lien(https://sweetalert.js.org/docs/)*/
// function inviteFriend(csrftoken, userId) {
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
//                 friend = getFriendByName(csrftoken, username);
//                 return friend || null;
//             }
//         }
//         else {
//             Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//         }
//     })
// };

// async function sendInvitationToBackend(userId, friend, csrftoken) {
//    //api
//     const friendsToAdd = friend.id;
//    await fetch(`api/users/add_friends/${userId}/`, {
//     method: 'PUT',
//     headers: {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': csrftoken,
//     },
//     body: JSON.stringify({ add_friends: friendsToAdd })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             Swal.fire('Invitation envoyée!', `${friend.username} a été invité.`, 'success');
//         } else {
//             Swal.fire('Erreur', data.message, 'error');
//             console.error('Error: invitation non envoyee', error);
//         }
//     })
//     .catch(error => {
//         Swal.fire('Erreur', 'Une erreur est survenue', 'error');
//         console.error('Error: une erreur est survenue 2', error);
//     });
// }

// // async function addFriendToUI(friend, csrftoken) {
// //     try {
// //         const data = await retrieveUserData(csrfToken);
// //         const friends = data.friends;
// //         console.log('in displayFriends = ', friends);
// //         if (friends && Array.isArray(friends)){
// //             const circlesContainer = document.getElementById('circlesContainer');
// //             const newFriendDiv = document.createElement('div');
// //             newFriendDiv.className = 'friend-circle';
// //             avatarUrl = friend.avatar;
// //             // Détermination de la couleur en fonction du statut
// //             let statusColor;
// //             switch (friend.status) {
// //                 case 'waiting': statusColor = 'yellow'; break;
// //                 case 'online': statusColor = 'green'; break;
// //                 case 'playing': statusColor = 'orange'; break;
// //                 case 'offline': statusColor = 'red'; break;
// //                 default: statusColor = 'gray';
// //             }

// //             // Structure HTML pour chaque ami
// //             newFriendDiv.innerHTML = `
// //             <div class="friend-avatar" style="background-image: url('${avatarUrl}');">
// //                 <div class="friend-status" style="background-color: ${statusColor};"></div>
// //             </div>
// //             <div class="friend-name">${username}</div>
// //             `;

// //             circlesContainer.appendChild(newFriendDiv);
// //         }
// //     } catch (error) {
// //         console.error('Error: cannot display friends', error);
// //         Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
// //     }
// // };

// // Exemple d'utilisation c'est just une teste mais il faut enlever apres en va rajouter de base de donne***/


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
//                 return
//             } else {
//                 Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//             }
//         }
//     });
// }

// function deleteFriend(friend, userId, csrftoken) {
//     const circlesContainer = document.getElementById('circlesContainer');
//     const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(username));
//     const friendsToDelete = friend.id;
//     if (friendDiv) {
//         Swal.fire({
//             title: 'Êtes-vous sûr?',
//             text: `Voulez-vous vraiment supprimer ${friend.username} de votre liste d'amis?`,
//             icon: 'warning',
//             showCancelButton: true,
//             confirmButtonText: 'Oui, supprimer!',
//             cancelButtonText: 'Annuler'
//         }).then((result) => {
//             if (result.isConfirmed) {
//                 // Simulate sending delete request to the backend
//                 fetch(`api/users/add_friends/${userId}/`, {
//                     method: 'PUT',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': csrftoken,
//                     },
//                     body: JSON.stringify({ remove_friends: friendsToDelete })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         circlesContainer.removeChild(friendDiv);
//                         Swal.fire('Supprimé!', `${friend.username} a été supprimé de votre liste d'amis.`, 'success');
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
// // displayFriends();

// async function displayFriends() {
//     try {
//         const data = await retrieveUserData();
//         const friends = data.friends;
//         console.log('in displayFriends = ', friends);
//         if (friends && Array.isArray(friends)) {
//             const circlesContainer = document.getElementById('circlesContainer');
//             circlesContainer.innerHTML = ''; // Clear previous friends if any
//             friends.forEach(friend => {
//                 const newFriendDiv = document.createElement('div');
//                 newFriendDiv.className = 'friend-circle';

//                 // Determine color based on status
//                 let statusColor;
//                 switch (friend.status) {
//                     case 'en ligne': statusColor = 'green'; break;
//                     case 'en partie': statusColor = 'orange'; break;
//                     case 'hors ligne': statusColor = 'red'; break;
//                     default: statusColor = 'gray';
//                 }
//                 const username = friend.username;
//                 const avatarUrl = friend.avatar;
//                 // HTML structure for each friend
//                 newFriendDiv.innerHTML = `
//                     <div class="friend-avatar" style="background-image: url('${avatarUrl}');">
//                         <div class="friend-status" style="background-color: ${statusColor};"></div>
//                     </div>
//                     <div class="friend-name">${username}</div>
//                 `;
//                 circlesContainer.appendChild(newFriendDiv);
//                 window.location.href = '#friends';
//             });
//         } else {
//             console.error('Error: Friends list is not available or not an array', data);
//         }
//     } catch (error) {
//         console.error('Error: cannot display friends', error);
//         Swal.fire('Erreur', 'Une erreur est survenue lors de l\'affichage des amis.', 'error');
//     }
// }

// // $(document).ready(function () {
// //     async function getCSRFToken() {
// //         const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// //         if (!csrftoken)
// //             console.log('no csrf token generated');
// //         else {
// //             console.log('csrf token', csrftoken);
// //             return csrftoken;
// //         }
// //     }

// //     async function retrieveUserData(csrftoken) {
// //         const response = await fetch('/api/users/me/', {
// //             method: 'GET',
// //             headers: {
// //                 'Content-Type': 'application/json',
// //                 'X-CSRFToken': csrftoken,
// //             }
// //         });
// //         if (!response.ok) {
// //             throw new Error('Failed to fetch current user');
// //         }
// //         return await response.json();
// //     }

// //     async function getFriendByName(csrftoken, username) {
// //         try {
// //             const response = await fetch('api/users/', {
// //                 method: 'GET',
// //                 headers: {
// //                     'Content-Type': 'application/json',
// //                     'X-CSRFToken': csrftoken,
// //                 }
// //             });
// //             if (!response.ok) {
// //                 throw new Error('Network response was not ok');
// //             }
// //             const data = await response.json();
// //             console.log('data in getFriend = ', data);
// //             if (Array.isArray(data)) {
// //                 const user = data.find(user => user.username === username);
// //                 console.log('user = ', user);
// //                 return user || null;
// //             } else {
// //                 console.error('Fetched data is not an array:', data);
// //                 return null;
// //             }
// //         } catch (error) {
// //             console.error("Error fetching users", error);
// //             return null;
// //         }
// //     }

// //     async function addFriendToBackend(friend, userId, csrftoken) {
// //         const friendsToAdd = [friend.id];
// //         try {
// //             console.log('friend.username = ', friend.username);
// //             console.log('friend.status = ', friend.status);
// //             console.log('csrf = ', csrftoken);
// //             const response = await fetch(`api/users/add_friends/${userId}/`, {
// //                 method: 'PUT',
// //                 headers: {
// //                     'Content-Type': 'application/json',
// //                     'X-CSRFToken': csrftoken,
// //                 },
// //                 body: JSON.stringify({ add_friends: friendsToAdd })
// //             });
// //             const data = await response.json();
// //             if (data.success) {
// //                 Swal.fire('Ajout effectué!', `${friend.username} a été ajouté.`, 'success');
// //                 return data;
// //             } else {
// //                 Swal.fire('Erreur', data.message, 'error');
// //             }
// //         } catch (error) {
// //             Swal.fire('Erreur', 'Une erreur est survenue', 'error');
// //             console.error('error in adding friend to database', error);
// //         }
// //         return null;
// //     }

// //     async function inviteFriend() {
// //         try {
// //             const result = await Swal.fire({
// //                 title: 'Inviter un ami',
// //                 input: 'text',
// //                 inputLabel: 'Nom d\'utilisateur de l\'ami',
// //                 inputPlaceholder: 'Entrez le nom d\'utilisateur',
// //                 showCancelButton: true,
// //                 confirmButtonText: 'Envoyer l\'invitation',
// //                 cancelButtonText: 'Annuler',
// //             });

// //             if (result.isConfirmed) {
// //                 const username = result.value;
// //                 if (username) {
// //                     const csrfToken = await getCSRFToken();
// //                     const friend = await getFriendByName(csrfToken, username);
// //                     if (friend) {
// //                         const user = await retrieveUserData(csrfToken);
// //                         const userId = user.id;
// //                         await addFriendToBackend(friend, userId, csrfToken);
// //                     } else {
// //                         Swal.fire('Erreur', 'Utilisateur non trouvé', 'error');
// //                     }
// //                 } else {
// //                     Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
// //                 }
// //             }
// //         } catch (error) {
// //             Swal.fire('Erreur', 'Une erreur est survenue', 'error');
// //             console.error('error in invite friend', error);
// //         }
// //     }

// //     function promptDeleteFriend() {
// //         Swal.fire({
// //             title: 'Supprimer un ami',
// //             input: 'text',
// //             inputLabel: 'Nom d\'utilisateur de l\'ami',
// //             inputPlaceholder: 'Entrez le nom d\'utilisateur',
// //             showCancelButton: true,
// //             confirmButtonText: 'Supprimer',
// //             cancelButtonText: 'Annuler',
// //         }).then(async (result) => {
// //             if (result.isConfirmed) {
// //                 const username = result.value;
// //                 if (username) {
// //                     const csrfToken = await getCSRFToken();
// //                     const friend = await getFriendByName(csrfToken, username);
// //                     if (friend) {
// //                         const user = await retrieveUserData(csrfToken);
// //                         const userId = user.id;
// //                         deleteFriend(friend, csrfToken, userId);
// //                     } else {
// //                         Swal.fire('Erreur', 'Utilisateur non trouvé', 'error');
// //                     }
// //                 } else {
// //                     Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
// //                 }
// //             }
// //         });
// //     }

// //     async function deleteFriend(friend, csrftoken, userId) {
// //         const circlesContainer = document.getElementById('circlesContainer');
// //         const friendDiv = Array.from(circlesContainer.children).find(div => div.textContent.includes(friend.username));
// //         const friendsToDelete = [friend.id];
// //         if (friendDiv) {
// //             Swal.fire({
// //                 title: 'Êtes-vous sûr?',
// //                 text: `Voulez-vous vraiment supprimer ${friend.username} de votre liste d'amis?`,
// //                 icon: 'warning',
// //                 showCancelButton: true,
// //                 confirmButtonText: 'Oui, supprimer!',
// //                 cancelButtonText: 'Annuler'
// //             }).then((result) => {
// //                 if (result.isConfirmed) {
// //                     fetch(`api/users/add_friends/${userId}/`, {
// //                         method: 'PUT',
// //                         headers: {
// //                             'Content-Type': 'application/json',
// //                             'X-CSRFToken': csrftoken,
// //                         },
// //                         body: JSON.stringify({ remove_friends: friendsToDelete })
// //                     })
// //                     .then(response => response.json())
// //                     .then(data => {
// //                         if (data.success) {
// //                             circlesContainer.removeChild(friendDiv);
// //                             Swal.fire('Supprimé!', `${friend.username} a été supprimé de votre liste d'amis.`, 'success');
// //                         } else {
// //                             Swal.fire('Erreur', data.message, 'error');
// //                         }
// //                     })
// //                     .catch(error => {
// //                         Swal.fire('Erreur', 'Une erreur est survenue', 'error');
// //                     });
// //                 }
// //             });
// //         } else {
// //             Swal.fire('Erreur', 'Ami non trouvé', 'error');
// //         }
// //     }

// //     // Attach functions to window object to be callable from HTML
// //     window.inviteFriend = inviteFriend;
// //     window.promptDeleteFriend = promptDeleteFriend;
// // });

// // console.log('friends.js');

// // getMenuInfos();
// // displayFriends();

// // function getCSRFToken() {
// //         return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// //     }

// // function displayCSRFToken(){
// //     const csrftoken = getCSRFToken();
// //     if (!csrftoken)
// //         console.log('no csrf token generated');
// //     else {
// //         console.log('csrf token', csrftoken);
// //         return csrftoken;
// //     }
// // };

// // //verifier que le username existe bien dans le fetch de data
// // async function getFriendByName(csrftoken, username) {
// //     try {            
// //         const response = await fetch('api/users/');
// //        if (!response.ok) {
// //             throw new Error('Network response was not ok');
// //             }
// //         const data = await response.json();
// //         console.log('data in getFriend = ', response)
// //         if (Array.isArray(data)) {
// //             // Check if the username exists in the data
// //             const user = data.find(user => user.username === username);
// //             console.log('user = ', user);
// //             // Return the user if found, otherwise return null
// //             return user || null;
// //         } else {
// //             console.error('Fetched data is not an array:', data);
// //             return null;
// //         }
// //     } catch (error) {
// //         console.error("Error fetching users", error);
// //         return null;
// //     }
// // };

// // async function retrieveUserData(csrftoken) {
// //     const response = await fetch('/api/users/me/', {
// //         method: 'GET',
// //         headers: {
// //             'Content-Type': 'application/json',
// //             'X-CSRFToken': csrftoken,
// //         }
// //     });
// //     if (!response.ok) {
// //         throw new Error('Failed to fetch current user');
// //     }
// //     return await response.json();
// // }

// async function inviteFriend() {
//     try {
//         const result = await Swal.fire({
//             title: 'Inviter un ami',
//             input: 'text',
//             inputLabel: 'Nom d\'utilisateur de l\'ami',
//             inputPlaceholder: 'Entrez le nom d\'utilisateur',
//             showCancelButton: true,
//             confirmButtonText: 'Envoyer l\'invitation',
//             cancelButtonText: 'Annuler',
//         });

//         if (result.isConfirmed) {
//             const username = result.value;
//             if (username) {
//                 const csrfToken = displayCSRFToken();
//                 const friend = await getFriendByName(csrfToken, username);
//                 if (friend) {
//                     const user = await retrieveUserData(csrfToken);
//                     const userId = user.id;
//                     await addFriendToBackend(friend, userId, csrfToken);
//                 } else {
//                     Swal.fire('Erreur', 'Utilisateur non trouvé', 'error');
//                 }
//             } else {
//                 Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//             }
//         }
//     } catch (error) {
//         Swal.fire('Erreur', 'Une erreur est survenue', 'error');
//         console.error('error in invite friend', error);
//     }
// }

// async function addFriendToBackend(friend, userId, csrftoken) {
//     let friendsToAdd = [friend.id];
//     try {
//         console.log('friend.username = ', friend.username);            
//         console.log('friend.status = ', friend.status);
//         console.log('csrf = ', csrftoken);
//         console.log('self.data= ', data);
//        const response = await fetch(`api/users/add_friends/${userId}/`, {
//             method: 'PUT',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': csrftoken
//             },
//             body: JSON.stringify({ add_friends: friendsToAdd })
//         })
//         if (response.success) {
//             Swal.fire('Ajout effectué!', `${friend.username} a été ajouté.`, 'success');
//             return await response.json();     
//         } 
//         else {
//             Swal.fire('Erreur', response.message, 'error');
//         }
//     } catch (error) {
//         Swal.fire('Erreur', 'Une erreur est survenue', 'error');
//         console.error('error in addind friend to database', error);
//     }
// }   

// // function ok
// async function displayFriends() {
//     const csrfToken = displayCSRFToken();
//     try{
//         const data = await retrieveUserData(csrfToken);
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


/*Swal.fire c'est une function pour alerte doc pour biblio lien(https://sweetalert.js.org/docs/)*/
// async function inviteFriend(){
//     const result = await Swal.fire({
//     title: 'Ajouter un ami',
//     input: 'text',
//     inputLabel: 'Nom d\'utilisateur de l\'ami',
//     inputPlaceholder: 'Entrez le nom d\'utilisateur',
//     showCancelButton: true,
//     confirmButtonText: 'Confirmer l\'ajout',
//     cancelButtonText: 'Annuler',
// });

// if (result.isConfirmed) {
//     const username = result.value;
    
//     if (username) {
//         try {
//             const user = await getFriendByName(username);
//             console.log('in inviteFriend,  user = ', user);
//             if (user) {
//                 const reponse = await addFriendToBackend(user);
//                 if (response.error)
//                     console.error('error in addind friend to database', error);
//                 else
//                     displayFriends();
//             } else {
//                 Swal.fire('Erreur', 'Utilisateur non trouvé', 'error');
//             }
//         } catch (error) {
//             Swal.fire('Erreur', 'Une erreur est survenue lors de l\'ajout de l\'ami', 'error');
//         }
//     } else {
//         Swal.fire('Erreur', 'Veuillez entrer un nom d\'utilisateur', 'error');
//     }
// }
// };

