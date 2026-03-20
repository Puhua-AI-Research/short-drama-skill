# 微短剧剧本创作 Skill

**Short Drama Screenplay Skill** — 面向 Cursor、Codex、Claude Code 等 AI 助手的微短剧编剧技能包：从选题到分集完稿、自检、合规与出海输出；**可选**接入普华 ph8 的 **生图 / 生视频** CLI。

---

## 目录

- [功能概览](#功能概览)
- [仓库结构](#仓库结构)
- [安装与配置](#安装与配置)
- [快速上手](#快速上手)
- [命令手册](#命令手册)
- [工作目录结构](#工作目录结构)
- [参考知识库](#参考知识库)
- [质量评分体系](#质量评分体系)
- [示例输出](#示例输出)
- [技术细节](#技术细节)
- [Agent 生图 / 生视频脚本](#agent-生图--生视频脚本)
- [普华 API 说明文档](#普华-api-说明文档)
- [致谢](#致谢)
- [许可协议](#许可协议)

---

## 功能概览

| 能力 | 说明 |
|------|------|
| 13 种题材模板 | 定义见 [`skills/references/genre-guide.md`](skills/references/genre-guide.md)（都市情感、霸总、甜宠、重生穿越、战神、古装宫廷、励志逆袭、家庭伦理、萌宝、悬疑、软科幻、末日重生、喜剧等），**支持题材叠加**（建议不超过 3 种，见题材指南） |
| 四层反派体系 | 小反派 → 中反派 → 大反派 → 隐藏反派 |
| 五种钩子类型 | 悬念 / 反转 / 情绪 / 信息 / 危机（见 `hook-design.md`） |
| 节奏与关键集 | 节奏曲线、单集微结构；关键集约占 15–25% 集数 |
| 爽点矩阵 | 按 `satisfaction-matrix.md` 规划爽点分布 |
| 双语与出海 | 国内剧本格式（△ 镜头、♪ 配乐）与英文好莱坞格式（INT./EXT.、SHOT）；`/出海` 文化适配 |
| 合规 | `compliance-checklist.md` 红线与高风险扫描 |
| **视频制作流程** | **完整的场次分镜 + 首尾帧衔接 + 运镜设计**，生成 1-3 分钟连贯短剧视频 |
| 可选 · 媒体生成 | `scripts/ph8_*.py`：角色图、分镜首尾帧、文生/图生短视频（需 `PH8_API_KEY`） |

---

## 仓库结构

```
short-drama-skill/
├── skills/
│   ├── short-drama-skill/
│   │   ├── SKILL.md              # 技能入口（命令与工作流）
│   │   ├── VIDEO-WORKFLOW-EXAMPLE.md  # 视频制作完整示例
│   │   ├── references/           # 方法论知识库（7 个 Markdown）
│   │   └── scripts/              # Agent 可执行的 ph8 CLI
│   │       ├── ph8_common.py
│   │       ├── ph8_generate_image.py
│   │       ├── ph8_generate_video.py
│   │       └── requirements.txt
├── .env.example              # 密钥与环境变量示例
├── README.md
└── LICENSE
```

---

## 安装与配置

### 1. 安装技能（Markdown 技能）

将本仓库克隆到本地，确保助手能读取 **`skills/SKILL.md`** 与 **`skills/references/`**。

**Cursor 中使用：**

```bash
cd your-project
git clone https://github.com/<你的账号>/short-drama-skill.git
# 在对话中引用 @skills/short-drama-skill/SKILL.md
```

或直接打开本仓库作为工作目录。

**验证：** 对助手发送 **`/开始`**，应出现选题与题材引导。

### 2. 可选：普华 ph8 生图 / 生视频

用于 **角色定装图、分镜首尾帧、短片预览**（详见 [`skills/short-drama-skill/SKILL.md`](skills/short-drama-skill/SKILL.md) 中「Agent 工具：图像生成 / 视频生成」）。

```bash
cd short-drama-skill   # 或你的项目根目录（与 .env 同级）
pip install -r skills/short-drama-skill/scripts/requirements.txt
cp .env.example .env   # 编辑并填写 PH8_API_KEY
```

- 脚本会 **自动读取项目根目录的 `.env`**（不覆盖已有环境变量）。
- **未配置密钥** 时，脚本在 stderr 打印配置说明并以非零退出；**Agent 须转告用户**，勿伪造已生成文件。
- **`--json-meta`**：成功时在 stdout 输出一行 JSON，便于解析路径。
- 视频任务较慢，建议 **`--no-progress`** 并由助手提示用户等待。

---

## 快速上手

典型编剧流程（与 `skills/SKILL.md` 一致）：

```
/开始          → 题材、受众、基调、结局、集数（50–100）、语言 / 出海
/创作方案      → 故事骨架、三幕、节奏、付费点、爽点矩阵 → creative-plan.md
/角色开发      → 角色档案、关系图、反派体系 → characters.md
                 ↓（可选）生成角色设定图 → assets/characters/
/目录          → 分集目录 🔥💰 标记 → episode-directory.md
/分集 1        → episodes/ep001.md（包含场次、首尾帧、运镜标记）
/自检 1        → 五维评分与修改建议（对话中输出报告）
/制作视频 1    → 为第1集生成完整视频（场次分镜 + 首尾帧衔接）
                 ├── ep001/frames/    （场次首尾帧）
                 ├── ep001/videos/    （场次视频）
                 └── ep001_complete.mp4（完整单集 80-120秒）
/合规          → compliance-report.md（国内向）
/导出          → export/{剧名}-完整剧本.md
```

**海外：** `/出海` 或 `/开始` 选择 English → 按 `INT./EXT.` 等格式写 `/分集`。

**视频制作流程：**
1. **角色图公共**：`assets/characters/` 存放全剧共用的角色设定图
2. **单集独立**：每集一个目录（`ep001/`, `ep002/` ...）
3. **场次完整**：每个场次包含首帧、尾帧、视频三个文件
4. **首尾帧衔接**：下一场次的首帧承接上一场次的尾帧，保证视觉连贯性
5. **运镜设计**：每个场次标注运镜方式（推镜/拉镜/摇镜/移镜等）
6. **合并成集**：所有场次视频合并为 1-3 分钟的完整单集

---

## 命令手册

以下为与 **`skills/SKILL.md`** 对齐的摘要；完整步骤、输出模板与引用资料以 skill 文件为准。

### 命令快速参考

| 命令 | 功能 | 输出 |
|------|------|------|
| `/开始` | 选题立项 | `.drama-state.json` |
| `/创作方案` | 故事骨架 | `creative-plan.md` |
| `/角色开发` | 角色档案 | `characters.md` |
| `/目录` | 分集目录 | `episode-directory.md` |
| `/分集 {N}` | 编写剧本 | `episodes/ep{NNN}.md` |
| `/自检 {N}` | 质量检查 | 对话中输出报告 |
| `/制作视频 {N}` | 生成视频 | `ep{NNN}/` 目录 |
| `/优化场次 {N} {X}` | 优化单个场次 | 更新对应场次文件 |
| `/合规` | 合规检查 | `compliance-report.md` |
| `/出海` | 文化适配 | 切换英文格式 |
| `/导出` | 导出剧本 | `export/{剧名}-完整剧本.md` |

### `/开始` — 选题立项

| 配置项 | 说明 |
|--------|------|
| 题材 | 13 类（见 genre-guide），可叠加 |
| 受众 | 男频 / 女频 / 全年龄 |
| 基调 | 爽燃 / 甜虐 / 搞笑 / 暗黑 / 温情 |
| 结局 | 大团圆 / 开放式 / 反转式 / 悲剧 |
| 集数 | 由用户指定（建议 30-100 集） |
| 语言 | 中文 或 English（English 视同出海模式） |

状态写入 **`.drama-state.json`**。

### `/创作方案`

输出 **`creative-plan.md`**：剧名备选、背景、故事线、**三幕结构**、节奏波形描述、**付费卡点**、**爽点矩阵**、结局与伏笔等。  
参考：`opening-rules.md`、`paywall-design.md`、`rhythm-curve.md`、`satisfaction-matrix.md`。

### `/角色开发`

输出 **`characters.md`**：档案、Mermaid 关系图、弧线、感情线、反派四层体系等。  
参考：`villain-design.md`。

### `/目录`

输出 **`episode-directory.md`**：每集一行，**🔥** 关键集（重大转折、高潮、重要剧情节点）；前 10 集节奏与占比要求见 skill。

### `/分集 {N}`

输出 **`episodes/ep{NNN}.md`**；支持 `/分集 3-5`、`/分集 next`。  
参考：第 1 集侧重 `opening-rules.md`，并配合 `rhythm-curve.md`、`satisfaction-matrix.md`、`hook-design.md`。

**新增剧本格式要求：**
- 每个场次标注时长（如 `## 场次一 {15秒}`）
- 每个场次包含运镜、情绪、光线标记
- 每个场次必须有 `【首帧】` 和 `【尾帧】` 描述
- 场次二及以后需要 `**衔接**` 说明

### `/制作视频 {N}`

为第 N 集生成完整视频内容。支持 `/制作视频 1` 或 `/制作视频 1-3`。

**工作流程：**
1. 读取剧本，解析场次结构
2. 为每个场次生成首尾帧图片（使用角色参考图）
3. 使用首尾帧控制生成每个场次视频（15-25秒）
4. 生成 ffmpeg 合并列表
5. 合并为完整单集（80-120秒）

**输出结构：**
```
ep001/
├── frames/          # 场次首尾帧
│   ├── scene1_start.png
│   ├── scene1_end.png
│   └── ...
├── videos/          # 场次视频
│   ├── scene1.mp4
│   └── ...
├── ep001_scenes.txt
└── ep001_complete.mp4
```

### `/优化场次 {集数} {场次号}`

重新生成指定集数的指定场次。支持：
- `/优化场次 1 2` — 重新生成第1集第2场次的所有内容
- `/优化场次 1 2 --frames-only` — 仅重新生成首尾帧
- `/优化场次 1 2 --video-only` — 仅重新生成视频

**使用场景：**
- 某个场次的首帧或尾帧不满意
- 某个场次的视频效果不理想
- 修改了剧本中某个场次的内容
- 调整运镜方式、情绪氛围或光线效果

**提示词优化建议：**
1. **首帧/尾帧不满意：** 增加构图、光线、色调的具体描述
2. **视频动作不连贯：** 确保首尾帧有明确的动作差异
3. **运镜效果不明显：** 使用更具体的运镜术语

### `/自检 {N}`

对单集、区间或 `all` 做 **节奏 / 爽点 / 台词 / 格式 / 连贯性** 五项 1–10 分（总分 50）。  
**报告默认在对话中给出**（Markdown 模板见 skill）；如需存档可自行写入 `reviews/`（本仓库 `.gitignore` 默认忽略该目录）。

### `/合规`

输出 **`compliance-report.md`**（国内模式）。参考：`compliance-checklist.md`。

### `/出海`

切换英文与好莱坞式场景头、镜头描述与文化映射（见 genre-guide 出海部分）。

### `/导出`

合并为 **`export/{剧名}-完整剧本.md`**。

---

## 工作目录结构

在项目根目录（跑 `/开始` 的目录）下，典型产物如下：

```
your-project/
├── .drama-state.json
├── creative-plan.md
├── characters.md
├── episode-directory.md
├── episodes/                   # 剧本目录
│   ├── ep001.md
│   ├── ep002.md
│   └── ...
├── assets/                     # 角色图公共目录（全剧共用）
│   └── characters/
│       ├── {角色名}.png
│       ├── {角色名}.json
│       └── ...
├── ep001/                      # 第1集独立目录
│   ├── frames/                 # 该集所有场次的首尾帧
│   │   ├── scene1_start.png
│   │   ├── scene1_end.png
│   │   ├── scene2_start.png
│   │   └── ...
│   ├── videos/                 # 该集所有场次视频
│   │   ├── scene1.mp4
│   │   ├── scene2.mp4
│   │   └── ...
│   ├── ep001_scenes.txt        # ffmpeg合并列表
│   └── ep001_complete.mp4      # 完整单集（80-120秒）
├── ep002/                      # 第2集独立目录
│   └── ...
├── reviews/                    # 可选：自检报告存档
├── compliance-report.md
├── export/
│   └── {剧名}-完整剧本.md
└── scripts/                    # 若随仓库携带
    └── ...
```

**目录组织原则：**
- **角色图公共**：`assets/characters/` 存放所有角色设定图，全剧共用
- **单集独立**：每集一个独立目录（`ep001/`, `ep002/` ...）
- **场次完整**：每个场次包含首帧、尾帧、视频三个文件
- **元数据保留**：使用 `--json-meta` 生成的 `.json` 文件保留，便于追溯和调试

---

## 参考知识库

所有文件位于 **`skills/references/`**（篇幅为大致规模，以实际文件为准）：

| 文件 | 内容要点 |
|------|----------|
| `genre-guide.md` | 13 类题材、叠加规则、出海映射 |
| `opening-rules.md` | 开篇黄金法则、6 种开场模板 |
| `rhythm-curve.md` | 节奏曲线、单集结构 |
| `hook-design.md` | 钩子类型与设计 |
| `satisfaction-matrix.md` | 爽点类型与配比 |
| `villain-design.md` | 四层反派 |
| `compliance-checklist.md` | 合规清单 |

**按命令加载（与 `skills/SKILL.md` 一致）：**

| 命令 | 参考文档 |
|------|----------|
| `/开始` | genre-guide.md |
| `/创作方案` | opening-rules.md, rhythm-curve.md, satisfaction-matrix.md |
| `/角色开发` | villain-design.md |
| `/目录` | rhythm-curve.md |
| `/分集 {N}` | opening-rules.md（第 1 集重点）, rhythm-curve.md, satisfaction-matrix.md, hook-design.md |
| `/合规` | compliance-checklist.md |

---

## 质量评分体系

`/自检` 五维度各 **1–10 分**，总分 **50**。

| 总分 | 说明（与 skill 一致） |
|------|------------------------|
| 45–50 | 优秀，可直接导出 |
| 35–44 | 良好，建议微调 |
| 25–34 | 及格，修改后建议再自检 |
| 25 以下 | 不合格，建议重写 |

---

## 示例输出

### 分集剧本片段（国内格式 - 新版带视频制作标记）

```markdown
## 场次一 {15秒}

**场景：** 内景 · 念念甜品屋 · 日
**出场人物：** 苏念
**运镜：** 全景推进到中景
**情绪：** 温馨、慵懒
**光线：** 暖黄色灯光

【首帧】甜品店全景，暖黄色灯光，墙上贴满便利贴，玻璃柜台里摆着精致甜品。温馨的社区小店氛围，9:16竖屏。

△ （全景）一间不大但布置温馨的社区甜品店，暖黄色灯光，
墙上贴满顾客留言的便利贴，玻璃柜台里摆着各色精致甜品。

△ （中景 - 推镜）**苏念**（26岁，马尾，围裙上沾着面粉）正弯腰
把一盘刚出炉的柠檬挞摆进柜台，动作轻柔。

**苏念**：（自言自语，满意地看着柠檬挞）
今天这批酸度刚好，老陈头肯定又要买三个。

【尾帧】苏念站在柜台后，满意地看着柠檬挞，脸上带着温柔的笑容。中景构图，9:16竖屏。

♪ 音乐提示：轻快的钢琴配乐，带一点法式小调的慵懒
```

### 自检评分示例

| 维度 | 得分 | 说明 |
|------|------|------|
| 节奏 | 8/10 | 四场戏节奏分配合理 |
| 爽点 | 7/10 | 铺垫集定位准确 |
| 台词 | 9/10 | 台词贴合人物性格 |
| 格式 | 9/10 | 镜头语言规范完整 |
| 连贯性 | 9/10 | 与角色档案高度一致 |

**总分：42/50**（良好，建议微调）

---

## 技术细节

- **技能本体**：纯 Markdown + 按需加载 references，**无运行时依赖**。
- **媒体 CLI**：仅 `scripts/requirements.txt` 中的 `openai` SDK，用于调用 ph8 兼容接口。
- **兼容**：任何能挂载 `skills/SKILL.md` 的 AI 编程助手均可使用本工作流。

---

## Agent 生图 / 生视频脚本

| 文件 | 作用 |
|------|------|
| `scripts/ph8_generate_image.py` | `images.generations`，文生图、`reference_images`（`--ref-uri` / `--ref-file`） |
| `scripts/ph8_generate_video.py` | `videos.create`，轮询，`download_content`；`--mode simple\|advanced`（首帧 / 尾帧 / 参考图） |
| `scripts/ph8_common.py` | 加载根目录 `.env`；缺失密钥时的 stderr 指引 |
| `scripts/requirements.txt` | `openai>=1.40.0` |
| `.env.example` | `PH8_API_KEY`、`OPENAI_BASE_URL`、`PH8_IMAGE_MODEL`、`PH8_VIDEO_MODEL` |

**常用参数摘抄：**

- 图像：`--prompt`、`--out`、`--model`、`--size`、`--ref-uri`、`--ref-file`、`--json-meta`
- 视频：`--prompt`、`--out`、`--ratio`（如 `9:16`）、`--duration`、`--image-url` / `--image-file`、`--first-frame-url`、`--last-frame-url`、`--json-meta`、`--no-progress`

详细命令模板、与编剧流程的结合方式、**无密钥时的 Agent 义务**，见 **`skills/SKILL.md`** 中的「Agent 工具：图像生成」「Agent 工具：视频生成」。

---

## 普华 API 说明文档

仓库根目录 **[`ph8.md`](ph8.md)** 提供普华开放平台的接口说明（OpenAI 兼容 Base URL、文本 / 图像 / 视频示例等），与 `scripts/ph8_*.py` 互补：脚本面向 **自动化调用**，`ph8.md` 面向 **人工查阅与扩展参数**。

---

## 致谢

本技能的创作方法论与行业知识参考短剧编剧实践及内容合规相关要求。

感谢 [binghe](https://x.com/binghe) 在 AI 辅助编剧方向的探索与分享。

---

## 许可协议

本项目采用 [MIT License](LICENSE) 开源协议。使用、修改与分发时请保留许可声明。
