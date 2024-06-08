/*!
* Start Bootstrap - One Page Wonder v6.0.6 (https://startbootstrap.com/theme/one-page-wonder)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-one-page-wonder/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

document.getElementById("article-form").addEventListener("submit", function(event) {
    event.preventDefault();

    var title = document.getElementById("title").value;
    var content = document.getElementById("content").value;

    // 发送数据到后端
    fetch('/submit-article', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({title: title, content: content})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('文章已发布！');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('发布失败！');
    });
});