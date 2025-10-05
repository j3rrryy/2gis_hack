import requests
import json
from typing import Optional, Dict, List, Any
from var_dto import LocationDto, PointDto, RoutingRequestDto


def parse_first_item_to_point_dto(data: dict) -> PointDto:
    try:
        items = data.get('result', {}).get('items', [])

        if not items:
            print("Список items пуст, возвращаю PointDto с значениями по умолчанию")
            return PointDto()

        first_item = items[0]
        print(
            f"Найден объект: ID={first_item.get('id')}, координаты=({first_item.get('lat')}, {first_item.get('lon')})")

        point_dto = PointDto(
            type='stop',
            lat=first_item.get('lat'),
            lon=first_item.get('lon')
        )

        return point_dto

    except Exception as e:
        print(f"Ошибка при парсинге первого элемента: {e}")
        return PointDto()


class InfrastructureChecker:
    def __init__(self):
        self.base_url_makers = 'https://catalog.api.2gis.com/3.0/markers?'
        self.base_url_routing = 'http://routing.api.2gis.com/routing/7.0.0/global?'
        self.key = '2dfc0b30-cdb7-4014-9142-4d101cb77824'

    def _make_request_get(self, url: str) -> Optional[dict]:
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

    def _make_request_post(self, url: str, params: dict) -> Optional[dict]:
        try:
            headers = {"Content-Type": "application/json"}
            json_params = params.model_dump()
            response = requests.post(url, json=json_params, headers=headers)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка HTTP запроса: {e}")

    def check_closest_inf(self, infra_type: str, x: float, y: float) -> int:
        url_markers = f"{self.base_url_makers}q={infra_type}&point={y}%2C{x}&radius=1000&sort=distance&key={self.key}"
        data = self._make_request_get(url_markers)
        print(data)
        item = parse_first_item_to_point_dto(data)
        print(item)
        items = [PointDto(type='stop', lat=item.lat, lon=item.lon)]
        items.append(PointDto(type='stop', lat=x, lon=y))
        routing_params = RoutingRequestDto(
            points=items,
            locale="ru",
            transport="walking",
            route_mode="fastest",
            traffic_mode="jam"
        )
        url_routing = f"{self.base_url_routing}&key={self.key}"
        route = self._make_request_post(url_routing, routing_params)
        r_l = self.get_route_length(route)
        return r_l

    def sum_maneuvers_distance(self, route: Dict[str, Any]) -> Optional[int]:
        try:
            if 'maneuvers' not in route:
                return None

            total_distance = 0
            for maneuver in route['maneuvers']:
                if 'outcoming_path' in maneuver and 'distance' in maneuver['outcoming_path']:
                    total_distance += maneuver['outcoming_path']['distance']

            return total_distance if total_distance > 0 else None

        except Exception as e:
            print(f"Ошибка при суммировании маневров: {e}")
            return None

    def get_route_length(self, route_data: Dict[str, Any]) -> Optional[int]:
        print(route_data)
        try:
            if not route_data or 'result' not in route_data:
                print("Отсутствует ключ 'result' в данных маршрута")
            results = route_data['result']
            if not results:
                print("Список маршрутов пуст")
                return None
            first_route = results[0]
            if 'total_distance' in first_route:
                distance = first_route['total_distance']
                print(f"Длина маршрута: {distance} м")
                return distance
            elif 'ui_total_distance' in first_route:
                ui_distance = first_route['ui_total_distance']
                if 'value' in ui_distance:
                    try:
                        distance = int(ui_distance['value'])
                        print(f"Длина маршрута: {distance} м")
                        return distance
                    except (ValueError, TypeError):
                        print(f"Некорректное значение расстояния: {ui_distance['value']}")
            else:
                total_from_maneuvers = self.sum_maneuvers_distance(first_route)
                if total_from_maneuvers:
                    print(f"Длина маршрута (сумма маневров): {total_from_maneuvers} м")
                    return total_from_maneuvers

            print("Не удалось извлечь длину маршрута")
            return None

        except Exception as e:

            return None




infra = InfrastructureChecker()
infra_type = "дрочильня"
x = 55.69756
y = 37.62522
infra.check_closest_inf(infra_type, x, y)