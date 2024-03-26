const http = require('http');
const fs = require('fs');
const querystring = require('querystring'); // Importer le module querystring pour analyser les données de requête URL encodées

const server = http.createServer((req, res) => {
  console.log('Requête reçue :', req.method, req.url);

  if (req.method === 'POST' && req.url === '/enregistrer') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      console.log('Données reçues :', body);
      
      // Analyser les données de la requête URL encodée en un objet JavaScript
      const formData = querystring.parse(body);
      
      // Enregistrer les données dans un fichier JSON
      fs.writeFile('donnees.json', JSON.stringify(formData), { flag: 'a+' }, err => {
        if (err) {
          console.error('Erreur lors de l\'enregistrement des données :', err);
          res.writeHead(500, {'Content-Type': 'text/plain'});
          res.end('Erreur lors de l\'enregistrement des données');
          return;
        }
        console.log('Les données ont été ajoutées avec succès à donnees.json');
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end('Données enregistrées avec succès');
      });
    });
  } else {
    fs.readFile('index.html', (err, data) => {
      if (err) {
        console.error('Erreur lors de la lecture du fichier HTML :', err);
        res.writeHead(500, {'Content-Type': 'text/plain'});
        res.end('Erreur lors de la lecture du fichier HTML');
        return;
      }
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(data);
    });
  }
});

const PORT = process.env.PORT || 9898;
server.listen(PORT, () => {
  console.log(`Serveur en cours d'exécution sur le port ${PORT}`);
});

