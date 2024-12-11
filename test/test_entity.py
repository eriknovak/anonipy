from anonipy.definitions import Entity

# =====================================
# Test Entity
# =====================================


def test_init_default():
    entity = Entity(
        text="test",
        label="test",
        start_index=0,
        end_index=4,
    )
    assert entity.text == "test"
    assert entity.label == "test"
    assert entity.start_index == 0
    assert entity.end_index == 4
    assert entity.score == 1.0
    assert entity.type is None
    assert entity.regex == ".*"


def test_init_custom():
    entity = Entity(
        text="test",
        label="test",
        start_index=0,
        end_index=4,
        score=0.89,
        type="test",
        regex="test",
    )
    assert entity.text == "test"
    assert entity.label == "test"
    assert entity.start_index == 0
    assert entity.end_index == 4
    assert entity.score == 0.89
    assert entity.type == "test"
    assert entity.regex == "test"
