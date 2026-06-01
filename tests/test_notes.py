"""
笔记 API 测试 — 覆盖 CRUD + 异常场景
"""
import json
import pytest
import os
from core.logger import logger

# 加载测试数据
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
with open(os.path.join(DATA_DIR, "test_data.json"), encoding="utf-8") as f:
    test_data = json.load(f)


class TestHealth:
    """健康检查接口测试"""

    def test_health_check(self, client):
        """GET /health — 应返回 ok"""
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestCreateNote:
    """创建笔记测试"""

    @pytest.mark.parametrize("note_data", test_data["valid_notes"])
    def test_create_note_success(self, client, note_data):
        """POST /notes — 创建成功应返回 201 及笔记内容"""
        resp = client.post("/notes", json=note_data)
        assert resp.status_code == 201

        body = resp.json()
        assert body["title"] == note_data["title"]
        assert body["content"] == note_data["content"]
        assert "id" in body

        # 保存 ID 供后续测试使用
        pytest.last_note_id = body["id"]
        logger.info(f"创建的笔记 ID: {body['id']}")

    @pytest.mark.parametrize("note_data", test_data["invalid_notes"])
    def test_create_note_invalid(self, client, note_data):
        """POST /notes — 非法数据应返回 422"""
        resp = client.post("/notes", json={
            "title": note_data["title"],
            "content": note_data["content"],
        })
        assert resp.status_code == note_data["expected_status"]


class TestListNotes:
    """获取笔记列表测试"""

    def test_list_notes(self, client):
        """GET /notes — 应返回列表"""
        resp = client.get("/notes")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestGetNote:
    """获取单条笔记测试"""

    def test_get_note_success(self, client):
        """GET /notes/{id} — 存在的笔记应返回 200"""
        note_id = getattr(pytest, "last_note_id", None)
        if not note_id:
            pytest.skip("需要先创建一条笔记")

        resp = client.get(f"/notes/{note_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == note_id

    def test_get_note_not_found(self, client):
        """GET /notes/{id} — 不存在的笔记应返回 404"""
        resp = client.get("/notes/nonexistent")
        assert resp.status_code == 404
        assert "笔记不存在" in resp.json()["detail"]


class TestUpdateNote:
    """更新笔记测试"""

    def test_update_note_success(self, client):
        """PUT /notes/{id} — 更新成功应返回新内容"""
        note_id = getattr(pytest, "last_note_id", None)
        if not note_id:
            pytest.skip("需要先创建一条笔记")

        update_data = {"title": "已更新", "content": "内容已修改"}
        resp = client.put(f"/notes/{note_id}", json=update_data)
        assert resp.status_code == 200

        body = resp.json()
        assert body["title"] == "已更新"
        assert body["content"] == "内容已修改"

    def test_update_note_not_found(self, client):
        """PUT /notes/{id} — 不存在的笔记应返回 404"""
        resp = client.put("/notes/nonexistent", json={"title": "新标题"})
        assert resp.status_code == 404


class TestDeleteNote:
    """删除笔记测试"""

    def test_delete_note_success(self, client):
        """DELETE /notes/{id} — 删除成功应返回 204"""
        note_id = getattr(pytest, "last_note_id", None)
        if not note_id:
            pytest.skip("需要先创建一条笔记")

        resp = client.delete(f"/notes/{note_id}")
        assert resp.status_code == 204

        # 验证已删除
        get_resp = client.get(f"/notes/{note_id}")
        assert get_resp.status_code == 404

    def test_delete_note_not_found(self, client):
        """DELETE /notes/{id} — 不存在的笔记应返回 404"""
        resp = client.delete("/notes/nonexistent")
        assert resp.status_code == 404