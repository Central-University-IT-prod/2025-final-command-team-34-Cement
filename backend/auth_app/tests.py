from rest_framework.test import APITestCase


class TestObjectAPI(APITestCase):
    def setUp(self):
        self.base_url = "/api"
        self.reg_data = {
            "login": "string",
            "tg": "user@example.com",
            "password": "stringst",
            "description": "string",
            "course": 3,
            "role": "student",
            "fio": "fio"
        }
        self.expected_reg = self.reg_data.copy()
        self.expected_reg.pop("password")
        self.expected_reg["token"] = "to_add"

        self.expected_create = self.reg_data.copy()
        self.expected_create.pop("password")
        self.expected_create["id"] = 1
        self.expected_create["profile_image"] = None

        self.patch_data = {
            "login": "new_login",
            "tg": "newemail@example.com",
            "description": "new_desc",
            "course": 2,
            "role": "admin",
            "fio": "new_fio"
        }
        self.expected_patch = self.patch_data.copy()
        self.expected_patch["profile_image"] = None
        self.expected_patch["id"] = 1

    def test_auth(self):
        base_url = self.base_url
        response = self.client.post(base_url + '/auth/', data=self.reg_data)
        self.assertEqual(201, response.status_code)

        self.expected_reg["token"] = response.data["token"]
        self.expected_reg["tags"] = []
        self.expected_reg["profile_image"] = None
        self.assertEqual(response.data, self.expected_reg)

        old_token = response.data["token"]
        login = self.reg_data["login"]
        old_password = self.reg_data["password"]

        response = self.client.post(base_url + '/auth/login/', {"login": login, "password": old_password})
        self.assertEqual(response.status_code, 200)
        token = response.data["token"]

        new_password = "new_password"
        response = self.client.post(base_url + '/users/change_password/',
                                    {"old_password": old_password, "new_password": new_password},
                                    headers={"Authorization": ("Bearer " + old_token)})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(base_url + '/users/change_password/',
                                    {"old_password": old_password, "new_password": new_password},
                                    headers={"Authorization": ("Bearer " + "random shi")})
        self.assertEqual(response.status_code, 403)

        response = self.client.post(base_url + '/users/change_password/',
                                    {"old_password": "wrong password", "new_password": new_password},
                                    headers={"Authorization": ("Bearer " + str(token))})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(base_url + '/auth/login/', {"login": login, "password": old_password})
        self.assertEqual(response.status_code, 403)
        response = self.client.post(base_url + '/auth/login/', {"login": login, "password": new_password})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(base_url + '/auth/', data=self.reg_data)
        self.assertEqual(400, response.status_code)

    def test_user(self):
        base_url = self.base_url
        response = self.client.post(base_url + '/auth/', data=self.reg_data)
        self.assertEqual(201, response.status_code)

        token = response.data["token"]
        response = self.client.get(base_url + '/users/me/', headers={"Authorization": ("Bearer " + token)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.expected_create)

        response = self.client.patch(base_url + '/users/me/',self.patch_data,
                                     headers={"Authorization": ("Bearer " + token)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.expected_patch)

        response = self.client.get(base_url + '/users/me/', headers={"Authorization": ("Bearer " + token)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.expected_patch)
