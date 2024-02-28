// script.js

function apiRequest(method, url, headers, data = null, callback) {
       

    const fetchOptions = {
        method: method,
        headers: headers,
        mode: 'cors', // В реальном примере могут быть другие настройки
    };

    if (data !== null) {
        fetchOptions.body = JSON.stringify(data);
    }

    fetch(url, fetchOptions)
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при выполнении запроса: ' + response.statusText);
        }
        return response.json();
    })
    .then(jsonResponse => {
        console.log('jsonResponse', jsonResponse);
        callback(jsonResponse);
    })
    .catch(error => {
        console.error('Произошла ошибка:', error.message);
    });
}

var user = {
    'login_id': null,
    'topic_id': null,
} 

function getUserIdAndTopicId(func = null){
    const url = 'http://127.0.0.1:80/api/getUserIdAndTopicId';
            
    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };

    const data = {
        'something': 'something',
    }

    apiRequest("POST", url, headers, data, function (jsonResponse) {
        login_id = jsonResponse['user_id'];
        topic_id = jsonResponse['topic_id'];
        user.login_id = login_id;
        user.topic_id = topic_id;
        console.log('login id: ', user.login_id);
        console.log('topic id: ', user.topic_id);
        if (func != null){
            func();
        }
    });
}


function safeSubstring(str, endValue) {
    let end = Math.min(endValue, str.length); // Начальное значение для конечного индекса

    while (end > 0) {
        try {
            return str.substring(0, end); // Пытаемся создать срез
        } catch (error) {
            if (error instanceof RangeError) {
                // Если возникает ошибка "index out of range", уменьшаем конечный индекс
                end--;
            } else {
                // Если возникает другая ошибка, выбрасываем исключение
                throw error;
            }
        }
    }

    return ''; // Если не удалось создать срез
}

function scrollContainerDown() {
    var container = document.getElementById('message-list');
    container.scrollTop = container.scrollHeight;
}


function getTopics(){
    console.log(document.title)

    if (user.topic_id != null){
        getMessages(user.topic_id);
    }     
    const url = 'http://127.0.0.1:80/api/getTopics';

    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };
    console.log('login_id: ', user.login_id)
    const data = {
        'login_id': user.login_id, // user.login,
    };
    
    apiRequest("POST", url, headers, data, function(jsonResponse) {
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
            a.href = `#${topic[0]}`;
            p.appendChild(a);
            topicList.appendChild(p);
        }   
        const elements = document.querySelectorAll('.topicName');
        // console.log('Elemnt id', elements);
        
        // Добавляем обработчик события для каждого элемента
        for (let element of elements) {
            element.addEventListener('click', function() {
                // console.log('Вы нажали на абзац.', element);
                console.log('Вы нажали на абзац c id', element.id);
                user.topic_id = element.id;
                getMessages(element.id);
            });
        }      
    });
}

function getMessages(topic_id) {
    const url = 'http://127.0.0.1:80/api/getMessage';
        
    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };
    const data = {
        'user_id': user.login_id, 
        'topic_id': topic_id,
    };  
    console.log('login_id: ', user.login_id)
    console.log('topic_id: ', topic_id)

    apiRequest("POST", url, headers, data, function (jsonResponse){
        console.log('messages: ', jsonResponse)
        const messages = jsonResponse['messages'];
        const messageList = document.getElementById("message-list");
        try{
            delFewElement();
        } catch (error) {
            // Обработка ошибки
            console.log("Произошла ошибка:", error.message);
        }
        try{
            // Находим элемент, у которого нужно удалить все дочерние элементы
            var parentElement = document.getElementById("message-list");
            
            // Удаляем все дочерние элементы
            while (parentElement.firstChild) {
                parentElement.removeChild(parentElement.firstChild);
            }
        } catch (error) {
            console.log("Произошла ошибка:", error.message);
        }
        for (var message of messages) {
            if (message[4] == 0){
                const messageList = document.getElementById("message-list");
                const userP = document.createElement("p");
                const userPre = document.createElement("pre");
                userP.textContent = 'You';
                userPre.textContent = message[3];
                messageList.appendChild(userP);
                messageList.appendChild(userPre);
            }else{
                const aiAnswer = 'Sorry i`m just fucked up. Answer me to the text time ;)';
                const aiP = document.createElement("p");
                const aiPre = document.createElement("pre");
                aiP.textContent = 'Ai';
                aiPre.textContent = message[3];
                messageList.appendChild(aiP);
                messageList.appendChild(aiPre);    
            }
        }
        scrollContainerDown();
    })
}


