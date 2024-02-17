import logging

import aiohttp


class BaseAPI:
    def __init__(self, base_link: str, base_token: str = ""):
        self._link = base_link
        self._token = base_token
        self.headers = {
            "Accept": "*/*",
        }

    async def get_json(self, route: str, params: dict | None = None):
        if params is None:
            params = {}
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(
                    url=f"{self._link}{route}",
                    params=params,
                    verify_ssl=False,
                ) as resp:
                    if resp.ok:
                        logging.info(f"{resp.status} {self._link}{route} {params=}")
                        return await resp.json()
                    else:
                        raise aiohttp.ClientError
        except aiohttp.ClientConnectionError:
            logging.warning(f"Api is unreachable {self._link}{route}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def get_data(self, route: str, params: dict | None = None):
        if params is None:
            params = {}
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(
                    url=f"{self._link}{route}",
                    params=params,
                    verify_ssl=False,
                ) as resp:
                    if resp.ok:
                        logging.info(f"{resp.status} {self._link}{route}")
                        return await resp.read()
                    else:
                        raise aiohttp.ClientError
        except aiohttp.ClientConnectionError:
            logging.warning(f"Api is unreachable {self._link}{route}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def post_json(self, route: str, data: dict | None = None) -> dict:
        """
        Send post request to host
        :param route: request link
        :param data: json object to send
        :return: json object from host
        """
        headers = self.headers
        headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        if data is None:
            data = {}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(
                    f'{self._link}{route}',
                    data=data,
                    verify_ssl=False,
                ) as post:
                    if post.ok:
                        logging.info(f"{post.status=} {self._link}{route} {data=}")
                        return await post.json()
                    else:
                        raise aiohttp.ClientError
        except aiohttp.ClientConnectionError:
            logging.warning(f"Api is unreachable {self._link}{route}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def put(self, route: str, data: dict | None = None) -> int:
        """
        Send put request to host
        :param route: request link
        :param data: json object to send
        :return: json object from host
        """
        headers = self.headers
        headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        if data is None:
            data = {}
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.put(
                    f'{self._link}{route}',
                    data=data,
                    verify_ssl=False,
                ) as put:
                    if put.ok:
                        logging.info(f"{put.status=} {self._link}{route} {data=}")
                        return put.status
                    else:
                        raise aiohttp.ClientError
        except aiohttp.ClientConnectionError:
            logging.warning(f"Api is unreachable {self._link}{route}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")

    async def delete(self, route: str, data: dict | None = None) -> int:
        if data is None:
            data = {}
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.delete(
                    url=f"{self._link}{route}",
                    data=data,
                    verify_ssl=False,
                ) as resp:
                    if resp.ok:
                        logging.info(f"{resp.status} {self._link}{route} {data=}")
                        return resp.status
                    else:
                        raise aiohttp.ClientError
        except aiohttp.ClientConnectionError:
            logging.warning(f"Api is unreachable {self._link}{route}")
        except Exception as e:
            logging.warning(f"Api is unreachable: {e}")


