from main.models import (
    TestSessionWordPair,
)


def get_current_word_pair(test_session):
    current_word_pair = TestSessionWordPair.objects.filter(
        test_session_id=test_session.id
    )[test_session.current_word_index]
    if test_session.is_showing_language_first:
        return {
            "showing_word": current_word_pair.word_pair.word1,
            "translation": current_word_pair.word_pair.word2,
        }
    else:
        return {
            "showing_word": current_word_pair.word_pair.word2,
            "translation": current_word_pair.word_pair.word1,
        }


def get_next_word(test_session):
    words = TestSessionWordPair.objects.filter(test_session_id=test_session.id)

    if len(words) - 1 == test_session.current_word_index:
        print("last word")

    else:
        test_session.current_word_index += 1
        test_session.save()
        return get_current_word_pair(test_session).get("showing_word")
