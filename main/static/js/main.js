function buttonClick(e) {
  e.style.color = "blue";
  console.log(e);
}

function login(e) {
  e.preventDefault();
  form = new FormData(e.target);

  fetch("api/login", {
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
        window.location.href = "http://127.0.0.1:8000/profile";
      } else {
        alert("ошибка");
      }
    })
    // catch - вызывается в случае ошибки, например, если сервер не отвечает
    .catch((err) => {
      console.error(err);
    });
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
        window.location.href = "http://127.0.0.1:8000/profile";
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

function logout(e) {
  // так как в параметр e передается объект события, то его можно использовать для остановки дефолтного поведения тега (в данном случае form)
  e.preventDefault();
  // получаем объект формы
  form = new FormData(e.target);

  fetch("api/logout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // передаем csrf-token в хедере
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
  })
    // then - вызывается после того, как запрос завершится успешно.
    .then((response) => {
      console.log(response);
      if (response.status == 204) {
        window.location.href = "http://127.0.0.1:8000/";
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
  words1 = form.getAll("word1");
  words2 = form.getAll("word2");
  words = [];
  for (let i = 0; i < words1.length; i++) {
    words.push({
      word1: words1[i],
      word2: words2[i],
    });
  }

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
      words: words,
    }),
  })
    .then((response) => {
      console.log(response);
      if (response.status == 201) {
        // window.location.reload();
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

function add_words_input() {
  const container = document.getElementsByClassName("words_input_container").item(0);
  const clone = container.lastElementChild.cloneNode(true);
  clone.childNodes.forEach((child) => {
    if (child.type == "text") {
      child.value = "";
    }
  });

  container.appendChild(clone);
}

function delete_words_input(e) {
  e.remove();
}

function start_test(e, dict_id) {
  e.preventDefault();
  form = new FormData(e.target);

  fetch("api/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": form.get("csrfmiddlewaretoken"),
    },
    body: JSON.stringify({
      dict_id: dict_id,
    }),
  })
    .then((response) => {
      console.log(response);
      if (response.status == 201) {
        // window.location.href = "http://127.0.0.1:8000/profile";
        alert("123");
      } else {
        alert("ошибка");
      }
    })
    .catch((err) => {
      console.error(err);
    });
}
