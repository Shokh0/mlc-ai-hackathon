import { text } from './module.js';



document.addEventListener("DOMContentLoaded", function() {
    const hello = document.getElementById("hello");


    hello.addEventListener('click', function(){
        hello.textContent = text;
    });
});