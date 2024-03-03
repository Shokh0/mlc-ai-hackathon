import { config } from './modules/config.js';


const loginButton = document.getElementById("loginButton"); 
loginButton.addEventListener("click", function(){
    // conso
    window.location.href = `${config.base_url}/login`;
});