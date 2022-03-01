import pytest

from todo import create_db, get_todos, add_todo, delete_todo


@pytest.mark.fast
def test_create_db(db):
    create_db(db)
    cur = db.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="todo";')
    result = cur.fetchall()
    assert result is not None


@pytest.mark.fast
def test_get_todos(db_fixture):
    result = get_todos(db_fixture)
    cur = db_fixture.cursor()
    cur.execute('SELECT * FROM todo')
    actual = cur.fetchall()
    assert result == actual


@pytest.mark.fast
def test_add_todo(db_fixture, line_to_add="nwe line"):
    add_todo(db_fixture, line_to_add)
    cur = db_fixture.cursor()
    cur.execute('SELECT * FROM todo WHERE todo_text = ?;', (line_to_add,))
    result = cur.fetchone()
    assert result is not None


@pytest.mark.fast
def test_delete_todo(db_fixture, line_to_delete="Some todo789654123"):
    cur = db_fixture.cursor()
    delete_todo(db_fixture, line_to_delete)
    cur.execute('SELECT * FROM todo WHERE todo_text = ?;', (line_to_delete,))
    result = cur.fetchone()
    assert result is None


@pytest.mark.slow
def test_add_many_todos(db_fixture):
    TIMES_OF_ADDING = 1_000
    [add_todo(db_fixture, i) for i in range(TIMES_OF_ADDING)]
    cur = db_fixture.cursor()
    cur.execute('SELECT * FROM todo;')
    result = len(cur.fetchall())
    assert result == TIMES_OF_ADDING


@pytest.mark.end_to_end
def test_user_story(db_fixture):
    USER_STORY_COUNT = 3

    for task in range(USER_STORY_COUNT):
        add_todo(db_fixture, task)
    result = len(get_todos(db_fixture))
    assert result == USER_STORY_COUNT

    for task in range(USER_STORY_COUNT):
        delete_todo(db_fixture, task)
    result = len(get_todos(db_fixture))
    assert result != 0
