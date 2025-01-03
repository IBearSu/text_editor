def encode_to_cp1251(text, encoding='cp1251'):
    """
    Преобразует строку в однобайтовую последовательность байтов.
    :param text: Исходная строка (Unicode).
    :param encoding: Кодировка (по умолчанию cp1251).
    :return: Байтовая строка.
    """
    try:
        return text.encode(encoding)
    except UnicodeEncodeError:
        raise ValueError(f"Текст содержит символы, которые нельзя закодировать в {encoding}.")

def decode_from_cp1251(text, encoding='cp1251'):
    """
    Преобразует строку в однобайтовую последовательность байтов.
    :param text: Исходная строка (Unicode).
    :param encoding: Кодировка (по умолчанию cp1251).
    :return: Байтовая строка.
    """
    try:
        return text.decode(encoding)
    except UnicodeEncodeError:
        raise ValueError(f"Текст содержит символы, которые нельзя декодировать из {encoding}.")
