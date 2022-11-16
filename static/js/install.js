const serviceWorkerPath = "/serviceworker.js";
const divInstall = document.getElementById("installContainer");
const butInstall = document.getElementById("butInstall");


if ("serviceWorker" in navigator) {
	navigator.serviceWorker
		.register(serviceWorkerPath)
		.then(function(response) {
			console.log("laregina service worker registered");
		}).catch(function(error) {
			console.log(error);
		});
}

butInstall.addEventListener('click', async () => {
	console.log('👍', 'butInstall-clicked');
	const promptEvent = window.deferredPrompt;
	if (!promptEvent) {
		return;
	}
 	promptEvent.prompt();

  	const result = await promptEvent.userChoice;
  	console.log('👍', 'userChoice', result);
  	window.deferredPrompt = null;

  	divInstall.classList.toggle('hidden', true);
});

window.addEventListener('appinstalled', (event) => {
	console.log('👍', 'appinstalled', event);
  	window.deferredPrompt = null;
});
