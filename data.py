LISTING_DATA = {
    'name': 'Учебное объявление: настольная лампа',
    'category': 'Авто',
    'condition': 'Новый',
    'city': 'Москва',
    'description': 'Тестовое объявление. Товар не продаётся, запись будет удалена после проверки.',
    'price': 1750,
}

CREATE_CATEGORIES = ['Авто', 'Книги', 'Технологии']

EDIT_CASES = [
    ('name', 'Учебное объявление: изменённое название'),
    ('category', 'Книги'),
    ('condition', 'Б/У'),
    ('city', 'Санкт-Петербург'),
    ('description', 'Обновлённое описание тестового товара.'),
    ('price', 2900),
]

FORBIDDEN_NAME = 'Название, которое другой пользователь не должен сохранить'
DUPLICATE_EMAIL_ERROR = {'statusCode': 400, 'message': 'Почта уже используется'}
FOREIGN_EDIT_ERROR = {
    'message': 'Оффер не найден или у вас нет прав на его редактирование',
    'error': 'Unauthorized',
    'statusCode': 401,
}
DELETE_SUCCESS = {'message': 'Объявление удалено успешно'}
