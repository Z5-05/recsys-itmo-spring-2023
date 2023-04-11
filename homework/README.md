### Запуск в целом все тот же, что и обычно.

в [botify/data](../botify/data) лежат три файла: 
1. Рекомендации контекстного рекоммендера ```contextual_tracks.json``` с ключами типа ```{'tracks': str, 'recommendations': List[Int]}```. Его поле в config.json - ```CONTEXTUAL_RECOMENDATIONS_FILE_PATH```;
2. Общий *json* с треками - ```{'artist': str, 'title': str, 'track': int}```, поле в конфиге - ```TRACKS_FILE_PATH```;
3. Данные собственного рекоммендера (о его логике в отчете) со структурой ```{'user': int, 'recommendations': List[Int]}```, поле в конфиге - ```CUSTOM_RECOMENDATIONS_FILE_PATH```.
<br>
Запускается все через:
```
docker-compose up -d --build
```
Как обычно проверяем все через:
```
curl http://localhost:5000/
```
Когда сервис работает теперь нужно получить пользовательские сессии и прогнать их через ноутбук с моделью. Окружение отдельное я создавать не стал, потому что всего, что мы использовали на 5-ом семинаре более чем достаточно. Генерим сессии:
```
python sim/run.py --episodes 1000 --config config/env.yml multi --processes 4
```
Перекидываем результат в [homework](./):
```
docker cp recommender-container:/app/log/data.json ~/MADE/recsys-itmo-spring-2023/homework
```
Запускаем ноутбук [homework/A_B_tester.ipynb](A_B_tester.ipynb).
______
Про рекоммендер и его обучение инфа здесь же, в [REPORT.md](REPORT.md).
______
**Файл с пользовательскими сессиями для обучения оказался слишком большим, поэтому его можно найти [тут](https://disk.yandex.ru/d/7rypJRo-ObwM-Q), а потом перекинуть в [homework/data](./data/)**
