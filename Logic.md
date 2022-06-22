# Логика методов

### Method post('/imports')

Обработчик создания объектов

Мы получаем на вход схему ShopUnitImports:

Добавляем в таблицу imports новый импорт данных - инкрементальное поле id

Итерируемся по объектам:

Если объект отсутствует в базе, то
    добавляем его в таблицу shop_units
    добавляем связь id-parentId в таблицу relations

Если объект присутствует в базе, то
    мы вставляем объект из таблицы shop_unit с этим ID в таблицу unit_history
    мы обновляем объект в таблицу shop_unit

Вставляемые поля:
    imports: число
    shop_units: id, name, type, updatedAt, importId
    shop_units: relation
Получается, что распределяются между основной таблицей (shop_units) и (shop_units_relation)

### Method delete('delete/{id}')

Приходит id объекта

Ищем в таблицах shop_units_relation, shop_units по id

Для этого id получаем всех его детей (children). [Может быть рекурсивный запрос из pg]

Удаляем по дереву из relations,
добавляем в историию
удаляем из основной таблицы shop_units


### Method get('/nodes/{id}')


### Method get('/node/{id}/statistic')


### Method node('/nodes/{id}')
