**Задача:**

Реализовать серверное приложение для работы с базой данных, представляющее собой трекер задач сотрудников. 
Приложение должно обеспечивать CRUD операции для сотрудников и задач, а также предоставлять два специальных эндпоинта для получения информации о загруженности сотрудников и важных задачах.

**Технические требования:**

1. **Язык программирования:**
    - Python 3.11
2. **Фреймворк:**
    - Django для реализации REST API с использованием Django REST Framework (DRF)
3. **База данных:**
    - PostgreSQL для хранения данных
4. **ORM:**
    - Django ORM для взаимодействия с базой данных
5. **Контейнеризация:**
    - Docker для контейнеризации приложения


**Запуск проекта:**

- клонируйте проект
- создайте файл .env по образцу. (Файл .env.sample)
- убедитесь, что на Вашем устройстве установлен Docker
- осуществите сборку образов и запуск контейнеров (docker compose up -d --build)

 
**Структура БД:**

Таблица сотрудников:
- ФИО
- Должность
  
Таблица задач:
- Наименование
- Ссылка на родительскую задачу (если есть зависимость)
- Исполнитель
- Срок исполнения
- Статус задачи

**Права доступа:**

Неавторизованным пользователям доступна регистрация, авторизация, а также просмотр отдельных сотрудников и заданий, постраничного списка сотрудников и заданий. 
Зарегистрированный пользователь может создавать, редактрировать, просматривать и удалять сотрудников и задания, постраничные списки сотрудников и заданий.  
Зарегистрированный пользователь имеет доступ к просмотру специаьлных эндпоинтов.

**Специальные эндпоинты:**

 Занятые сотрудники:
 - Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач.
   
 Важные задачи:
 1. Запрашивает из БД задачи, которые не взяты в работу, но от которых зависят другие задачи, взятые в работу.
 2. Реализует поиск по сотрудникам, которые могут взять такие задачи
        (наименее загруженный сотрудник или сотрудник, выполняющий родительскую задачу, если ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника).
 3. Возвращает список объектов в формате: `{Важная задача, Срок, [ФИО рекомендованных исполнителей]}`.

**Валидация входящих запросов:**

 Сотрудники:
 - ФИО сотрудника может содержать только буквы кириллицы и дефисы. Фамилия, имя и отчетсво начинаются с заглавной буквы. Допустимо отсутсвие отчества.
   
 Задачи:
 - Срок исполнения задачи не может быть раньше текущей даты или срока исполнения родительской задачи.

**Практическое применение:**

Незарегистрированными пользователями являются сотрудники компании. Зарегистрированным - руководитель подразделения. 
Трекер задач дает возможность руководителю эффективно управлять заданиями, назначенными сотрудникам.
Использование приложения способствует равномерному распределению нагрузки между сотрудниками. 
Трекер задач позволяет исключить простои, благодаря прозрачности и упорядочению процессов, что, как следствие, помогает в своевременном выполнении ключевых задач компании.
