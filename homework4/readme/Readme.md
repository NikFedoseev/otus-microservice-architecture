Команда для запуска
```
helm dependency build ./helm
helm install app ./helm
kubectl port-forward service/app-grafana 9001:80
```

JSON модель дашборда находится в файле ./dashboard.json
Скриншот дашборда после тестирования в файле dashboard.png
