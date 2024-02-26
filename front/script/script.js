// script.js
// document.addEventListener("DOMContentLoaded", () => {
    
// });

var user = {
    'login': null,
} 


if (document.title == "eduChat"){

    const textarea = document.getElementById("myTextarea");
    const textareaWrapper = document.getElementById("textareaWrapper");
    
    function resizeTextarea() {
        textareaWrapper.style.height = "";
        textarea.style.height = "";
        textarea.style.height = textarea.scrollHeight + "px"; // Установить высоту равной высоте textarea
        textareaWrapper.style.height = parseInt(textarea.scrollHeight) + 25 + "px"; // Установить высоту равной высоте textarea
    }
    textarea.addEventListener("input", resizeTextarea);
    textarea.addEventListener("keyup", resizeTextarea);
    textarea.addEventListener("keydown", resizeTextarea);

    document.addEventListener("DOMContentLoaded", () => {
        console.log(document.title)

            const url = 'http://127.0.0.1:80/api/getTopics';

            const headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            };
        
            const data = {
                'login':  'andrew', // user.login,
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
                    const topics = jsonResponse['topics'];
                    const topicList = document.getElementById("topic-list");
                    
                    for (let topic of topics) {
                        // console.log(book);
                        const p = document.createElement("p");
                        p.textContent = topic;
                        topicList.appendChild(p);
                    }
                } else {
                    console.error('Ошибка при выполнении запроса:', request.statusText);
                }
            };
            
            request.onerror = function() {
                console.error('Ошибка сети');
            };

            request.send(JSON.stringify(data));
    });
}


if (document.title == "login"){

    const searchAuthorizationButtonImg = document.getElementById('authorizationButton-img');

    searchAuthorizationButtonImg.addEventListener('click', function() {
        // Ваш код для выполнения действия при нажатии на изображение
        
        const inputLogin = document.getElementById('input-login').value.trim();
        const inputPassword = document.getElementById('input-password').value.trim();
        console.log(`${inputLogin} ${inputPassword}`);

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
                if (jsonResponse['status'] == true){
                    user.login = inputLogin;
                    window.location.href = "http://127.0.0.1:5500/front/ai-chat.html";
                }
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

        request.send(JSON.stringify(data));

    });
}