from observer_sandbox import ai, ai_control, ai_runtime
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def _model(model_id: str, name: str) -> dict:
    return {
        "id": model_id,
        "name": name,
        "context_length": 128000,
        "capabilities": {"reasoning": True},
    }


def test_nanogpt_subscription_and_all_catalog_modes_are_explicit(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_NANOGPT_API_KEY", "test-key")
    calls: list[str] = []

    def fake_get_json(url, headers=None, timeout=20.0):
        calls.append(url)
        if "/subscription/v1/models" in url:
            return {"data": [_model("sub/model", "Subscription Model")]}
        if "/paid/v1/models" in url:
            return {"data": [_model("paid/model", "Paid Model")]}
        raise AssertionError(url)

    monkeypatch.setattr(ai, "_get_json", fake_get_json)
    with connect(db) as conn:
        assert ai_control.refresh_provider_catalog(conn, "nanogpt", catalog_mode="subscription") == 1
        subscription_models = ai_control.models_for_provider(conn, "nanogpt")
        assert [item["model_id"] for item in subscription_models] == ["sub/model"]
        assert subscription_models[0]["metadata"]["observer_nanogpt_billing_scope"] == "subscription"

        calls.clear()
        assert ai_control.refresh_provider_catalog(conn, "nanogpt", catalog_mode="all") == 2
        all_models = {item["model_id"]: item for item in ai_control.models_for_provider(conn, "nanogpt")}
        assert set(all_models) == {"sub/model", "paid/model"}
        assert all_models["sub/model"]["metadata"]["observer_nanogpt_billing_scope"] == "subscription"
        assert all_models["paid/model"]["metadata"]["observer_nanogpt_billing_scope"] == "paid"
        assert any("/subscription/v1/models?detailed=true" in url for url in calls)
        assert any("/paid/v1/models?detailed=true" in url for url in calls)


def test_nanogpt_inference_routes_subscription_and_paid_models_separately(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_NANOGPT_API_KEY", "test-key")
    urls: list[str] = []

    def fake_post(url, *, headers, payload, timeout=45.0):
        urls.append(url)
        return {"choices": [{"message": {"content": '{"action":"idle","duration_minutes":1,"target":"","reason":"probe"}'}}]}

    monkeypatch.setattr(ai_runtime, "_post_json", fake_post)
    with connect(db) as conn:
        provider = conn.execute("SELECT * FROM ai_providers WHERE id='nanogpt'").fetchone()
        ai_runtime._generate_nanogpt(provider, "test-key", "sub/model", "probe", {}, billing_scope="subscription")
        ai_runtime._generate_nanogpt(provider, "test-key", "paid/model", "probe", {}, billing_scope="paid")

    assert urls[0].endswith("/subscription/v1/chat/completions")
    assert urls[1].endswith("/v1/chat/completions")


def test_nanogpt_runtime_scope_is_read_from_cached_model_metadata(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            """
            INSERT INTO ai_models(provider_id,model_id,display_name,metadata_json,active)
            VALUES('nanogpt','paid/model','Paid Model','{"observer_nanogpt_billing_scope":"paid"}',1)
            """
        )
        conn.commit()
        assert ai_runtime.nanogpt_model_billing_scope(conn, "paid/model") == "paid"
        assert ai_runtime.nanogpt_model_billing_scope(conn, "unknown/model") == "subscription"
