console.log('utils.js loaded');

const loadjQuery = () => {
   return new Promise((resolve, reject) => {
       if (typeof window.jQuery !== 'undefined') {
			console.log('jQuery already loaded');
           resolve(); // 
       } else {
           const script = document.createElement('script');
           script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
           script.onload = resolve;
           script.onerror = reject;
           document.head.appendChild(script);
       }
   });
};

async function getUserId() {
    try {
      const response = await fetch(`/api/users/me`);
      const data = await response.json();
      // Vérifier si l'utilisateur est authentifié
      if (data) {
          console.log('user.username', data.username);
          return data.id; // Retourner l'ID de l'utilisateur
        } else {
          console.error('User not authenticated in getMenuData');
        }
      }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
  };

async function retrieveUserData() {
    try {
      const response = await fetch(`/api/users/me`);
      const data = await response.json();
      // Vérifier si l'utilisateur est authentifié
      if (data) {
          console.log('user.username', data.username);
          return data; // Retourner l'ID de l'utilisateur
        } else {
          console.error('User not authenticated in getMenuData');
        }
      }
    catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
  };

async function getFriendData() {
    try {
        const userId = await getUserId();
        const response = await fetch(`api/users/retrieve_friends_data/${userId}/`);
        if (!response.ok) {
            throw new Error('Network response was not ok for friends data');
        }
        const friendsData = await response.json();
        console.log('friendsDta: ', friendsData.friend_request);
        return friendsData.friend_request; // Assurez-vous que `friend_request` est bien la clé correcte
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return [];
    }
}

async function getTourId(partyId) {
  try {
    const response = await fetch(`api/party/${partyId}/`);
    if (!response.ok) {
        throw new Error('Network response was not ok for friends data');
    }
    const partyData = await response.json();
    console.log('partyData: ', partyData.tour);
    return partyData.tour; // Assurez-vous que `friend_request` est bien la clé correcte
} catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    return [];
}

}
