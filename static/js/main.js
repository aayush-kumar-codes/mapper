if (document.querySelector('.main-footer')) {
    document.querySelector('.main-footer').firstChild.nextSibling.remove();
}

if (document.getElementById('jazzy-logo')) {
    document.getElementById('jazzy-logo').firstChild.nextSibling.remove();
}

if (document.querySelector('.login-logo')) {
    document.querySelector('.login-logo').firstChild.nextSibling.remove();
}

if (document.getElementsByClassName('.jazzmin-login-page')) {
    const loginBoxMsg = document.querySelector('.login-box-msg');
    loginBoxMsg.textContent = "Welcome!";
    loginBoxMsg.style.fontWeight = "900";
    loginBoxMsg.style.fontSize = "1.8rem";
    loginBoxMsg.style.marginBottom = "20px";
    document.querySelector('.card-body').style.height = '20rem';
}