function demarrerJeu() {
  console.log("Préparation du jeu...");
  var i = 0;
  var interval = setInterval(function() {
    if (i >= 5) {
      clearInterval(interval);
      window.location.href = 'Pong-Game/AI3D.html'; // URL de votre jeu
    } else {
      var rect = document.createElement('div');
      rect.className = 'rectangle';
      document.getElementById('loadingBar').appendChild(rect);
      setTimeout(function() { rect.style.opacity = 1; }, 100);
    }
    i++;
  }, 1000);
}