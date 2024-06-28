console.log('accueil.js');


$(document).ready(function() {
  console.log('apres ready');

  let token = localStorage.getItem('access');
  let refreshToken = localStorage.getItem('refresh');

 
  console.log('Value of token in accueil:', token);
  console.log('Value of refreshToken in acceiul:', refreshToken);

  if (!token || token === 'undefined' || token === 'null' ||
      !refreshToken || refreshToken === 'undefined' || refreshToken === 'null') {
    console.log("jwt token is not here");
    window.location.href = '#login';
  } else {
    fetchData();
  }

  function fetchData(isRefresh = false) {
    fetch('/protected/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    .then(response => {
      if (response.status === 401 && !isRefresh) {
        // Token expired, try to refresh
        return refreshAccessToken().then(() => fetchData(true));
      }
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    })
    .then(data => {
      console.log(data); // Log the response data
      // Update the HTML with the username only if it's not a refresh operation
      if (!isRefresh && data.username) {
        $('#userLogin').text(data.username);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      displayError('An unexpected error occurred.');
    });
  }

  function refreshAccessToken() {
    return fetch('token_refresh/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to refresh token');
      }
      return response.json();
    })
    .then(data => {
      console.log('Token refresh successful:', data);
      localStorage.setItem('access', data.access);
      token = data.access;
      return data.access;
    })
    .catch(error => {
      console.error('Error refreshing token:', error);
      // Handle refresh token failure (e.g., redirect to login)
      window.location.href = '#login';
    });
  }

  function displayError(errorMessage) {
    $('#error-message').text(errorMessage);
  }
});




