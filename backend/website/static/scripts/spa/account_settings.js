console.log('accout_settings.js');


document.getElementById('avatar-btn').addEventListener('click', function() {
    document.getElementById('avatar').click();
});

document.getElementById('avatar').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatar-img').src = e.target.result;
            document.getElementById('avatar-sidebar').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

$('#accountSettingsForm').on('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    $.ajax({
        type: 'POST',
        url: 'account_settings/',  // Your form action URL
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            alert('Informations mises à jour avec succès');
            window.location.href = '#account_settings';
        },
        error: function(response) {
            const errorMessage = response.responseJSON ? JSON.stringify(response.responseJSON) : 'Erreur lors de la mise à jour des informations';
            $('#error-message').text(errorMessage).show();
        }
    });
});

$('#passwordChangeForm').on('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),  // Get form action URL dynamically
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            alert('Votre mot de passe a été mis à jour avec succès');
            window.location.href = '#account_settings';  // Redirect to account settings
        },
        error: function(response) {
            const errorMessage = response.responseJSON ? JSON.stringify(response.responseJSON) : 'Erreur lors de la mise à jour du mot de passe';
            $('#error-message').text(errorMessage).show();
        }
    });
});

