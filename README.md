# 🧪 API 接口自动化测试框架

[![API Tests](https://github.com/wanzhiwei5/api-test-framework/actions/workflows/test.yml/badge.svg)](https://github.com/wanzhiwei5/api-test-framework/actions/workflows/test.yml)

> 从零搭建的企业级接口自动化测试框架，基于 **Python + pytest + requests**，集成 **GitHub Actions CI/CD**。

---

## 📋 项目介绍

本项目是一个完整的 API 自动化测试框架，对一套**笔记管理系统（REST API）**进行了全面的接口测试覆盖。

### 你能从这个项目学到什么

| 技能 | 说明 |
|------|------|
| 🐍 Python 测试开发 | 用 pytest 写自动化测试用例 |
| 🔗 HTTP 接口测试 | 覆盖 GET / POST / PUT / DELETE |
| 📊 数据驱动测试 | 测试数据与代码分离，JSON 参数化 |
| ⚙️ 框架设计 | 配置管理 / 日志系统 / 客户端封装 |
| 🤖 CI/CD | GitHub Actions 自动运行测试 |
| 📈 测试报告 | 生成 HTML 可视化报告 |

---

## 🏗️ 项目架构

```
api-test-framework/
│
├── app/                        # 被测系统（演示用）
│   └── main.py                # FastAPI 笔记 REST API（6 个接口）
│
├── core/                       # 🔧 测试框架核心
│   ├── config.py              # 多环境配置管理（dev/staging/prod）
│   ├── client.py              # HTTP 客户端封装（统一请求/响应/日志）
│   └── logger.py              # 日志系统（全链路追踪）
│
├── tests/                      # ✅ 测试用例
│   └── test_notes.py          # 6 个测试类，12 条测试用例
│
├── data/                       # 📊 测试数据
│   └── test_data.json         # 参数化数据（正常/异常场景）
│
├── .github/workflows/          # 🤖 CI/CD 配置
│   └── test.yml               # GitHub Actions 工作流
│
├── conftest.py                 # pytest 全局夹具（fixtures）
├── pytest.ini                  # pytest 配置
├── requirements.txt            # 依赖清单
└── README.md                   # 📖 项目文档
```

---

## 🔍 测试覆盖范围

### 被测 API 接口（app/main.py）

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/notes` | 创建笔记 |
| GET | `/notes` | 获取笔记列表 |
| GET | `/notes/{id}` | 获取单条笔记 |
| PUT | `/notes/{id}` | 更新笔记 |
| DELETE | `/notes/{id}` | 删除笔记 |

### 测试用例清单（共 12 条）

| 测试类 | 测试方法 | 验证点 |
|--------|---------|--------|
| **TestHealth** | test_health_check | ✅ 健康检查返回 200 |
| **TestCreateNote** | test_create_note_success × 2 | ✅ 创建笔记返回 201，内容正确 |
| | test_create_note_invalid × 2 | ✅ 非法数据返回 422 |
| **TestListNotes** | test_list_notes | ✅ 列表返回 200，类型为 list |
| **TestGetNote** | test_get_note_success | ✅ 获取存在笔记返回 200 |
| | test_get_note_not_found | ✅ 不存在笔记返回 404 |
| **TestUpdateNote** | test_update_note_success | ✅ 更新成功返回新内容 |
| | test_update_note_not_found | ✅ 更新不存在笔记返回 404 |
| **TestDeleteNote** | test_delete_note_success | ✅ 删除成功返回 204，再查为 404 |
| | test_delete_note_not_found | ✅ 删除不存在笔记返回 404 |

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- pip

### 1. 克隆项目

```bash
git clone https://github.com/wanzhiwei5/api-test-framework.git
cd api-test-framework
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动被测系统

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. 运行测试

新开一个终端，执行：

```bash
pytest -v
```

所有测试通过后，你会看到：

```
collected 12 items
tests/test_notes.py::TestHealth::test_health_check PASSED
tests/test_notes.py::TestCreateNote::test_create_note_success[note_data0] PASSED
...
================== 12 passed in 2.14s ===================
```

### 生成 HTML 报告

```bash
pytest -v --html=reports/report.html --self-contained-html
```

然后打开 `reports/report.html` 查看可视化报告。

---

## 🤖 CI/CD — GitHub Actions

项目配置了 **GitHub Actions** 自动测试，每次 `push` 或 `pull_request` 到 `main` 分支时自动运行。

![CI Status](https://github.com/wanzhiwei5/api-test-framework/actions/workflows/test.yml/badge.svg)

### 工作流流程

```
代码推送 → GitHub 触发 Action
              ↓
        启动 Ubuntu 虚拟机
              ↓
        安装 Python 3.11
              ↓
        pip install 依赖
              ↓
        启动笔记 API 服务
              ↓
        运行 12 条测试用例
              ↓
        生成并归档 HTML 报告
              ↓
        ✅ 全部通过 / ❌ 失败通知
```

你可以在 [Actions 页面](https://github.com/wanzhiwei5/api-test-framework/actions) 查看每次运行结果。

---

## 📁 核心代码解读

### 配置管理（core/config.py）

```python
class TestConfig(BaseSettings):
    base_url: str = "http://localhost:8000"   # API 地址
    timeout: int = 10                           # 超时时间
```

**为什么这样做？** 将可变配置集中管理。环境切换（本地 → 测试服务器）只需修改一处。

### HTTP 客户端（core/client.py）

```python
class APIClient:
    def get(self, path): ...
    def post(self, path, json): ...
    def put(self, path, json): ...
    def delete(self, path): ...
```

**为什么这样做？** 统一封装请求/响应/日志，测试代码只需关注业务逻辑。

### 数据驱动测试（tests/test_notes.py）

```python
@pytest.mark.parametrize("note_data", test_data["valid_notes"])
def test_create_note_success(self, client, note_data):
    ...
```

**为什么这样做？** 测试数据与代码分离，新增测试数据只需编辑 JSON 文件。

---

## 📈 简历怎么写

> **项目：API 接口自动化测试框架**
>
> 基于 **Python + pytest + requests** 搭建完整的接口自动化测试体系。
>
> - **框架设计**：封装配置管理、HTTP 客户端、日志系统三层架构
> - **测试覆盖**：6 个 CRUD 接口，12 条测试用例，含正常及异常场景
> - **数据驱动**：JSON 参数化，测试数据与代码分离，易维护
> - **CI/CD**：GitHub Actions 自动运行测试，每次提交自动验证
>
> 🔗 https://github.com/wanzhiwei5/api-test-framework

---

## 📝 后续扩展方向

- [ ] 集成 Allure 报告（更专业的可视化测试报告）
- [ ] 添加性能测试（locust 压测）
- [ ] 部署被测系统到云端（Render / Fly.io）
- [ ] 添加 Mock 测试（模拟第三方接口）
- [ ] 集成钉钉/企业微信通知（测试失败自动告警）

---

## 📄 许可证

MIT License
