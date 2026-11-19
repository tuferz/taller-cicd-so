import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Usamos una BD temporal por cada prueba para no ensuciar datos reales
    test_db = str(tmp_path / "test_notas.db")
    monkeypatch.setattr(app_module, "DB_PATH", test_db)
    app_module.init_db()
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_inicio_vacio(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_notas"] == 0
    assert "contenedor_id" in data


def test_agregar_y_listar_nota(client):
    res = client.post("/notas", json={"texto": "Hola desde CI/CD"})
    assert res.status_code == 201

    res_lista = client.get("/")
    data = res_lista.get_json()
    assert data["total_notas"] == 1
    assert data["notas"][0]["texto"] == "Hola desde CI/CD"


def test_nota_vacia_falla(client):
    res = client.post("/notas", json={"texto": "   "})
    assert res.status_code == 400
