# Python-клиент для платформы webinar.ru (mts-link.ru)

## Клиент находится в разработке!

### Особенности

Клиент полностью асинхронный с поддержкой валидации Pydantic. Требуется Python 3.11 или выше. Основан на `aiohttp` и `pydantic`.

> Сделан на основе документации: https://help.webinar.ru/ru/articles/3180654-api-список-методов-вебинары

### Установка

```console
$ pip install webinarru
```

### Простое использоание

Создайте файл `main.py`:

```Python hl_lines="9  14"
import asyncio
from pprint import pprint
from WebinarRu import WebinarAPI

webinar = WebinarAPI("YOUR_API_TOKEN")


async def main():
    # Получение списка часовых поясов
    timezones = await webinar.get_timezones()
    pprint(timezones)

    # Выгрузка мероприятий
    events = await webinar.get_events(date_from=datetime.datetime(2024, 8, 10), status=["STOP", "ACTIVE"])
    pprint(events)
    
    # Участники вебинаров
    for event in events:
        for eventsession in event.eventSessions:
            participations = await webinar.get_event_session_participations(eventsession.id)
            pprint(participations)

if __name__ == '__main__':
    asyncio.run(main())
```
