function loadScriptsSequentially(scriptUrls) {
    let i = 0;

    function loadNextScript() {
        if (i >= scriptUrls.length) {
            return; // All scripts loaded
        }

        const script = document.createElement('script');
        script.src = scriptUrls[i];
        script.onload = loadNextScript;
        document.head.appendChild(script);
        i++;
    }

    loadNextScript();
}

const scriptUrls = [
    "{% static 'scripts/spa/protected.js' %}",
    "{% static 'scripts/spa/accueil.js' %}"
];

loadScriptsSequentially(scriptUrls);
