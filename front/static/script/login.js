import { config } from './modules/config.js';

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

const searchAuthorizationButtonImg = document.getElementById('loginButton');

searchAuthorizationButtonImg.addEventListener('click', function() {
    // Ваш код для выполнения действия при нажатии на изображение
    
    const inputGmail = document.getElementById('input-login').value.trim();
    const inputPassword = document.getElementById('input-password').value.trim();
    console.log(`${inputGmail} ${inputPassword}`);

    // URL адрес вашего API
    const url = `${config.base_url}/api/login`;

    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };
    const data = {
        'gmail': inputGmail,
        'password': inputPassword,
    };
    apiRequest("POST", url, headers, data, function(jsonResponse){
        if (jsonResponse['status'] == true){
            // user.login = inputGmail;
            // console.log(jsonResponse["url"]);
            window.location.href = jsonResponse["url"];
        }
    })
});