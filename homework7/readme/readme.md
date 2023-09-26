#### Описание
В проекте используется естественный ключ идемпотентности, на основе хеша от списка заказов. При создании нового заказа проверяется ключ переданный в заголовке x-idempotency-key (ключ обязательный), если хеш переданный в заголовке не будет совпадать с ключом сгененированным на сервере - в ответе будет 409.


#### Запуск проекта

```
kubectl apply -f ./manifests
helm install api -n ms-order ./helm
```

#### Запуск тестов

```
newman run ./otus-idempotency.postman_collection.json -e ./otus-api.postman_environment.json --verbose
```

baseUrl = arch.homework для изменения нужно отредактировать baseUrl в файле файл otus-api-gw.postman_environment.json