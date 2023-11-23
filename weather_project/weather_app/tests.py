# Пример теста Django-вью
from django.test import TestCase, RequestFactory
from weather_project.views import forecasts, weather, process_cache, get_bot_status
from django.test import TestCase
from unittest.mock import patch
# http://localhost:7771/get_status


class MyViewTests(TestCase):
    def test_my_forecasts(self):
        factory = RequestFactory()
        request = factory.get('/forecasts', params={'city': 'Несуществующий город для теста'})
        response = forecasts(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NameCityError')

    def test_my_weather(self):
        factory = RequestFactory()
        request = factory.get('/weather', params={'city': 'Несуществующий город для теста'})
        response = weather(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NameCityError')

# Пример теста кэширования в редисе
class MyCachedFunctionTests(TestCase):
    @patch('weather_project.views.process_cache')
    def test_my_cached_function(self, mock_external_api):
        mock_external_api.return_value = {'data': 'example'}

        # Вызовем функцию в первый раз
        result_1 = process_cache('my_key')
        self.assertEqual(result_1, {'data': 'example'})
        mock_external_api.assert_called_once()

        # Вызовем функцию во второй раз, ожидаем кэшированный результат
        result_2 = process_cache('my_key')
        self.assertEqual(result_2, {'data': 'example'})
        mock_external_api.assert_called_once()  # Функция не вызывается второй раз из-за кэширования

class MyCachedFunctionTests(TestCase):
    @patch('weather_project.views.requests.get')
    def test_get_bot_status(self, mock_requests_get):
        mock_requests_get.return_value.text = 'Status OK'
        result = get_bot_status()
        self.assertEqual(result, 'Status OK')
        mock_requests_get.assert_called_once_with("http://bot:7772/get_status")
