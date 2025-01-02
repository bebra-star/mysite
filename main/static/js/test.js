let showingWord;
let dictId;

function setGlobalDictId(value) {
    dictId = value;
}

function getTestWord() {
    fetch(`${window.location.origin}/api/dictionary/${dictId}/test/word`)
        .then((res) => {
            res.json().then((data) => {
                showingWord = data.data;
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

function sendAnswer(csrftoken, answer) {}

function answerSubmit(e) {
    e.preventDefault();
    form = new FormData(e.target);

    fetch(
        `${window.location.origin}/api/dictionary/${dictId}/test/answer-word`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": form.get("csrfmiddlewaretoken"),
            },
            body: JSON.stringify({
                answer: form.get("answer"),
            }),
        }
    )
        .then((res) => {
            res.json().then((data) => {
                console.log(data);
                showingWord = data.data.next_word;
                displayShowingWord();
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function skipWordClicked() {
    fetch(`${window.location.origin}/api/dictionary/${dictId}/test/skip-word`, {
        method: "GET",
    })
        .then((res) => {
            res.json().then((data) => {
                console.log(data);
                showingWord = data.data.next_word;
                displayShowingWord();
            });
        })
        .catch((err) => {
            console.error(err);
        });
}
