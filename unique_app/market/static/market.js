const username = document.getElementById('username');
const logout_a = document.getElementById('logout_a');

let user = username.innerHTML;

//set username in localstorage once entered /market
localStorage.setItem('username', user);


//if user logged out remove username from localstorage
logout_a.addEventListener('click', () => {
    localStorage.removeItem('username');
});
