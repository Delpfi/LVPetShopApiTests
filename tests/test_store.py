import requests
import allure
import jsonschema

from tests.schemas.inventory_schema import INVENTORY_SCHEMA
from tests.schemas.order_schema import ORDER_SCHEMA


BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    #42 TestIT Размещение заказа (POST /store/order) LV
    @allure.title("Размещение заказа")
    def test_new_order(self):

        with allure.step("Отправить запрос на размещение заказа с данными"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

            with allure.step("Проверка статуса ответа и валидация данных"):
                assert response.status_code == 200
                jsonschema.validate(response_json, ORDER_SCHEMA)

            with allure.step("Проверка параметров заказа в ответе"):
                assert response_json["id"] == payload["id"]
                assert response_json["petId"] == payload["petId"]
                assert response_json["quantity"] == payload["quantity"]
                assert response_json["status"] == payload["status"]
                assert response_json["complete"] == payload["complete"]

    #43 TestIT Получение информации о заказе по ID (GET /store/order/{orderId}) LV
    @allure.title("Получение информации о заказе по ID")
    def test_get_store_order(self,create_order):

        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]
        with allure.step("Отправить запрос на получения информации о закаке по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200
            assert response.json()["id"] == order_id

    #44 TestIT Удаление заказа по ID (DELETE /store/order/{orderId}) LV
    @allure.title("Удаление заказа по ID")
    def test_delete_order(self,create_order):

        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]
        with allure.step("Отправить запрос на удаления заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200
        with allure.step("Отправить запрос на получение информации по удаленному заказу"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404

    #45 TestIT Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId}) LV
    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):

        with allure.step("Отправить запрос на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")
            assert response.status_code == 404

    #46 TestIT Получение инвентаря магазина (GET /store/inventory) LV
    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):

        with allure.step("Отправить запрос на получение инвентаря магазина и проверка данных"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            assert response.status_code == 200
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)