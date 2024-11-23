var dict;
var currentWordIndex = 0;
var isDisplayLanguageFirst = true;
// "флипнутая" карта отображает противоположный основному языку перевод.
var isCardFlipped = false

function fetchDictionary(dictId) {
    fetch(window.location.origin + "/api/dictionary/" + dictId)
        .then((res) => {
            res.json()
                .then(
                    (data) => {
                        initDictionary(data.data)
                    }
                )
        })
        .catch((err) => {
            console.error(err);
        });
}

function initDictionary(dict1) {
    dict = dict1
    updateCurrentWord(dict.words[0].word1)
}

function getCurrentWordByIndex() {
    return dict.words[currentWordIndex]

}

function nextWord() {
    currentWordIndex = (currentWordIndex + 1) % dict.words.length;
    return getCurrentWordByIndex()
}

function previousWord() {
    if (currentWordIndex == 0) {
        currentWordIndex = dict.words.length
    }

    currentWordIndex--;
    return getCurrentWordByIndex()
}


function updateCurrentWord(value) {
    currentCard = document.querySelector(".card > .current-card__text")
    currentCard.innerHTML = value;
}

function getTranslateFromWordPair(wordPair) {
    b = isDisplayLanguageFirst

    if (isCardFlipped) {
        b = !b
    }

    return b ? wordPair.word1 : wordPair.word2
}

function handleNextWord() {
    isCardFlipped = false;
    updateCurrentWord(getTranslateFromWordPair(nextWord()))
}

function handlePreviousWord() {
    isCardFlipped = false;
    updateCurrentWord(getTranslateFromWordPair(previousWord()))
}

function updateDisplayLanguage() {
    updateCurrentWord(getTranslateFromWordPair(getCurrentWordByIndex()))
}

function handleLanguageSwitch() {
    isDisplayLanguageFirst = !isDisplayLanguageFirst;

    updateDisplayLanguage();
}

function flipCard() {
    isCardFlipped = !isCardFlipped
    updateDisplayLanguage()
}