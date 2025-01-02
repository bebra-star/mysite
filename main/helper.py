from main.models import TestSessionWordPair, TestSession


def apply_language_to_word_pair(
    test_session: TestSession, word_pair: TestSessionWordPair
):
    if test_session.is_showing_language_first:
        return {
            "showing_word": word_pair.word_pair.word1,
            "translation": word_pair.word_pair.word2,
        }
    else:
        return {
            "showing_word": word_pair.word_pair.word2,
            "translation": word_pair.word_pair.word1,
        }


def get_current_word_pair(test_session):
    return TestSessionWordPair.objects.filter(test_session_id=test_session.id)[
        test_session.current_word_index
    ]


def get_next_word(test_session):
    words = TestSessionWordPair.objects.filter(test_session_id=test_session.id)

    if len(words) - 1 == test_session.current_word_index:
        print("last word")

    else:
        test_session.current_word_index += 1
        test_session.save()

        return get_current_word_pair(test_session)


def get_showing_word(test_session: TestSession, word_pair: TestSessionWordPair):
    return apply_language_to_word_pair(test_session, word_pair).get("showing_word")
