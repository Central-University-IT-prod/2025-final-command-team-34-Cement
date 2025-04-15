from rest_framework.test import APITestCase
import json

class TestObjectAPI(APITestCase):
    def setUp(self):
        self.base_url = "/api"
        self.single_tag = {"name": "tag1"}
        self.tags_array = [{"name": "tag2"},{"name": "tag3"},{"name": "tag4"}]

        self.single_create_exp = self.single_tag.copy()
        self.single_create_exp["id"] = 1

        self.create_exp = self.tags_array.copy()
        self.create_exp[0]["id"] = 2
        self.create_exp[1]["id"] = 3
        self.create_exp[2]["id"] = 4

        self.reg_data = {
            "login": "string",
            "tg": "user@example.com",
            "password": "stringst",
            "description": "string",
            "course": 3,
            "role": "mentor",
            "fio": "fio",
            "tags": [1,2,3]
        }
        self.expected_create = self.reg_data.copy()
        self.expected_create.pop("password")
        self.expected_create["id"] = 1
        self.expected_create["mentor_rating"] = 0

    def test_tags(self):
        base_url = self.base_url
        response = self.client.post(base_url + "/tags/", data=self.single_tag)
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.single_create_exp, response.data)

        tag_id = response.data["id"]
        response = self.client.get(base_url + "/tags/" + str(tag_id) + "/")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"id": tag_id, "name": self.single_tag["name"]}, response.data)

        response = self.client.post(
            base_url + "/tags/bulk/",
            data=json.dumps(self.tags_array),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.create_exp, response.data)

        for i in range(0, 3):
            tag_id = response.data[i]["id"]
            get_response = self.client.get(base_url + "/tags/" + str(tag_id) + "/")
            self.assertEqual(200, get_response.status_code)
            self.assertEqual({"id": tag_id, "name": self.tags_array[i]["name"]}, get_response.data)

        response = self.client.post(base_url + '/auth/', data=self.reg_data)
        self.assertEqual(201, response.status_code)

        token = response.data["token"]
        response = self.client.get(base_url + '/users/me/', headers={"Authorization": ("Bearer " + token)})
        self.assertEqual(response.status_code, 200)
