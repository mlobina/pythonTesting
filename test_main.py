import pytest
from unittest.mock import patch
import main



@pytest.mark.parametrize("user_doc_number, result", [
    ("11-2", True),
    ("123", False),
    ("", False)
])
def test_check_document_existance(user_doc_number, result):
    assert main.check_document_existance(user_doc_number) == result


user_input_number = '11-2'


@patch('builtins.input', return_value=user_input_number)
def test_get_doc_owner_name(mock_input):
    for current_document in main.documents:
        doc_number = current_document['number']
        if doc_number == user_input_number:
            doc_owner_name = current_document['name']
    assert main.get_doc_owner_name() == doc_owner_name


def test_remove_doc_from_shelf():
    main.remove_doc_from_shelf(user_input_number)
    shelf_documents = [x for xs in main.directories.values() for x in xs]
    assert user_input_number not in shelf_documents


@pytest.mark.parametrize("shelf_number, result", [
    ("5", ("5", True)),
    ("1", ("1", False))
])
def test_add_new_shelf(shelf_number, result):
    assert main.add_new_shelf(shelf_number) == result
    assert shelf_number in main.directories.keys()


@pytest.mark.parametrize("new_doc_number, shelf_number", [
    ("123", "1"),
    ("123", "5"),
])
def test_append_doc_to_shelf(new_doc_number, shelf_number):
    main.append_doc_to_shelf(new_doc_number, shelf_number)
    assert new_doc_number in [x for xs in main.directories.values() for x in xs]


@patch('builtins.input', return_value=user_input_number)
def test_delete_doc(mock_input):
    main.delete_doc()
    assert user_input_number not in [x for xs in main.directories.values() for x in xs]


@patch('builtins.input', return_value=user_input_number)
def test_get_doc_shelf(mock_input):
    for shelf_number, shelf_documents in main.directories.items():
        if user_input_number in shelf_documents:
            assert main.get_doc_shelf() == shelf_number


move_doc = ["123345", "1"]


@patch('builtins.input', side_effect = move_doc)
def test_move_doc_to_shelf(mock_input):
    main.move_doc_to_shelf()
    user_doc_number, user_shelf_number = move_doc
    assert user_doc_number in main.directories[user_shelf_number]


def test_show_document_info():

    for x in range(0, len(main.documents)):
        doc_info = f'"{main.documents[x]["type"]}" "{main.documents[x]["number"]}" "{main.documents[x]["name"]}"'
        assert main.show_document_info(main.documents[x]) == doc_info


def test_show_all_docs_info():
    all_docs_info = [f'"{x["type"]}" "{x["number"]}" "{x["name"]}"'\
                     for x in main.documents]
    assert main.show_all_docs_info() == all_docs_info


add_new_doc = {"123321", "passport", "Eric Freeman", "2"}


@patch('builtins.input', side_effect = add_new_doc)
def test_add_new_doc(mock_input):
    main.add_new_doc()
    new_doc_number, new_doc_type, new_doc_owner_name, new_doc_shelf_number = add_new_doc
    new_doc = {'type': new_doc_type,
               'number': new_doc_number,
               'name': new_doc_owner_name}
    assert new_doc in main.documents
    assert new_doc_shelf_number in main.directories

if __name__ == '__main__':
    pytest.main()