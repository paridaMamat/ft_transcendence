$.ajax({
    url: '/api/users/',  // je ne sais pas c'est qu'elle api mais moi j'ai appelle comme sa
    method: 'GET',
    
    success: function(data) {
        if (data.length > 0) {
            //  user
            $('#userLogin').text((user.username));
            // avatar par default
            $('#avatar').attr('src', userAvatarURL);
        }           
    },
    error: function(xhr, status, error) {
        console.error("Erreur lors de la récupération des données: ", error);
    }
});