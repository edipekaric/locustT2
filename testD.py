from locust import HttpUser, task, between
import random
import uuid
from datetime import datetime
import time

# Global counter for session ID increment
session_counter = 0

class LoadTestUser(HttpUser):
    wait_time = between(20, 30) #Task D)d), add think time

    # Static list of product IDs
    product_ids = [
        "090d388b-48d0-4f74-902d-bbf9d183b6db", "0d0532bf-89aa-4b8e-bd78-ddf013496b16",
        "29eae5f6-b9b8-4e35-9d1b-354b39afb03b", "32798fe4-d45c-49b2-881d-ab01a8365f5d",
        "38fd2598-2584-48e1-b886-81b40d3c61f1", "440fd909-4764-44db-8d60-f28f7cbbccc0",
        "4897ccd9-87b7-4f98-8125-09eaf82a7664", "48f31947-f1bd-47c4-ad2e-54ee5363a9b0",
        "492f655c-8954-4197-b4e2-e40a3e09a46c", "49efe262-671b-4455-8276-9ea57876bb29",
        "4d219109-1fcf-4f6e-abbc-eee84f61e923", "51ae158c-181d-4bdd-acdc-de6f1420de1c",
        "54590fe6-9e46-44de-b877-7b1646ada263", "6564b835-7516-4404-b02c-c0b106d892cc",
        "700de00a-b931-497e-9a7b-e4b555e5724b", "77b8bcb1-b347-4553-9c88-1c02955426de",
        "99623092-00b2-4d02-8412-ef7cea692332", "a8994f0f-6e08-49cb-aefd-a2f525059703",
        "b5d20b73-0146-4ebc-8570-b1a950c089a2", "bd341732-240d-45ce-b053-11365d9a2410",
        "d3264a86-a9e5-4087-8d3c-d861f16e725d", "d82b01d6-f49f-4377-a6c8-8ea66a6124f2",
        "dd06342b-c979-4bea-87da-dd1d3b7aadeb", "fa671b44-4bfa-43af-b28a-f818b886b77e",
        "fc238fe4-79bc-4643-8e89-10137f69d53c"
    ]

    def on_start(self):
        """Initialize a unique session ID."""
        global session_counter
        session_counter += 1
        self.session_id = f"session-{session_counter}"  # Unique session ID
        print(f"Session started with ID: {self.session_id}")

    @task
    def mainExecution(self):
        self.browse_products()
        self.add_to_cart()
        self.confirm_order()
        #self.stop()

    def browse_products(self):
        """Fetch the list of products from the /products endpoint."""
        #Task D)a), browse all alailable items/products
        response = self.client.get("/products")
        if response.status_code == 200 or response.status_code == 201:
            print(f"Fetched products for session {self.session_id}.")
            products = response.json()  # Assume the response is a JSON array of product details
            # Use the product IDs from the response if available, otherwise use the static list
            self.available_products = [product["id"] for product in products] if products else self.product_ids
        else:
            print(f"Failed to fetch products: {response.status_code}, {response.text}")
            self.available_products = self.product_ids  # Fallback to static list if the request fails

    def add_to_cart(self):
        #Task D)b), add configurable amout of random items to cart
        num_items = random.randint(1, 5)  # Random number of items to add
        cart_content = {}

        # Select random product IDs and quantities
        for _ in range(num_items):
            product_id = random.choice(self.available_products)
            quantity = random.randint(1, 3)  # Random quantity between 1 and 3
            cart_content[product_id] = quantity

        # Create payload for the cart
        payload = {
            "id": self.session_id,
            "content": cart_content,
            "creationDate": datetime.now().isoformat()
        }

        # Send POST request to create the cart
        response = self.client.post("/cart", json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Cart created for session {self.session_id} with {num_items} items.")
        else:
            print(f"Failed to create cart: {response.status_code}, {response.text}")


    def confirm_order(self):
        #Task D)c), Confirm order from cart
        time.sleep(7)
        #sleeping time is the last digit of student id
        """Confirm the order."""
        payload = {
            "sessionId": self.session_id,
            "cardNumber": str(random.randint(4000000000000000, 4999999999999999)),
            "cardOwner": f"User-{uuid.uuid4().hex[:8]}",
            "checksum": str(random.randint(1000, 9999)),
            "lastName": f"Last-{uuid.uuid4().hex[:4]}",
            "address1": f"{random.randint(1, 9999)} {random.choice(['Main St', 'Elm St', 'Oak Ave', 'Pine Rd'])}",
            "cardType": random.choice(["VISA", "MasterCard"])
        }
        response = self.client.post("/confirm", json=payload)
        if response.status_code == 200:
            print(f"Order confirmed for session {self.session_id}.")
        else:
            print(f"Failed to confirm order: {response.status_code}, {response.text}")