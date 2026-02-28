# 智能简历筛选系统（AI Resume Screener）

一个可落地的智能简历筛选原型，支持：

- **0-100 匹配度评分**（关键词、技能相似度、经验匹配）
- **客户偏好学习**（根据 accept/reject 反馈更新权重）
- **PDF / 图片简历解析能力封装**（通过 `pdftotext` / `tesseract` 命令）
- **“点开简历即分析”接入接口设计**（可对接 Boss / 猎聘插件或桌面代理）

## 核心能力

### 1) 智能评分（0-100）
评分公式由三部分组成，并可按招聘者偏好动态调整：

- `keyword_coverage`：岗位关键词覆盖率
- `skill_similarity`：岗位与简历词向量余弦相似度（基于词频）
- `experience_match`：年限匹配度（如岗位要求 3 年、候选人 5 年）

### 2) 偏好学习
每次招聘者反馈：

- `accept`：强化当前特征权重
- `reject`：削弱当前特征权重

模型按 `recruiter_id` 独立存储（`data/preferences.json`）。

### 3) 简历解析
- PDF：调用 `pdftotext`
- 图片：调用 `tesseract -l chi_sim+eng`

> 如果运行环境未安装这些命令，会抛出可解释错误，便于工程化降级。

## 与 Boss / 猎聘联动方案（建议）

后端能力已经具备，前端可通过浏览器插件实现：

1. 监听简历详情弹层出现
2. 提取简历文本（DOM 或截图 OCR）
3. 调用本系统分析函数/接口
4. 将评分浮层展示在页面

## 快速运行

```bash
python -m pytest -q
python -m app.main
```

## 项目结构

```text
app/
  analyzer.py      # 匹配评分逻辑
  preference.py    # 偏好学习逻辑
  parser.py        # PDF/图片文本解析
  main.py          # 服务入口函数（示例调用）
  storage.py       # 偏好持久化
tests/
  test_analyzer.py
  test_api.py
```
