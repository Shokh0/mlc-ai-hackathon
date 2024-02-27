// script.js
// document.addEventListener("DOMContentLoaded", () => {
    
// });

var user = {
    'login_id': 1,
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


    function apiRequest(method, url, headers, data = null, callback) {
        
        var request = new XMLHttpRequest();
        request.open(method, url);
        Object.keys(headers).forEach(key => {
            request.setRequestHeader(key, headers[key]);
        });
        
        request.onload = function() {
            if (request.status === 200) {
                const jsonResponse = JSON.parse(request.responseText); // парсим JSON
                console.log('jsonResponse', jsonResponse); // выводим результат в консоль
                callback(jsonResponse);
            } else {
                console.error('Ошибка при выполнении запроса:', request.statusText);
            }
        };
        
        request.onerror = function() {
            console.error('Ошибка сети');
        };
        if (data != null) {
            request.send(JSON.stringify(data));
        }else{
            request.send();
        }
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
        // console.log(document.title)

        const url = 'http://127.0.0.1:80/api/getTopics';

        const headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        };
    
        const data = {
            'login_id': user.login_id, // user.login,
        };
        
        apiRequest("POST", url, headers, data, function(jsonResponse){
            console.log('jsonResponse 2', jsonResponse); // выводим результат в консоль
            const topics = jsonResponse['topics'];
            const topicList = document.getElementById("topic-list");
            
            for (let topic of topics) {
                // console.log(book);
                const p = document.createElement("p");
                const a = document.createElement("a");
                p.id = topic[0];
                p.className = 'topicName';
                a.textContent = topic[2];
                a.href = '#';
                p.appendChild(a);
                topicList.appendChild(p);
            }
            const elements = document.querySelectorAll('.topicName');
            console.log('Elemnt id', elements);
    
            // Добавляем обработчик события для каждого элемента
            for (let element of elements) {
                element.addEventListener('click', function() {
                    console.log('Вы нажали на абзац.', element);
                });
            }           
        });
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
        apiRequest("POST", url, headers, data, function(jsonResponse){
            if (jsonResponse['status'] == true){
                user.login = inputLogin;
                window.location.href = "http://127.0.0.1:5500/front/ai-chat.html";
            }
        })
    });
}