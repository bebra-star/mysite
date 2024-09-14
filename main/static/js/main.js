function buttonClick(e) {
    e.style.color = "blue";
    console.log(e)
}

function register(e) {
    e.preventDefault();
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": e.target.elements.csrfmiddlewaretoken.value
        },
        body: JSON.stringify({
            name: e.target.elements.name.value,
            password: e.target.elements.password.value
        }),
    }).then(response => {
        console.log(response);
        if (response.status == 201) {
            alert("я зарегался");
        } else {
            alert("ошибка");
        }
    })
        .catch(err => {
            console.error(err);
        });

}
