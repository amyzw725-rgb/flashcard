# 日语单词 Flashcard

面向 **JLPT N4 / N3** 学习者的日语单词闪卡工具。输入一个生活场景主题（如「去迪士尼乐园」「餐厅点餐」），即可生成带例句、罗马音与中文释义的单词卡，支持翻转复习与本地存档。

## 功能

- **主题生成**：根据中文或日文主题关键词，从内置词库中抽取 3–6 张相关单词卡
- **闪卡交互**：正面显示单词、罗马音与例句（关键词高亮）；背面显示中文释义与例句翻译；支持点击翻转
- **导航**：上一张 / 下一张、卡片序号显示
- **存档**：将当前卡组保存到浏览器 `localStorage`，支持从存档库加载复习
- **可选后端**：Flask API 提供按主题生成单词、按类别查询等接口（与前端目前为独立运行）

## 项目结构

```
日语卡片/
├── Flashcard.py.py          # 前端单页应用（HTML + CSS + JavaScript）
├── api.py.py                # Flask 后端 API（可选）
├── deepseek_html_20260517_6b9099.html   # 早期 HTML 版本（参考）
└── README.md
```

> **说明**：`Flashcard.py.py` 与 `api.py.py` 文件名带有重复的 `.py` 后缀，实际分别为 HTML 页面与 Python 脚本。若需规范命名，可改为 `Flashcard.html` 与 `api.py`。

## 快速开始

### 方式一：仅使用前端（推荐入门）

1. 用浏览器直接打开 `Flashcard.py.py`（或重命名后的 `Flashcard.html`）
2. 在输入框中填写主题，点击 **生成**
3. 使用 **翻转卡片**、**上一个** / **下一个** 学习
4. 满意后点击 **存档当前**，日后在右侧 **存档库** 中点击条目复习

前端内置示例主题词库（迪士尼、餐厅、购物等），无需联网即可演示；页脚注明完整智能生成可对接 DeepSeek API。

### 方式二：启动 Flask API

```bash
cd "C:\Users\amyzh\Desktop\日语卡片"
pip install flask flask-cors
python api.py.py
```

服务默认运行在 `http://0.0.0.0:5000`。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | API 说明与端点列表 |
| POST | `/api/generate` | 按主题生成单词卡，Body: `{"topic": "旅行", "count": 5}` |
| GET | `/api/topics` | 获取可用词库类别 |
| GET | `/api/words/<category>` | 获取指定类别单词，可选 `?count=3` |
| GET | `/api/health` | 健康检查 |

词库类别包括：`travel`、`food`、`shopping`、`business`、`daily_life` 等。`call_deepseek_api` 目前为**本地词库模拟**，按主题关键词匹配类别后随机抽词，并非真实调用 DeepSeek。

## 单词卡字段

每张卡片包含：

| 字段 | 说明 |
|------|------|
| `word` | 日语单词 |
| `romaji` | 罗马音 |
| `example` | 例句（HTML，含 `<span class="highlight">` 高亮） |
| `meaning` | 中文释义 |
| `translation` | 例句中文翻译 |
| `level` | （API 词库）N4 / N3 标注 |

## 技术栈

- **前端**：原生 HTML / CSS / JavaScript，`localStorage` 持久化存档，Font Awesome 图标 CDN
- **后端**：Python 3 + Flask + flask-cors

## 后续扩展

- [ ] 将前端 `generateFlashcards` 改为请求 `/api/generate`，统一词库与逻辑
- [ ] 接入 DeepSeek（或其他 LLM）API，按主题动态生成单词与例句
- [ ] 规范文件名：`Flashcard.html`、`api.py`
- [ ] 增加 `requirements.txt` 与静态资源目录（如 `favicon.ico`）

## 许可

个人学习项目。词库与界面仅供练习使用，商用或分发前请自行核对内容与版权。
