const get_button = document.getElementById('gt_st_btn');
const logout_a = document.getElementById('logout_a');


//get username from localstorage
const username = localStorage.getItem('username');

//check if username is in localstorage
//display welcome back message and change button text to go to market as user is logged in
if(username){
    get_button.innerHTML = `Go to market`;
    let welcome_message = document.getElementById('h_header');
    welcome_message.innerHTML = `Welcome back <span class="app-name">${username.toUpperCase()}</span>`;
    let del = document.getElementById('wlc_message');
    del.remove();
}

//if user logged out remove username from localstorage and redirect to home page
if(logout_a){
    logout_a.addEventListener('click', () => {
        localStorage.removeItem('username');
        window.location.href = '/';
    });
}

//redirect to market page
get_button.addEventListener('click', () => {
    window.location.href = '/market';
});