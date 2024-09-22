function buttonClick(e) {
  e.style.color = "blue";
  console.log(e);
}

function register(e) {
  // так как в параметр e передается объект события, то его можно использовать для остановки дефолтного поведения тега (в данном случае form)
  e.preventDefault();
  // получаем объект формы
  form = new FormData(e.target);

  fetch("api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // передаем csrf-token в хедере
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
    // получаем json из объекта.
    body: JSON.stringify({
      name: form.get("name"),
      password: form.get("password"),
    }),
  })
    // then - вызывается после того, как запрос завершится успешно.
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
    // catch - вызывается в случае ошибки, например, если сервер не отвечает
    .catch((err) => {
      console.error(err);
    });
}

function createDict(e) {
  e.preventDefault();
  form = new FormData(e.target);

  fetch("api/dictionary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
    body: JSON.stringify({
      name: form.get("name"),
      language1: form.get("lang1"),
      language2: form.get("lang2"),
    }),
  })
    .then((response) => {
      console.log(response);
      if (response.status == 201) {
        window.location.reload();
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
