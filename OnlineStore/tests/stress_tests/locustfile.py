import random
import string

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(5, 8)
    host = 'http://127.0.0.1:8443'

    @task
    def signups(self):
        letters = string.ascii_letters + string.digits
        user = ''.join(random.SystemRandom().choice(letters) for _ in range(5))
        self.client.post(f"/signup?username={user}&age=20&password={user}", verify=False)
        self.client.post(f"/?username={user}&password={user}", verify=False)
        self.client.post(f"/logout", verify=False)


    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    # def on_start(self):
    #     self.client.get("/")
