Команда для запуска через helm
```
helm install app ./chart
```


Команда для запуска манифестов
```
kubectl apply -f k8s/
```

Команды первоначальных миграций не требуются, миграции будет применены в initContainers в манифесте deployment.yml

Постман коллекция находится в директории readme/otus.postman_collection