### 1. Описание продукта
Трейд бот. Принимает на http сервере сигнал вверх или вниз. На основе сигнала соверщает действие. Вот так выглядит json сигнала:

json = {
"password": str,
"symbol": "SOLUSDT",
"position_side": "Buy",
"stop_in_percent": "0.65",
"take_in_percent": "1.49",
"size": "0.3",
"leverage": "4",
"time_frame": "1m",
"interval_stop_in_percent": "75",
"step_move_stop_in_percent": "90",
"part_from_potential_profit": "3",
"max_count_trail_take": "0",
"limit_depth": "0.3",
"time_to_set_stop": "120",
"time_to_cancel_order": "60"
}

Графический интерфейс для взаимодействия с ботом -- телеграм

Бот уимеет:
1) Оложенный стоп-лосс
2) Трейлинг стоп
3) Сигналы на основе технического анализа
4) Сигналы на основе нейросети
5) Выгрузка истории с биржи
6) Формирование датасета для обучения модели
7) Использование готовых архитектур и собственное построение архитектуры
8) Расчет индикаторов в реальном времени
9) Самописная СУБД для детального контроля данных
10) Закрытие лимиток, которые долго не исполняются


### 2. Сервисы продукта
1) set stop
2) trailing stop
3) cancel order
4) open position
5) telegram
6) nginx
7) db
8) stream positions

### 3. Программы продукта
Продукт программы не создает

### 4. Зависимости продукта
1) Docker + Docker compose
2) Python + threading + WebSocket
3) Nginx + SSL

### 5. Тестироование продукта
Тестов нет. Ручками

### 6. Запуск системы
(.env):
1) DOMAIN=domain.ru
2) BOT_TOKEN=str
3) API_KEY=str
4) API_SECRET_KEY=str

cmd:
1) Первичный запуск: прочитайте и запустите файл ./cmd/user/install-ssl.sh
2) Запуск: ./cmd/user/start-bot.sh
3) Рестарт: ./cmd/user/restart-bot.sh
4) Перевыпуск ssl: ./cmd/user/reinstall-ssl.sh
5) Стоп: ./cmd/user/stop-bot.sh
