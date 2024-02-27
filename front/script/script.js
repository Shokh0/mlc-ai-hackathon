// script.js
// document.addEventListener("DOMContentLoaded", () => {
    
// });

var user = {
    'login': null,
} 


if (document.title == "eduChat"){

    const textarea = document.getElementById("myTextarea");
    const textareaWrapper = document.getElementById("textareaWrapper");
    
    function delFewElement() {
        var welcomTextToDelete = document.getElementById("welcomTextToDelete");
        var helpBlockToDelete = document.getElementById("helpBlockToDelete");
        welcomTextToDelete.parentNode.removeChild(welcomTextToDelete);
        helpBlockToDelete.parentNode.removeChild(helpBlockToDelete);
    }

    function resizeTextarea() {
        textareaWrapper.style.height = "";
        textarea.style.height = "";
        textarea.style.height = textarea.scrollHeight + "px"; // Установить высоту равной высоте textarea
        textareaWrapper.style.height = parseInt(textarea.scrollHeight) + 25 + "px"; // Установить высоту равной высоте textarea
    }

    function getTextareaData(event) {
        if (event.key === "Enter" && event.shiftKey) {
            // Не обрабатывать комбинацию Shift + Enter
             return;
        }
        if (event.key === "Enter") { // Обработка нажатия клавиши Enter
            event.preventDefault(); // Отменяем стандартное действие клавиши Enter (перенос на новую строку)
            const enteredText = textarea.value.trim(); // Получаем введенный текст и удаляем лишние пробелы
            console.log("Введенный текст:", enteredText); // Выводим введенный текст в консоль (можно изменить на другое действие)
            textarea.value = ""; // Очищаем textarea\
            
            const messageList = document.getElementById("message-list");
            const userP = document.createElement("p");
            const userPre = document.createElement("pre");
            userP.textContent = 'You';
            userPre.textContent = enteredText;
            messageList.appendChild(userP)
            messageList.appendChild(userPre)
            // Ai answer
            // Api request
            const aiP = document.createElement("p");
            const aiPre = document.createElement("pre");
            aiP.textContent = 'Ai';
            aiPre.textContent = 'Sorry i`m just fucked up. Answer me to the text time ;)';
            messageList.appendChild(aiP)
            messageList.appendChild(aiPre)
            delFewElement()
            resizeTextarea()
        }
    }
    textarea.addEventListener("input", resizeTextarea);
    textarea.addEventListener("keyup", resizeTextarea);
    textarea.addEventListener("keydown", resizeTextarea);
    textarea.addEventListener("keypress", getTextareaData);


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