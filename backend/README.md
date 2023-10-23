##DOCS API
https://documenter.getpostman.com/view/4633020/damprodam-flask-api/RWEfNKWM#d64b04fd-d63e-40bb-b816-be893492fd0d

# ветки проекта
у проекта есть несколько веток у которых свой собственный путь:

- `master` главная ветка API главного сайта damprodam.ru, фреймов(frame.damprodam.ru, framecs.damprodam.ru, framesv.damprodam.ru, frame-ym.damprodam.ru)
- `partner_api` ветка API для партнеров(damprodam.ru/api/v1/) и партнерской админки(damprodam.ru/partner/admin/)
- `test-server` ветка тестового API для сайта test.damprodam.ru, тестового фрейма(testframe.damprodam.ru)
- `arm` ветка API для армянского сайта dramdram.am
- `master_admin` ветка для админки мастеров damprodam.ru/master/
- `db` ветка со всеми манипуляциями с базой данных(модели и миграции). эта ветка общая у всех и в каждой самостоятельной ветке должны присутствовать коммиты из этой ветки

# старт проекта
если в папке `instance` нет файла `config.py` копируем его туда `cp config.py.example instance/config.py` и редактируем со своими настройками
делаем `docker-compose up`
заходим в контейнер web
запускаем `./manage.py`
в меню:

- `db` все манипуляции с базой данных
- `run` команда запуска flask(`./manage.py run`)
- `fix` команда создания фикстур
- `kok` команда запуска фикстур(применять только один раз во избежании дублекатов)
- `test` команда запуска тестов
- `leads` команда выгрузки лидов из базы в txt файл
- `minprices` команда манипуляции с ценами

манипуляции с базой данных:

- `db migrate` генерация новой миграции на основе созданных/измененных моделей
- `db upgrade` применение всех миграций
- `db downgrade` откат всех миграций на 1 версию

!! все изменения в полях `src/db/models` должны сопровождаться файлом миграции. каждое изменение должно находиться в одном коммите и запушена в ветку `db`

структура папок и файлов:

- `docker` описание образов докера
- `instance` все конфиги тут
- `logs` все логи тут
- `src/api/cross_tradein.py` файл отвечающий за заказы со всех сервисов с логикой обмена, создание заказов для всех новых сервисов тоже делать через этот файл
- `src/db/models` тут описываются все модели
- `src/lib` дополнительные библиотеки
- `src/static` статика для админки
- `src/templates` шаблоны для админки
- `src/views` контроллеры админки
- `jump_to_container.py` файл для быстрого входа в докер контейнер
- `requirements.txt` зависимости python основной версии. если есть проблема с зависимостями, из контейнера: `pip3 install -r requirements.txt`
- `python2_requirements.txt` зависимости python 2 версии.  если есть проблема с зависимостями, из контейнера: `pip install -r python2_requirements.txt`
- `service_creds.json` конфигурационный файл в корне приложения(когда-нибудт нужно перенести в instance) отвечает за доступ к google API
- `supervisor.conf` конфигурационный файл supervisor, который запускает приложение и не дает ему упасть