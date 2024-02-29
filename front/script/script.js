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
        if (user.topic_id == null) {
            addFewElement();
        }
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
        if (user.topic_id != null){
            getMessages(user.topic_id);
        }   
        // Добавляем обработчик события для каждого элемента
        for (let element of elements) {
            element.addEventListener('click', function() {
                // console.log('Вы нажали на абзац.', element);
                console.log('Вы нажали на абзац c id', element.id);
                // window.location.href = "http://127.0.0.1:5500/front/ai-chat.html";
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
    console.log('getMessages login_id: ', user.login_id)
    console.log('getMessages topic_id: ', topic_id)

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
            // // Находим элемент, у которого нужно удалить все дочерние элементы
            // var parentElement = document.getElementById("message-list");
            
            // // Удаляем все дочерние элементы
            // while (parentElement.firstChild) {
            //     parentElement.removeChild(parentElement.firstChild);
            // }
            delAllMessages();
        } catch (error) {
            console.log("Произошла ошибка:", error.message);
        }
        for (var message of messages) {
            if (message[4] == 0){
                const messageList = document.getElementById("message-list");
                const userP = document.createElement("p");
                const userPre = document.createElement("pre");
                userP.textContent = 'You:';
                userPre.textContent = message[3];
                messageList.appendChild(userP);
                messageList.appendChild(userPre);
            }else{
                // const aiAnswer = 'Sorry i`m just fucked up. Answer me to the text time ;)';
                const aiP = document.createElement("p");
                const aiPre = document.createElement("pre");
                aiP.textContent = 'EduChat:';
                aiPre.textContent = message[3];
                messageList.appendChild(aiP);
                messageList.appendChild(aiPre);    
            }
        }
        scrollContainerDown();
    })
}


document.addEventListener("DOMContentLoaded", () => {
    // try{
    //     delFewElement();
    // } catch (error) {
    //     // Обработка ошибки
    //     console.log("Произошла ошибка:", error.message);
    // }
    
    getUserIdAndTopicId(getTopics);
});


const textarea = document.getElementById("myTextarea");
const textareaWrapper = document.getElementById("textareaWrapper");

function delAllMessages() {
    // Находим элемент, у которого нужно удалить все дочерние элементы
    var parentElement = document.getElementById("message-list");
            
    // Удаляем все дочерние элементы
    while (parentElement.firstChild) {
        parentElement.removeChild(parentElement.firstChild);
    }
}

function delFewElement() {
    var welcomTextToDelete = document.getElementById("welcomTextToDelete");
    var helpBlockToDelete = document.getElementById("helpBlockToDelete");
    welcomTextToDelete.parentNode.removeChild(welcomTextToDelete);
    helpBlockToDelete.parentNode.removeChild(helpBlockToDelete);
}

function addFewElement() {
    // Создаем элементы
    var imageElement = document.createElement("img");
    imageElement.id = "welcomTextToDelete";
    imageElement.className = "chat-header-welcome-text";
    imageElement.src = "media\\svg\\chat\\header.svg";
    imageElement.alt = "chat header";

    // Создаем элементы
    var helpBlockContainer = document.createElement("div");
    helpBlockContainer.id = "helpBlockToDelete";
    helpBlockContainer.className = "chat-help-blocks-container";

    var column1 = document.createElement("div");
    column1.className = "chat-help-blocks-container-column";
    column1.innerHTML = "<p><b>Solve equation in two variables...</b></p><p><b>Choose OKVED for a coffee shop...</b></p>";

    var column2 = document.createElement("div");
    column2.className = "chat-help-blocks-container-column";
    column2.innerHTML = "<p><b>All Newton's laws...</b></p><p><b>Build a demand schedule...</b></p>";

    // Добавляем элементы в DOM
    helpBlockContainer.appendChild(column1);
    helpBlockContainer.appendChild(column2);

    // Добавляем созданный блок в нужное место в DOM
    var parentElement = document.getElementById("chat-space"); // Замените "parentElementId" на ID элемента, куда вы хотите добавить созданный блок
    parentElement.appendChild(imageElement);
    parentElement.appendChild(helpBlockContainer);

}

function resizeTextarea() {
    textareaWrapper.style.height = "";
    textarea.style.height = "";
    textarea.style.height = textarea.scrollHeight + "px"; // Установить высоту равной высоте textarea
    textareaWrapper.style.height = parseInt(textarea.scrollHeight) + 25 + "px"; // Установить высоту равной высоте textarea
}

function enterData () {
    const enteredText = textarea.value.trim(); // Получаем введенный текст и удаляем лишние пробелы
    console.log("Введенный текст:", enteredText); // Выводим введенный текст в консоль (можно изменить на другое действие)
    if (enteredText == "") {
        return null;
    }
    try{
        delFewElement();
    } catch (error) {
        // Обработка ошибки
        console.log("Произошла ошибка:", error.message);
    }
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
    userP.textContent = 'You:';
    userPre.textContent = enteredText;
    messageList.appendChild(userP);
    messageList.appendChild(userPre);

    apiRequest("POST", url, headers, data, function (jsonResponse) {
    
        // const aiAnswer = 'Sorry i`m just fucked up. Answer me to the text time ;)';
        const aiAnswer = jsonResponse['message'];
        const aiP = document.createElement("p");
        const aiPre = document.createElement("pre");
        aiP.textContent = 'EduChat:';
        aiPre.textContent = aiAnswer;
        messageList.appendChild(aiP);
        messageList.appendChild(aiPre);

        const message_url = 'http://127.0.0.1:80/api/addMessage';

        const headers = {
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

                const message_url = 'http://127.0.0.1:80/api/addMessage';
                const headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                };
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
                apiRequest("POST", message_url, headers, user_data, function(jsonResponse) {
                    console.log(jsonResponse['message']);
                });
                apiRequest("POST", message_url, headers, ai_data, function(jsonResponse) {
                    console.log(jsonResponse['message']);
                });
            });
        } else {
            // Если у пользователя уже есть топик, просто отправляем сообщения
            apiRequest("POST", message_url, headers, user_data, function(jsonResponse) {
                console.log(jsonResponse['message']);
            });
            apiRequest("POST", message_url, headers, ai_data, function(jsonResponse) {
                console.log(jsonResponse['message']);
            });
        }
        scrollContainerDown();
        resizeTextarea();                   
    });
}

function getTextareaData(event) {
    
    if (event.key === "Enter" && event.shiftKey) {
        // Не обрабатывать комбинацию Shift + Enter
        return;
    }
    if (event.key === "Enter") { // Обработка нажатия клавиши Enter
        event.preventDefault(); // Отменяем стандартное действие клавиши Enter (перенос на новую строку)
        enterData();
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
        delAllMessages();
        addFewElement();
    });
}

const newChat = document.getElementById('new-chat');
const inputIcon = document.getElementById('inputIcon');

newChat.addEventListener('click', getNewChat);
inputIcon.addEventListener("click", enterData);
textarea.addEventListener("input", resizeTextarea);
textarea.addEventListener("keyup", resizeTextarea);
textarea.addEventListener("keydown", resizeTextarea);
textarea.addEventListener("keypress", getTextareaData);