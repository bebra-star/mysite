from main.models import TestSessionWordPair, TestSession, TestSessionWordPairStatus


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
        return None
    else:
        test_session.current_word_index += 1
        test_session.save()

        return get_current_word_pair(test_session)


def get_showing_word(test_session: TestSession, word_pair: TestSessionWordPair):
    return apply_language_to_word_pair(test_session, word_pair).get("showing_word")


def get_test_result(test_session: TestSession):
    words = TestSessionWordPair.objects.filter(test_session_id=test_session.id)

    words_count = len(words)
    skipped_count = 0
    learned_count = 0
    for word in words:
        match word.status:
            case TestSessionWordPairStatus.LEARNED:
                learned_count += 1
            case TestSessionWordPairStatus.SKIPPED:
                skipped_count += 1
            case None:
                raise ValueError("WordPair has no status")

    return {
        "words_count": words_count,
        "learned_count": learned_count,
        "skipped_count": skipped_count,
        "not_learned_words": words_count - learned_count - skipped_count,
    }
