var dict;
var currentWordIndex = 0;
var isDisplayLanguageFirst = true;
// "флипнутая" карта отображает противоположный основному языку перевод.
var isCardFlipped = false;

function fetchDictionary(dictId) {
    fetch(window.location.origin + "/api/dictionary/" + dictId)
        .then((res) => {
            res.json().then((data) => {
                dict = data.data;
                console.log("dict", dict);
                updateCurrentWord(dict.words[0].word1);
            });
        })
        .catch((err) => {
            console.error(err);
        });
}

function getCurrentWordByIndex() {
    return dict.words[currentWordIndex];
}

function nextWord() {
    currentWordIndex = (currentWordIndex + 1) % dict.words.length;
    return getCurrentWordByIndex();
}

function previousWord() {
    if (currentWordIndex == 0) {
        currentWordIndex = dict.words.length;
    }

    currentWordIndex--;
    return getCurrentWordByIndex();
}

function updateCurrentWord(value) {
    currentCard = document.querySelector(".card > .current-card__text");
    currentCard.innerHTML = value;
}

function getTranslateFromWordPair(wordPair) {
    let b = isDisplayLanguageFirst;

    if (isCardFlipped) {
        b = !b;
    }

    return b ? wordPair.word1 : wordPair.word2;
}

function handleNextWord() {
    isCardFlipped = false;
    updateCurrentWord(getTranslateFromWordPair(nextWord()));
}

function handlePreviousWord() {
    isCardFlipped = false;
    updateCurrentWord(getTranslateFromWordPair(previousWord()));
}

function updateDisplayLanguage() {
    updateCurrentWord(getTranslateFromWordPair(getCurrentWordByIndex()));
}

function handleLanguageSwitch() {
    isDisplayLanguageFirst = !isDisplayLanguageFirst;

    updateDisplayLanguage();
}

function flipCard() {
    isCardFlipped = !isCardFlipped;
    updateDisplayLanguage();
}

function openPopup() {
    document.querySelector(".dialog").showModal();
}

function closePopup() {
    document.querySelector(".dialog").close();
}

function startTest(e, dictId) {
    e.preventDefault();
    const form = new FormData(e.target);
    // todo: rename
    const is_showing_language_first = !form.get("is_showing_language_first");

    fetch(window.location.origin + "/api/start-test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": form.get("csrfmiddlewaretoken"),
        },
        body: JSON.stringify({
            dict_id: dictId,
            is_showing_language_first: is_showing_language_first,
        }),
    })
        .then((response) => {
            if (response.status == 200) {
                window.location.href += "/test";
            } else {
                alert("ошибка");
            }
        })
        .catch((err) => {
            console.error(err);
        });
}
