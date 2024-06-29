console.log('logout.js');

// function changeStatus() {
//     getUserID()
//       .then(userId => {
//         console.log(userId);
//         return fetch(`/api/users/update/${userId}/`, {
//           method: 'PUT',
//           headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${token}`
//           },
//           body: JSON.stringify({ status: 'offline' }) // equivalent des serializer cote client, convertit 1 obj JS en une chaîne JSON.
//         });
//       })
//       .then(response => {
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         return response.json();
//       })
//       .then(data => {
//         if (data.username) {
//           window.location.href = '#login';
//         } else {
//           console.error('User not authenticated');
//         }
//       })
//       .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//       });
//   }
  