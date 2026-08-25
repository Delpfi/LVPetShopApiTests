import allure
import jsonschema
import pytest
import requests
from tests.schemas.pet_schema import PET_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):

        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    #38 TestIT Попытка обновить несуществующего питомца (PUT /pet)
    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    #37 TestIT Попытка получить информацию о несуществующем питомце (GET /pet/{petId}) LV
    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    #31 TestIT Добавление нового питомца (POST /pet)
    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)


        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'] , "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"


    #41 TestIT Добавление нового питомца c полными данными (POST /pet) LV
    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full_data(self):
        with allure.step("Подготовка полных данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"}

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA) #jsonschema.validate - проверка правильности структуры, типов данных и обязательных полей JSON-документа по заранее описанным правилам(PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе, полные данные "):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'] , "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "фотоурл питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "тег питомца не совпадает с ожидаемым"

    #32 TestIT Получение информации о питомце по ID
    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    #33 TestIT Обновление информации о питомце (PUT /pet) LV
    @allure.title("Обновление информации о питомце")
    def test_put_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправить запрос с подготовленными данными на обновления"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            assert response.status_code == 200
            assert response.json()["id"] == payload["id"]
            assert response.json()["name"] == payload["name"]
            assert response.json()["status"] == payload["status"]

    #34 TestIT Удаление питомца по ID (DELETE /pet/{petId}) LV
    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправить запрос на удаления питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации по удаленному питомцу"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    #35 TestIT Получение списка питомцев по статусу
    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [("available", 200),
         ("sold", 200),
         ("pending", 200),
         (" ", 400),
         ("failed", 400),
         ]
    )
    def test_get_pets_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status":{status}})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), list)
