from app import task_tracker

client = task_tracker.test_client()


class TestViews:

    def setup(self):
        task_tracker.testing = True
        self.client = task_tracker.test_client()

    def test_index(self):
        response = self.client.get("/")
        assert response.status_code == 200
        # assert 'Главная страница' in str(response.data)

    def test_create_task(self):
        response = self.client.get("/create_task")
        assert response.status_code == 302

    def test_login(self):
        response = self.client.post('/login', data=dict(
            login='test',
            password='test'
        ), follow_redirects=True)
        assert response.status_code == 200

    def test_logout(self):
        return self.client.get('/logout', follow_redirects=True)

