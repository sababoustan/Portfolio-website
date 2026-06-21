from locust import HttpUser, task, between


class APIUser(HttpUser):
    host = "http://web:8000"
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post('/api/accounts/token/', json={
            "username": "saba",
            "password": "sba80boo"
        })
        if response.status_code == 200:
            token = response.json().get("access")
            self.client.headers = {
                "Authorization": f"Bearer {token}"
            }
        else:
            print("Login failed:", response.text)

    @task(3)
    def get_products(self):
        self.client.get("/api/products/products-list/")

    @task(1)
    def get_profile(self):
        self.client.get("/api/accounts/profile/")
