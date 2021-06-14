import random
import string
import time

from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(9, 11)
    host = 'http://127.0.0.1:8443'

    @task
    def signups(self):
        letters = string.ascii_letters + string.digits
        user = ''.join(random.SystemRandom().choice(letters) for _ in range(5))
        self.client.post(f"/signup?username={user}&age=20&password={user}", verify=False)
        while 1:
            self.client.post(f"/?username={user}&password={user}", verify=False)
            self.client.post(f"/logout", verify=False)
            time.sleep(9)

    @task
    def guests(self):
        while 1:
            self.client.get(f"/guest_dashboard?", verify=False)
            self.client.post(f"/logout", verify=False)
            time.sleep(9)

    def on_start(self):
        self.client.get("/", verify=False)
