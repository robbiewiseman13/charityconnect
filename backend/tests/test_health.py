def test_health(client):
    from django.urls import reverse
    r = client.get(reverse("health"))
    assert r.status_code == 200
    assert r.content == b"ok"
