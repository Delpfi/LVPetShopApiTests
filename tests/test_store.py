import requests
import allure
import jsonschema
BASE_URL = "http://5.181.109.28:9090/api/v3"
from tests.schemas.inventory_schema import INVENTORY_SCHEMA
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
            assert response.status_code == 200
            assert response.json()["id"] == payload["id"]
            assert response.json()["petId"] == payload["petId"]
            assert response.json()["quantity"] == payload["quantity"]
            assert response.json()["status"] == payload["status"]
            assert response.json()["complete"] == payload["complete"]

    #43 TestIT Получение информации о заказе по ID (GET /store/order/{orderId}) LV
    @allure.title("Получение информации о заказе по ID")
    def test_get_store_order(self):

        with allure.step("Отправить запрос на получения информации о закаке по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            assert response.status_code == 200
            assert response.json()["id"] == 1

    #44 TestIT Удаление заказа по ID (DELETE /store/order/{orderId}) LV
    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):

        with allure.step("Отправить запрос на удаления заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")
            assert response.status_code == 200
        with allure.step("Отправить запрос на получение информации по удаленному заказу"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
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