Запуск проекта
```
kubectl apply -f ./menifests
helm istall api -n ms-auth ./auth/helm
helm install api -n ms-profile ./profile/helm
```

Запуск тестов
```
newman run ./otus-api-gateway.postman_collection.json -e ./otus-api-gw.postman_environment.json --verbose
```

baseUrl = arch.homework для изменения нужно отредактировать baseUrl в файле файл otus-api-gw.postman_environment.json 


Схема архитектуроно решения - api-gateway-diagram.jpg

Суть архитектурного решания:

Запросы начинающиеся с префикса /ms-auth* адресуются к микросервису авторизации и не требуют авторизации.
При регистрации пользователя создается микросервис авторизации ходит в микросервис профилей и создает запись в бд.
При этом в самом сервите авторизации в бд создается запись с учетными данными в связке с id профиля.
При логине если учетные данные верны создается сессия и хранится в сессионном хранилище. Ключ сессии - uuid, значение - jwt токен
При логауте сессия удаляется из хранилища

Запросы начинающиеся с префикса /ms-profile* адресуются к микросервису профилей и требуют авторизации.
Авторизация сделана на стороне istio, на каждый запрос к микросервису профилей, будет сделан запрос к микросервису авторизации.
Из кук запроса достается session_id и проверяется наличие сессии в сессионном хранилище. Есть сессии нет - 401. Если сессия есть то в заголовки запроса будет добавлены поля x-user-id, x-profile-id, x-auth-token. Дополнительно проверяется валидность токена, и issuer токена, если токен не валиден либо issuer неизвестный - 403. На стороне микрсервиса профилей есть проверка входных данных для чтения/изменения профиля. Если id профиля не равен x-profile-id - 403.