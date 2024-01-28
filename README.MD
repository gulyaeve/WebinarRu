# Python-клиент для платформы webinar.ru

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
    timezones = await webinar.get_timezones()
    pprint(timezones)


if __name__ == '__main__':
    asyncio.run(main())
```