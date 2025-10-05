from check_distance import InfrastructureChecker


class Scoring:
    def __init__(self, x: float, y: float):  # Исправлен тип на float
        self.x = x
        self.y = y
        self.infa = InfrastructureChecker()
        self.score = 0
        self.category_rate = dict()

    def calculate(
        self, inf_type: str, min_dist: int, max_dist: int
    ) -> None:  # Добавлен тип возврата
        try:
            distance = self.infa.check_closest_inf(inf_type, self.x, self.y)
            if distance is None:
                print(f"Не удалось получить расстояние до {inf_type}")
                return

            # Исправленная формула расчета баллов
            if distance <= min_dist:
                points = 10
            elif distance >= max_dist:
                points = 0
            else:
                # Линейное уменьшение от min_dist к max_dist
                points = 10 * (1 - (distance - min_dist) / (max_dist - min_dist))

            self.score += points

        except Exception as e:
            print(f"Ошибка при расчете для {inf_type}: {e}")

    def return_score(self) -> float:  # Изменен тип на float
        return self.score


# Использование
x = 55.69756
y = 37.62522

conditions = {
    # Транспорт и мобильность
    "метро": [200, 2000],
    "остановка_автобуса": [100, 500],
    "велодорожка": [300, 1500],
    # Образование и развитие
    "детский_сад": [200, 1000],
    "школа": [500, 2000],
    "библиотека": [1000, 3000],
    # Здравоохранение
    "больница": [1000, 5000],
    "поликлиника": [500, 2000],
    "аптека": [300, 1500],
    # Отдых и спорт
    "парк": [300, 1500],
    "спортплощадка": [500, 2000],
    # Покупки и услуги
    "супермаркет": [300, 1500],
    "продуктовый_магазин": [200, 1000],
    "торговый_центр": [1000, 5000],
    # Социальная инфраструктура
    "кафе": [300, 2000],
    "ресторан": [500, 3000],
    "банк": [500, 2500],
    "почта": [1000, 4000],
    # Безопасность
    "отделение_полиции": [1000, 5000],
    "пожарная_часть": [2000, 8000],
    # Культура и развлечения
    "кинотеатр": [1000, 5000],
    "театр": [2000, 10000],
    "музей": [2000, 10000],
    # Специализированные объекты
    "автосервис": [1000, 5000],
    "автомойка": [1000, 5000],
    "строймаркет": [2000, 10000],
}

# Создаем объект оценки
sc = Scoring(x, y)

# Исправленный цикл (убрали дубликаты и исправили итерацию)
for inf_type, distances in conditions.items():  # Исправлено на items()
    sc.calculate(inf_type, distances[0], distances[1])

print(f"\nИтоговый балл: {sc.return_score():.1f}")
print(f"Максимально возможный: {len(conditions) * 10}")
print(f"Процент качества: {(sc.return_score() / (len(conditions) * 10)) * 100:.1f}%")
