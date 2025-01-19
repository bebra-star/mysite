let showingWord;
let currentWordIndex = 0;
let dictId;
let answer;
let ended = false;

function setGlobalDictId(value) {
    dictId = value;
}

function getTestWord() {
    fetch(`${window.location.origin}/api/dictionary/${dictId}/test/word`)
        .then((res) => {
            res.json().then((data) => {
                showingWord = data.data.showing_word;
                displayShowingWord();
                currentWordIndex = data.data.current_word_index + 1;
                displayCurrentWordIndex();
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function displayShowingWord() {
    document.querySelector(".showing-word__text").innerText = showingWord;
}
function displayCurrentWordIndex() {
    document.querySelector(".words-counter__number-1").innerText =
        currentWordIndex;
}

function getTranslationInput() {
    return document
        .querySelector(".translation__input")
        .value.trim()
        .toLowerCase();
}
function handleNewWordResponse(data) {
    wordTest = document.body.querySelector(".word-test");
    wordResult = document.body.querySelector(".word-result__container");

    wordTest.style.display = "none";

    if (data.success) {
        wordResult.querySelector(".word-result__wrong-answer").style.display =
            "none";
        wordResult.querySelector(".correct-answer__text").innerText = answer;
    } else {
        wordResult.querySelector(".wrong-answer__text").innerText = answer;
        wordResult.querySelector(".word-result__wrong-answer").style =
            undefined;
    }

    wordResult.querySelector(".correct-answer__text").innerText =
        data.correct_answer;
    wordResult.style = undefined;
    wordTest.querySelector(".translation__input").value = "";

    if (data.next_word) {
        showingWord = data.next_word;
        currentWordIndex++;
    } else {
        renderResultPage(data);
        ended = true;
    }
}

function iKnowClicked() {
    fetch(
        `${window.location.origin}/api/dictionary/${dictId}/test/i-know-word`,
        {
            method: "GET",
        }
    )
        .then((res) => {
            res.json().then((data) => {
                handleNewWordResponse(data.data);
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function answerSubmit(e) {
    e.preventDefault();
    form = new FormData(e.target);
    answer = form.get("answer");

    fetch(
        `${window.location.origin}/api/dictionary/${dictId}/test/answer-word`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": form.get("csrfmiddlewaretoken"),
            },
            body: JSON.stringify({
                answer,
            }),
        }
    )
        .then((res) => {
            if (!res.ok) console.error(res);
            res.json().then((data) => {
                handleNewWordResponse(data.data);
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
                handleNewWordResponse(data.data);
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function renderResultPage(results) {
    resultsPage = document.body.querySelector(".test-result-page");

    resultsPage.querySelector(".results__learned-words").innerText =
        results.learned_count;
    resultsPage.querySelector(".results__not-learned-words").innerText =
        results.not_learned_words;
    resultsPage.querySelector(".results__skipped-words").innerText =
        results.skipped_count;
}

function showResultPage() {
    resultsPage = document.body.querySelector(".test-result-page");

    resultsPage.style.display = "block";
    document.body.querySelector(".test-page").style.display = "none";
}

function continueResult() {
    wordTest = document.body.querySelector(".word-test");
    wordResult = document.body.querySelector(".word-result__container");
    wordTest.style = undefined;
    wordResult.style.display = "none";

    if (ended) {
        showResultPage();
        ended = false;
    } else {
        displayShowingWord();
        displayCurrentWordIndex();
    }
}
