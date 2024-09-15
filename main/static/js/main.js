function buttonClick(e) {
  e.style.color = "blue";
  console.log(e);
}

function register(e) {
  e.preventDefault();
  form = new FormData(e.target);

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
    body: JSON.stringify({
      name: form.get("name"),
      password: form.get("password"),
    }),
  })
    .then((response) => {
      console.log(response);
      if (response.status == 201) {
        alert("я зарегался");
      } else if (response.status == 409) {
        alert("пользователь с таким именем уже существует");
      } else {
        alert("ошибка");
      }
    })
    .catch((err) => {
      console.error(err);
    });
}

function createDict(e) {
  e.preventDefault();
  form = new FormData(e.target);

  fetch("/dictinory", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
    body: JSON.stringify({
      name: form.get("name"),
      language1: form.get("password"),
    }),
  })
    .then((response) => {
      console.log(response);
      if (response.status == 201) {
        alert("я зарегался");
      } else if (response.status == 409) {
        alert("пользователь с таким именем уже существует");
      } else {
        alert("ошибка");
      }
    })
    .catch((err) => {
      console.error(err);
    });
}
