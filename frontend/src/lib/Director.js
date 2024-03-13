const BASE_URL = 'https://127.0.0.1:8080';

const getToken = () => {
  return localStorage.getItem('token');
};

const getHeaders = (form) => {
  let headers = {}
  if (form) {
  
  } else {
    headers = {
      'Content-Type': 'application/json',
    };
  }
  const token = getToken();
  if (token) {
    headers.Authorization = `Token ${token}`;
  }
  return headers;
};

export const director = async (url, method = 'GET', data = null, form=false) => {
  const headers = getHeaders(form);
  const config = {
    method: method,
    headers: headers,
  };

  if (data) {
    config.body = form ? data : JSON.stringify(data);
  }


  try {
    const response = await fetch(`${BASE_URL}/${url}`, config);
    const responseData = await response.json();
    if (!response.ok) {
      throw new Error(responseData.detail || 'Une erreur est survenue');
    }
    
    return responseData;
  } catch (error) {
    console.error('Erreur lors de la requête :', error.message);
    throw error;
  }
};