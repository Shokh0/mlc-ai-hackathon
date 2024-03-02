// import { config } from './modules/config.js';
const config = {
    base_url: 'http://127.0.0.1:80', // 'http://26.142.248.33:80'
}

const loginButton = document.getElementById("loginButton"); 
loginButton.addEventListener("click", function(){
    // conso
    window.location.href = `${config.base_url}/login`;
});