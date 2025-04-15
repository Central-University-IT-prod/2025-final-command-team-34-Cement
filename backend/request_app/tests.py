import json

from rest_framework.test import APITestCase


class TestObjectAPI(APITestCase):
    def setUp(self):
        self.base_url = "/api"
        self.student_reg_data = {
            "login": "student",
            "tg": "student_tg",
            "password": "stringst",
            "description": "string",
            "course": 3,
            "role": "student",
            "fio": "fio"
        }
        self.mentor_reg_data = self.student_reg_data.copy()
        self.mentor_reg_data["login"] = "mentor1"
        self.mentor_reg_data["tg"] = "mentor_tg1"
        self.mentor_reg_data["role"] = "mentor"
        self.tags_array = [{"name": "tag2"}, {"name": "tag3"}, {"name": "tag4"}]
        self.create_tag_req = {
            "mentor": 2,
            "tags": [
                1,2,3
            ],
            "problem": "string"
        }
        self.exp_after_create = self.create_tag_req.copy()
        self.exp_after_create["student"] = 1
        self.exp_after_create["status"] = "in_progress"


    def test_requests(self):
        base_url = self.base_url
        response = self.client.post(base_url + '/auth/', data=self.student_reg_data)
        self.assertEqual(201, response.status_code)
        student_token = response.data["token"]

        response = self.client.post(base_url + '/requests/', data = self.create_tag_req,
                                    headers={"Authorization": "Bearer " + student_token})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(
            base_url + "/tags/bulk/",
            data=json.dumps(self.tags_array),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        response = self.client.post(base_url + '/requests/', data = self.create_tag_req,
                                    headers={"Authorization": "Bearer " + student_token})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(base_url + '/auth/', data=self.mentor_reg_data)
        self.assertEqual(201, response.status_code)
        mentor_token = response.data["token"]

        response = self.client.post(base_url + '/requests/', data=self.create_tag_req,
                                   headers={"Authorization": "Bearer " + mentor_token})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(base_url + '/requests/', data=self.create_tag_req,
                                    headers={"Authorization": "Bearer " + student_token})
        self.assertEqual(response.status_code, 201)
