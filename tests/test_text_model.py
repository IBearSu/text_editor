import pytest
from text_editor_project.models.MyString import MyString
from text_editor_project.models.cursor import Cursor
from text_editor_project.models.helpers import encode_to_cp1251, decode_from_cp1251
from text_editor_project.models.text_model import TextModel

# Создаем экземпляр модели текста для использования в тестах
@pytest.fixture
def text_model():
    return TextModel()

def test_add_new_line(text_model):
    # Добавление новой строки в текстовую модель
    text_model.add_new_line(0, "Hello, World!")
    assert len(text_model.lines) == 1
    assert decode_from_cp1251(text_model.lines[0].c_strb()) == "Hello, World!"

def test_append_line(text_model):
    # Добавление строки в конец
    text_model.append_line("New line")
    assert len(text_model.lines) == 1
    assert decode_from_cp1251(text_model.lines[0].c_strb()) == "New line"

def test_insert_text_without_notifications(text_model):
    # Вставка текста в определенную позицию
    text_model.append_line("Initial line")
    text_model.insert_text_without_notifications(0, 0, encode_to_cp1251("Inserted text "))
    assert text_model.lines[0].c_str() == "Inserted text Initial line"

def test_delete_all_text_on_the_line(text_model):
    # Удаление всего текста на строке
    text_model.append_line("Line to be cleared")
    text_model.delete_all_text_on_the_line(0)
    assert decode_from_cp1251(text_model.lines[0].c_strb()) == "\n"  # Ожидаем пустую строку с символом новой строки

def test_find_text(text_model):
    # Поиск текста
    text_model.append_line("This is a test line")
    result = text_model.find_text("test")
    assert result == (0, 10)  # Текст "test" начинается с позиции 10 на первой строке

def test_find_text_not_found(text_model):
    # Поиск несуществующего текста
    text_model.append_line("This is a test line")
    result = text_model.find_text("nonexistent")
    assert result is None  # Текст не найден

def test_insert_char(text_model):
    # Вставка символа в строку
    text_model.append_line("Hello")
    text_model.insert_char(0, 5, "!")
    assert decode_from_cp1251(text_model.lines[0].c_strb()) == "Hello!"

def test_clear_text(text_model):
    # Очистка всего текста
    text_model.append_line("Some text")
    text_model.clear()
    assert len(text_model.lines) == 0  # Все строки должны быть удалены

def test_delete_word_at_position(text_model):
    # Удаление слова на позиции
    text_model.append_line("This is a sample line")
    text_model.delete_word_at_position(0, 10)  # Удалить слово "sample"
    assert decode_from_cp1251(text_model.lines[0].c_strb()) == "This is a line"  # После удаления "sample"

def test_add_subscriber(text_model):
    # Проверка добавления подписчика
    mock_subscriber = MockSubscriber()
    text_model.add_subscriber(mock_subscriber)
    assert mock_subscriber in text_model.view_subscribers

def test_remove_subscriber(text_model):
    # Проверка удаления подписчика
    mock_subscriber = MockSubscriber()
    text_model.add_subscriber(mock_subscriber)
    text_model.remove_subscriber(mock_subscriber)
    assert mock_subscriber not in text_model.view_subscribers

# Мок-класс для тестирования подписчиков
class MockSubscriber:
    def update(self, model):
        pass  # Просто имитируем метод обновления подписчика

