import requests
import json
from typing import Optional


class InfrastructureChecker:
    def __init__(self):
        self.base_url = 'https://catalog.api.2gis.com/3.0/items?'
        self.key = '2dfc0b30-cdb7-4014-9142-4d101cb77824'

    def _make_request(self, url: str) -> Optional[dict]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Ошибка API: {e}") from e
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка соединения: {e}") from e
        except json.JSONDecodeError as e:
            raise Exception(f"Ошибка разбора JSON: {e}") from e

    def check_infrastructure(self, infra_type: str, x: float, y: float) -> int:
        url = f"{self.base_url}q={infra_type}&point={x}%2C{y}&radius=1000&key={self.key}"
        data = self._make_request(url)
        print(data)
        if data and data.get('result', {}).get('items'):
            return 10
        url = f"{self.base_url}q={infra_type}&point={x}%2C{y}&radius=666&key={self.key}"
        data = self._make_request(url)
        print(data)
        if data and data.get('result', {}).get('items'):
            return 5
        return 0

infra = InfrastructureChecker()
infra_type = "массажка"
x = 37.625262
y = 55.697711
print(infra.check_infrastructure(infra_type, x, y))