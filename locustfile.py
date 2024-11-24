from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(2, 5)

    @task(2)
    def browse_products(self):
        # Fetch available products
        self.client.get("/products")

    @task(1)
    def view_cart(self):
        # Fetch items in a generic cart without a session ID
        self.client.get("/cart")

    @task(1)
    def confirm_order(self):
        # Place an order with hardcoded payment details and no session ID
        payload = {
            "sessionId": "h1",
            "cardNumber": "4111111111111111",
            "cardOwner": "John Doe",
            "checksum": "1234",
            "lastName": "Doe",
            "address1": "123 Main St",
            "cardType": "VISA"
        }
        self.client.post("/confirm", json=payload)
