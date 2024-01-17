const username = document.getElementById('username');
const logout_a = document.getElementById('logout_a');

let user = username.innerHTML;

localStorage.setItem('username', user);



logout_a.addEventListener('click', () => {
    localStorage.removeItem('username');
});
