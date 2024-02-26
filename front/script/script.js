// script.js
document.addEventListener("DOMContentLoaded", () => {
    const url = 'http://127.0.0.1:80/api/books';
    var request = new XMLHttpRequest();
    request.open("GET", url);
    
    request.onload = function() {
        if (request.status === 200) {
            const jsonResponse = JSON.parse(request.responseText); // парсим JSON
            console.log(jsonResponse); // выводим результат в консоль
            const books = jsonResponse['books'];
            const bookList = document.getElementById("book-list");
            
            for (let book of books) {
                // console.log(book);
                const li = document.createElement("li");
                li.textContent = book;
                bookList.appendChild(li);
            }
        } else {
            console.error('Ошибка при выполнении запроса:', request.statusText);
        }
    };
    
    request.onerror = function() {
        console.error('Ошибка сети');
    };

    request.send();
    
});
