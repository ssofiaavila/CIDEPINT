from web import create_app


app = create_app(env="test")

client = app.test_client()

def test_web():
    response = client.get("/")
    assert response.status_code == 200