document.addEventListener("DOMContentLoaded", () => {
    getUserIdAndTopicId(getTopics);
});


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
        const url = 'http://127.0.0.1:80/api/lamini';
    
        const headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        };
        const data = {
            'question': enteredText,
        };  
        const messageList = document.getElementById("message-list");
        const userP = document.createElement("p");
        const userPre = document.createElement("pre");
        userP.textContent = 'You';
        userPre.textContent = enteredText;
        messageList.appendChild(userP);
        messageList.appendChild(userPre);
        apiRequest("POST", url, headers, data, function (jsonResponse) {
            
            // Api request
            // Ai answer
            
            // const aiAnswer = 'Sorry i`m just fucked up. Answer me to the text time ;)';
            const aiAnswer = jsonResponse['message'];
            const aiP = document.createElement("p");
            const aiPre = document.createElement("pre");
            aiP.textContent = 'Ai';
            aiPre.textContent = aiAnswer;
            messageList.appendChild(aiP);
            messageList.appendChild(aiPre);
    
            scrollContainerDown();
            resizeTextarea();
            try{
                delFewElement();
            } catch (error) {
                // Обработка ошибки
                console.log("Произошла ошибка:", error.message);
            }
            const message_url = 'http://127.0.0.1:80/api/addMessage';
    
            const user_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            };
            const ai_headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            };
            const user_data = {
                'topic_id': user.topic_id, 
                'content': enteredText, 
                'is_ai': 0,
            };
            const ai_data = {
                'topic_id': user.topic_id, 
                'content': aiAnswer, 
                'is_ai': 1,
            };
            
            if (user.topic_id == null) {
                const topicTitle = safeSubstring(enteredText, 20);
                const topic_url = 'http://127.0.0.1:80/api/addTopic';
            
                const headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                };
                const data = {
                    'user_id': user.login_id, 
                    'title': topicTitle,
                };    
                console.log('topicTitle: ', topicTitle);
                console.log('user.login_id: ', user.login_id);
            
                // Отправляем запрос на добавление топика
                apiRequest("POST", topic_url, headers, data, function(jsonResponse) {
                    user.topic_id = jsonResponse['topic_id'];
                    console.log('user.topic_id: ', user.topic_id);
                    // alert('addTopic response: ' + user.topic_id);
            
                    const user_data = {
                        'topic_id': jsonResponse['topic_id'],
                        'content': enteredText, 
                        'is_ai': 0,
                    };
                    const ai_data = {
                        'topic_id': jsonResponse['topic_id'],
                        'content': aiAnswer, 
                        'is_ai': 1,
                    };    
                    // Отправляем запросы на добавление сообщений пользователя и AI
                    apiRequest("POST", message_url, user_headers, user_data, function(jsonResponse) {
                        console.log(jsonResponse['message']);
                        apiRequest("POST", message_url, ai_headers, ai_data, function(jsonResponse) {
                            console.log(jsonResponse['message']);
                            // console.log('addMessage');
                            getMessages(user.topic_id);
                        });
                    });
                });
            } else {
                // Если у пользователя уже есть топик, просто отправляем сообщения
                apiRequest("POST", message_url, user_headers, user_data, function(jsonResponse) {
                    console.log(jsonResponse['message']);
                    apiRequest("POST", message_url, ai_headers, ai_data, function(jsonResponse) {
                        console.log(jsonResponse['message']);
                    });
                });
            }                   
        });
    }
}

function getNewChat() {
    const url = 'http://127.0.0.1:80/api/newChat';
        
    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };
    const data = {
        'something': 'something', 
    };

    apiRequest("POST", url, headers, data, function(jsonResponse){
        console.log(jsonResponse);
        user.topic_id = null;
    });
}

const newChat = document.getElementById('new-chat');

newChat.addEventListener('click', getNewChat);
textarea.addEventListener("input", resizeTextarea);
textarea.addEventListener("keyup", resizeTextarea);
textarea.addEventListener("keydown", resizeTextarea);
textarea.addEventListener("keypress", getTextareaData);