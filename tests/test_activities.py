def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    email = "tester@example.com"
    resp = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
    email = "dup@example.com"
    resp1 = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert resp1.status_code == 200
    resp2 = client.post("/activities/Chess%20Club/signup?email=" + email)
    assert resp2.status_code == 400


def test_remove_participant(client):
    email = "remove_me@example.com"
    # sign up first
    client.post("/activities/Chess%20Club/signup?email=" + email)
    resp = client.delete("/activities/Chess%20Club/participants?email=" + email)
    assert resp.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent(client):
    resp = client.delete("/activities/Chess%20Club/participants?email=notfound@example.com")
    assert resp.status_code == 404
