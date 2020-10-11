if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('/service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered!');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}
document.querySelector('head').insertAdjacentHTML('afterbegin', ` 
<title>Sohbeting</title>
<style>
    :root {
        --color-0: #f5f5f5;
        --color-1: #adb5bb;
        --color-2: #3d6d8f;
        --color-3: #114d78;
        --color-4: #093657;
        --color-5: #001726;
    }
</style>
<link rel="apple-touch-icon" sizes="180x180" href="/meta/apple-touch-icon.png">
<link rel="apple-touch-startup-image" href="/meta/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Sohbeting">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="#114d78">
<link rel="icon" type="image/png" sizes="32x32" href="/meta/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/meta/favicon-16x16.png">
<link rel="manifest" href="/meta/site.webmanifest">
<link rel="mask-icon" href="/meta/safari-pinned-tab.svg" color="#5bbad5">
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="theme-color" content="#ffffff">
<meta name="viewport"    content="width=device-width, initial-scale=1, shrink-to-fit=no">
<meta name="description" content="Lightweight browser chat application.">
<link rel="stylesheet" href="/css/global.css">
`)