import json

from rest_framework.test import APITestCase


class TestObjectAPI(APITestCase):
    def setUp(self):
        self.tags_array = [{"name": "tag1"}, {"name": "tag2"}, {"name": "tag3"}]
        self.reg_data = {
            "login": "string",
            "tg": "baushev",
            "password": "stringst",
            "description": "string",
            "course": 3,
            "role": "mentor",
            "fio": "fio",
            "tags": [1, 2, 3]
        }
        self.exp_tags_stats = [
            {"id": 1, "name": "tag1", "mentors": 3},
            {"id": 2, "name": "tag2", "mentors": 2},
            {"id": 3, "name": "tag3", "mentors": 1}
        ]

    def test_tags_stats(self):
        base_url = "/api"
        response = self.client.post(
            base_url + "/tags/bulk/",
            data=json.dumps(self.tags_array),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        response = self.client.post(base_url + "/auth/", data=self.reg_data)
        self.assertEqual(201, response.status_code)

        self.reg_data["login"] = "login2"
        self.reg_data["tg"] = "tg2"
        self.reg_data["tags"] = [1, 2]
        response = self.client.post(base_url + "/auth/", data=self.reg_data)
        self.assertEqual(201, response.status_code)

        self.reg_data["login"] = "login3"
        self.reg_data["tg"] = "tg3"
        self.reg_data["tags"] = [1]
        response = self.client.post(base_url + "/auth/", data=self.reg_data)
        self.assertEqual(201, response.status_code)

        response = self.client.get(base_url + "/analytics/mentors/tags/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.exp_tags_stats, response.data)
