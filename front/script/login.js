// login.js
// document.addEventListener("DOMContentLoaded", () => {
    
// });
                   
const searchYuthorizationButtonImg = document.getElementById('authorizationButton-img');

searchYuthorizationButtonImg.addEventListener('click', function() {
    // Ваш код для выполнения действия при нажатии на изображение
    
    const inputLogin = document.getElementById('input-login').value.trim();
    const inputPassword = document.getElementById('input-password').value.trim();
    alert(`${inputLogin} ${inputPassword}`);

    // URL адрес вашего API
    const url = 'http://127.0.0.1:80/api/login';

    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };

    const data = {
        'login': inputLogin,
        'password': inputPassword,
    };

    var request = new XMLHttpRequest();
    request.open("POST", url);
    Object.keys(headers).forEach(key => {
        request.setRequestHeader(key, headers[key]);
    });
    
    request.onload = function() {
        if (request.status === 200) {
            const jsonResponse = JSON.parse(request.responseText); // парсим JSON
            console.log(jsonResponse); // выводим результат в консоль
            // const books = jsonResponse['books'];
            // const bookList = document.getElementById("book-list");
            
            // for (let book of books) {
            //     // console.log(book);
            //     const li = document.createElement("li");
            //     li.textContent = book;
            //     bookList.appendChild(li);
            // }
        } else {
            console.error('Ошибка при выполнении запроса:', request.statusText);
        }
    };
    
    request.onerror = function() {
        console.error('Ошибка сети');
    };

    request.send();

});

