let showingWord;
let tranlation;
let dictId;

function setGlobalDictId(value) {
    dictId = value;
}

function getTestWord() {
    fetch(`${window.location.origin}/api/dictionary/${dictId}/test/word`)
        .then((res) => {
            res.json().then((data) => {
                showingWord = data.data.showing_word;
                tranlation = data.data.translation;
                displayShowingWord();
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function displayShowingWord() {
    document.querySelector(".showing-word__text").innerText = showingWord;
}

function getTranslationInput() {
    return document
        .querySelector(".translation__input")
        .value.trim()
        .toLowerCase();
}

function sendAnswer(csrftoken, answer) {
    fetch(
        `${window.location.origin}/api/dictionary/${dictId}/test/answer-word`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({
                answer: answer,
            }),
        }
    )
        .then((res) => {
            res.json().then((data) => {
                console.log(data);
                showingWord = data.data.showing_word;
                tranlation = data.data.translation;
                displayShowingWord();
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function answer(e) {
    e.preventDefault();
    form = new FormData(e.target);

    sendAnswer(form.get("csrfmiddlewaretoken"), form.get("answer"));
}

function skipWordClicked() {}
