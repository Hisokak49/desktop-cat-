from cat_states import CatState


def test_cat_states_are_unique():
    values = [state.value for state in CatState]
    assert len(values) == len(set(values))


def test_expected_state_groups_are_present():
    assert {
        CatState.IDLE,
        CatState.FOLLOW,
        CatState.WATCH,
        CatState.THINKING,
    }.issubset(set(CatState))

    assert {
        CatState.TYPING,
        CatState.POMODORO,
        CatState.BREAK,
    }.issubset(set(CatState))

    assert {
        CatState.PLAY,
        CatState.ZOOMIES,
        CatState.SLEEP,
        CatState.STRETCH,
    }.issubset(set(CatState))


def test_state_values_are_stable_strings():
    for state in CatState:
        assert isinstance(state.value, str)
        assert state.value == state.value.lower()
        assert state.value.strip() == state.value
