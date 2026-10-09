
from locust import HttpUser, task, between
from uuid import uuid4


class UsuarioAPI(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def listar_usuarios(self):
        with self.client.get(
            "/api/users?page=1&per_page=20",
            name="GET /api/users",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Error HTTP {response.status_code}")

    @task(3)
    def listar_correos(self):
        with self.client.get(
            "/api/users/emails?page=1&per_page=20",
            name="GET /api/users/emails",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Error HTTP {response.status_code}")

    @task(3)
    def mayores_20(self):
        with self.client.get(
            "/api/users/over-twenty?page=1&per_page=20",
            name="GET /api/users/over-twenty",
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Error HTTP {response.status_code}")

    @task(1)
    def crear_usuarios(self):
        identificador = uuid4().hex

        datos = {
            "users": [
                {
                    "name": "Usuario Prueba 1",
                    "email": f"usuario1_{identificador}@test.com",
                    "birth_date": "1998-05-12"
                },
                {
                    "name": "Usuario Prueba 2",
                    "email": f"usuario2_{identificador}@test.com",
                    "birth_date": "2000-11-03"
                },
                {
                    "name": "Usuario Prueba 3",
                    "email": f"usuario3_{identificador}@test.com",
                    "birth_date": "1995-01-20"
                }
            ]
        }

        with self.client.post(
            "/api/users/bulk",
            json=datos,
            name="POST /api/users/bulk",
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Error HTTP {response.status_code}")
