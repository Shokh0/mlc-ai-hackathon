


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
            // user.login = inputLogin;
            // console.log(jsonResponse["message"]);
            window.location.href = jsonResponse["message"];
        }
    })
});