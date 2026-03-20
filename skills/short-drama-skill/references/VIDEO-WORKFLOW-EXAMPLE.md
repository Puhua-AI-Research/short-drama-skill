# 短剧视频制作完整工作流示例

本文档展示如何使用更新后的短剧技能，从剧本到完整视频的全流程。

## 核心改进

### 1. 文件组织结构

```
项目目录/
├── assets/
│   └── characters/          # 角色图公共目录（全剧共用）
│       ├── sunwukong.png
│       ├── jade_emperor.png
│       └── ...
├── episodes/                # 剧本目录
│   ├── ep001.md
│   ├── ep002.md
│   └── ...
├── ep001/                   # 第1集独立目录
│   ├── frames/              # 该集所有场次的首尾帧
│   │   ├── scene1_start.png
│   │   ├── scene1_end.png
│   │   ├── scene2_start.png
│   │   ├── scene2_end.png
│   │   └── ...
│   ├── videos/              # 该集所有场次视频
│   │   ├── scene1.mp4
│   │   ├── scene2.mp4
│   │   └── ...
│   ├── ep001_scenes.txt     # 合并列表
│   └── ep001_complete.mp4   # 完整单集
├── ep002/                   # 第2集独立目录
│   └── ...
└── ...
```

### 2. 剧本格式改进

每个场次必须包含：

- **时长标记**：`## 场次一 {15秒}`
- **运镜方案**：`**运镜：** 全景推进到中景`
- **情绪氛围**：`**情绪：** 震撼、神秘`
- **光线效果**：`**光线：** 逆光，金色光芒`
- **首帧描述**：`【首帧】{静态画面完整描述}`
- **尾帧描述**：`【尾帧】{动作完成后的画面}`
- **衔接说明**（场次二及以后）：`**衔接：** {与上一场次的关系}`

### 3. 视频生成流程

每集视频 = 多个场次片段 + 首尾帧衔接

```
场次1（15秒）→ 场次2（18秒）→ 场次3（20秒）→ 场次4（15秒）→ 场次5（12秒）
    ↓              ↓              ↓              ↓              ↓
尾帧衔接首帧   尾帧衔接首帧   尾帧衔接首帧   尾帧衔接首帧
                                                                ↓
                                                        完整单集（80秒）
```

## 完整示例：第1集《灵石诞生》

### 步骤1：编写剧本（使用新格式）

```markdown
# 第1集：灵石诞生

> 本集关键词：诞生、天命、初遇
> 本集爽点：身份爽（天生神力）
> 预计时长：80秒（5个场次）

---

## 场次一 {15秒}

**场景：** 外景 · 花果山山巅 · 日
**出场人物：** 石猴（孙悟空）
**运镜：** 全景推进到中景
**情绪：** 震撼、神秘
**光线：** 逆光，金色光芒

【首帧】花果山山巅全景，巨大的五彩灵石矗立在悬崖边，裂纹密布，金光从裂缝中透出。天空乌云密布，阳光从云层缝隙射下。电影级构图，9:16竖屏。

△ （全景）花果山山巅，风云变色，雷声滚滚。

△ （中景 - 推镜）五彩灵石突然炸裂，金光冲天，一个身影从中跃出。

△ （中景）石猴落地，金色瞳孔，面如桃李，身穿虎皮裙，充满灵性。

【尾帧】石猴站立在炸裂的灵石碎片中，双手握拳，仰望天空，金色光芒环绕全身。中景构图，英雄降临姿态，9:16竖屏。

♪ 音乐提示：史诗级配乐，震撼鼓点，神秘东方旋律

---

## 场次二 {18秒}

**场景：** 外景 · 花果山密林 · 日
**出场人物：** 石猴、众猴
**运镜：** 固定镜头 + 跟随移镜
**情绪：** 好奇、活泼
**光线：** 自然光，斑驳树影
**衔接：** 石猴从山巅走下，进入密林，光线从逆光转为自然光

【首帧】石猴走进密林，阳光透过树叶洒下斑驳光影。前景是石猴背影，中景是嬉戏的众猴。全景构图，9:16竖屏。

△ （全景）石猴走进密林，众猴停止嬉戏，好奇地望着他。

△ （中景 - 移镜）石猴走近，众猴围拢过来，叽叽喳喳。

**老猴**（惊讶）："你...你是从灵石里出来的？"

**石猴**（好奇地看着自己的手）："我...我是谁？"

△ （特写）石猴的金色瞳孔，充满困惑。

【尾帧】众猴围绕石猴，老猴伸手指向远处。中景构图，众猴在前景，石猴在中心，9:16竖屏。

♪ 音乐提示：轻快的民族乐器，好奇感

---

## 场次三 {20秒}

**场景：** 外景 · 水帘洞前 · 日
**出场人物：** 石猴、众猴
**运镜：** 全景拉远 + 推镜
**情绪：** 惊险、勇敢
**光线：** 明亮，水雾折射光线
**衔接：** 众猴带领石猴来到瀑布前，场景从密林转到开阔的水帘洞

【首帧】巨大的瀑布从山崖倾泻而下，水雾弥漫。众猴站在瀑布前，石猴在中心。全景构图，9:16竖屏。

△ （全景）瀑布轰鸣，水雾弥漫，众猴望而却步。

**老猴**（指着瀑布）："谁能穿过瀑布，找到洞府，就是我们的大王！"

△ （中景 - 推镜）石猴眼神一亮，纵身跃起。

△ （特写）石猴穿过瀑布的瞬间，水珠在阳光下闪烁。

【尾帧】石猴消失在瀑布后，只留下水雾和惊讶的众猴。中景构图，瀑布占据画面中心，9:16竖屏。

♪ 音乐提示：紧张的鼓点，冒险感

---

## 场次四 {15秒}

**场景：** 内景 · 水帘洞内 · 日
**出场人物：** 石猴
**运镜：** 推镜 + 环绕
**情绪：** 震撼、兴奋
**光线：** 从洞口透入的光线，洞内昏暗
**衔接：** 从瀑布外的明亮转到洞内的昏暗，光线对比强烈

【首帧】石猴站在洞口，背后是瀑布的光线，面前是昏暗的洞穴。逆光剪影，中景构图，9:16竖屏。

△ （中景 - 推镜）石猴走进洞内，四处张望。

△ （全景 - 环绕）洞内宽敞，石桌石椅俱全，仿佛天然宫殿。

**石猴**（兴奋）："好地方！真是好地方！"

△ （特写）石猴的眼睛闪烁着金光，充满喜悦。

【尾帧】石猴转身面向洞口，双手叉腰，英雄姿态。中景构图，背景是洞内景象，9:16竖屏。

♪ 音乐提示：宏大的配乐，发现新世界的感觉

---

## 场次五 {12秒}

**场景：** 外景 · 水帘洞前 · 日
**出场人物：** 石猴、众猴
**运镜：** 拉镜 + 升降
**情绪：** 欢庆、爽燃
**光线：** 明亮，阳光洒下
**衔接：** 石猴从洞内冲出，光线从昏暗转为明亮，情绪从兴奋转为欢庆

【首帧】石猴从瀑布中跃出，水珠飞溅，阳光照耀。中景构图，石猴在空中，9:16竖屏。

△ （中景）石猴落地，众猴欢呼。

**众猴**（齐声）："大王！大王！"

△ （全景 - 升降）镜头升起，俯瞰众猴跪拜石猴的场景。

△ （特写）石猴的脸，从困惑到自信的转变。

【尾帧】石猴站在高处，众猴跪拜，阳光从背后照射，形成英雄剪影。全景构图，9:16竖屏。

♪ 音乐提示：高昂的胜利配乐

---

> 🎣 本集钩子：石猴成为美猴王，但他的金色瞳孔突然闪烁，似乎预示着更大的命运...
> 📺 下集预告：美猴王开始统治花果山，但他渴望更强大的力量...
> 📊 场次统计：共5个场次，总时长80秒
```

### 步骤2：生成角色设定图（全剧共用）

```bash
# 创建角色目录
mkdir -p assets/characters

# 生成孙悟空设定图
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "孙悟空，年轻猴王形象，金色瞳孔，面如桃李，虎皮裙，充满灵性和野性。中国古典美学，电影级人物设定，9:16竖屏" \
  --out "assets/characters/sunwukong.png" \
  --json-meta
```

### 步骤3：为第1集生成所有场次的首尾帧

```bash
# 创建第1集目录
mkdir -p ep001/frames ep001/videos

# === 场次一：首尾帧 ===
# 首帧：灵石完整
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "花果山山巅全景，巨大的五彩灵石矗立在悬崖边，裂纹密布，金光从裂缝中透出。天空乌云密布，阳光从云层缝隙射下。电影级构图，9:16竖屏" \
  --out "ep001/frames/scene1_start.png" \
  --json-meta

# 尾帧：石猴跃出后
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴站立在炸裂的灵石碎片中，双手握拳，仰望天空，金色光芒环绕全身。中景构图，英雄降临姿态，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene1_end.png" \
  --json-meta

# === 场次二：首尾帧 ===
# 首帧：石猴进入密林
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴走进密林，阳光透过树叶洒下斑驳光影。前景是石猴背影，中景是嬉戏的众猴。全景构图，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene2_start.png" \
  --json-meta

# 尾帧：众猴围绕
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "众猴围绕石猴，老猴伸手指向远处。中景构图，众猴在前景，石猴在中心，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene2_end.png" \
  --json-meta

# === 场次三：首尾帧 ===
# 首帧：瀑布前
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "巨大的瀑布从山崖倾泻而下，水雾弥漫。众猴站在瀑布前，石猴在中心。全景构图，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene3_start.png" \
  --json-meta

# 尾帧：石猴消失在瀑布后
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴消失在瀑布后，只留下水雾和惊讶的众猴。中景构图，瀑布占据画面中心，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene3_end.png" \
  --json-meta

# === 场次四：首尾帧 ===
# 首帧：洞口逆光
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴站在洞口，背后是瀑布的光线，面前是昏暗的洞穴。逆光剪影，中景构图，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene4_start.png" \
  --json-meta

# 尾帧：转身面向洞口
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴转身面向洞口，双手叉腰，英雄姿态。中景构图，背景是洞内景象，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene4_end.png" \
  --json-meta

# === 场次五：首尾帧 ===
# 首帧：从瀑布跃出
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴从瀑布中跃出，水珠飞溅，阳光照耀。中景构图，石猴在空中，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene5_start.png" \
  --json-meta

# 尾帧：英雄剪影
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴站在高处，众猴跪拜，阳光从背后照射，形成英雄剪影。全景构图，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene5_end.png" \
  --json-meta
```

### 步骤4：为每个场次生成视频（使用首尾帧控制）

```bash
# === 场次一：灵石炸裂（15秒）===
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "五彩灵石炸裂，金光冲天，石猴从中跃出落地，仰望天空。运镜：全景推进到中景。情绪：震撼、神秘。光线：逆光，金色光芒" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene1_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene1_end.png" \
  --ratio "9:16" --duration 15 --seed 42 --resolution 1080p \
  --out "ep001/videos/scene1.mp4" \
  --json-meta --no-progress

# === 场次二：初遇众猴（18秒）===
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "石猴走进密林，众猴围拢，对话交流，老猴指向远处。运镜：固定镜头 + 跟随移镜。情绪：好奇、活泼。光线：自然光，斑驳树影" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene2_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene2_end.png" \
  --ratio "9:16" --duration 18 --seed 43 --resolution 1080p \
  --out "ep001/videos/scene2.mp4" \
  --json-meta --no-progress

# === 场次三：水帘洞挑战（20秒）===
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "众猴站在瀑布前，石猴纵身跃起，穿过瀑布消失。运镜：全景拉远 + 推镜。情绪：惊险、勇敢。光线：明亮，水雾折射光线" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene3_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene3_end.png" \
  --ratio "9:16" --duration 20 --seed 44 --resolution 1080p \
  --out "ep001/videos/scene3.mp4" \
  --json-meta --no-progress

# === 场次四：发现洞府（15秒）===
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "石猴走进洞内，四处张望，发现宽敞的天然宫殿，转身面向洞口。运镜：推镜 + 环绕。情绪：震撼、兴奋。光线：从洞口透入的光线，洞内昏暗" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene4_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene4_end.png" \
  --ratio "9:16" --duration 15 --seed 45 --resolution 1080p \
  --out "ep001/videos/scene4.mp4" \
  --json-meta --no-progress

# === 场次五：加冕为王（12秒）===
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "石猴从瀑布跃出，众猴欢呼跪拜，镜头升起俯瞰全景，形成英雄剪影。运镜：拉镜 + 升降。情绪：欢庆、爽燃。光线：明亮，阳光洒下" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene5_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene5_end.png" \
  --ratio "9:16" --duration 12 --seed 46 --resolution 1080p \
  --out "ep001/videos/scene5.mp4" \
  --json-meta --no-progress
```

### 步骤5：合并场次为完整单集

```bash
# 创建合并列表
cat > ep001/ep001_scenes.txt << EOF
file 'videos/scene1.mp4'
file 'videos/scene2.mp4'
file 'videos/scene3.mp4'
file 'videos/scene4.mp4'
file 'videos/scene5.mp4'
EOF

# 合并视频
cd ep001
ffmpeg -f concat -safe 0 -i ep001_scenes.txt -c copy ep001_complete.mp4

# 检查完整单集
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ep001_complete.mp4
# 预期输出：80.0（秒）
```

### 步骤6：验证输出

```bash
# 检查文件结构
tree ep001/

# 预期输出：
# ep001/
# ├── frames/
# │   ├── scene1_start.png
# │   ├── scene1_start.json
# │   ├── scene1_end.png
# │   ├── scene1_end.json
# │   ├── scene2_start.png
# │   ├── scene2_end.png
# │   ├── scene3_start.png
# │   ├── scene3_end.png
# │   ├── scene4_start.png
# │   ├── scene4_end.png
# │   ├── scene5_start.png
# │   └── scene5_end.png
# ├── videos/
# │   ├── scene1.mp4
# │   ├── scene1.json
# │   ├── scene2.mp4
# │   ├── scene2.json
# │   ├── scene3.mp4
# │   ├── scene3.json
# │   ├── scene4.mp4
# │   ├── scene4.json
# │   ├── scene5.mp4
# │   └── scene5.json
# ├── ep001_scenes.txt
# └── ep001_complete.mp4

# 检查文件大小
ls -lh ep001/videos/*.mp4
ls -lh ep001/ep001_complete.mp4
```

## 关键改进总结

### 1. 连贯性保证

- **首尾帧衔接**：每个场次的尾帧设计要考虑下一场次的首帧
- **运镜连贯**：相邻场次的运镜方式要有逻辑（推镜→固定→拉镜）
- **情绪曲线**：场次间的情绪要有起伏（震撼→好奇→惊险→兴奋→欢庆）
- **光线过渡**：光线变化要自然（逆光→自然光→明亮→昏暗→明亮）

### 2. 单集时长合理

- 每集 80-120 秒（1.3-2 分钟）
- 每个场次 10-25 秒
- 3-5 个场次组成一集
- 总时长适合短视频平台

### 3. 角色一致性

- 角色图存放在公共目录 `assets/characters/`
- 所有场次生成图片时都使用 `--ref-file` 引用角色图
- 确保同一角色在不同场次中外观一致

### 4. 文件组织清晰

- 每集独立目录（`ep001/`, `ep002/` ...）
- 场次资产集中管理（`frames/`, `videos/`）
- 元数据保留（`.json` 文件）便于追溯和调试

## 下一步

1. **继续制作第2集**：使用相同的流程
2. **添加后期制作**：字幕、音效、BGM
3. **批量生成**：使用 `/制作视频 1-10` 批量生成多集
4. **优化提示词**：根据生成效果调整提示词模板

## 场次优化示例

如果某个场次的效果不满意，可以使用 `/优化场次` 命令重新生成。

### 示例：优化第1集第2场次

假设第2场次的首帧光线不理想，需要重新生成：

```bash
# 仅重新生成首尾帧
python skills/short-drama-skill/scripts/ph8_generate_image.py \
  --prompt "石猴走进密林，阳光透过树叶洒下斑驳光影，光线更加明亮温暖。前景是石猴背影，中景是嬉戏的众猴。全景构图，9:16竖屏" \
  --ref-file "assets/characters/sunwukong.png" \
  --out "ep001/frames/scene2_start.png" \
  --json-meta

# 使用新的首帧重新生成视频
python skills/short-drama-skill/scripts/ph8_generate_video.py --mode advanced \
  --prompt "石猴走进密林，众猴围拢，对话交流，老猴指向远处。运镜：固定镜头 + 跟随移镜。情绪：好奇、活泼。光线：明亮自然光，斑驳树影" \
  --first-frame-url "file://$(pwd)/ep001/frames/scene2_start.png" \
  --last-frame-url "file://$(pwd)/ep001/frames/scene2_end.png" \
  --ratio "9:16" --duration 18 --seed 43 --resolution 1080p \
  --out "ep001/videos/scene2.mp4" \
  --json-meta --no-progress

# 重新合并完整单集
cd ep001
ffmpeg -f concat -safe 0 -i ep001_scenes.txt -c copy -y ep001_complete.mp4
```

## 常见问题

### Q: 如何确保场次间的连贯性？

A: 在编写剧本时，为每个场次（从场次二开始）添加 **衔接** 说明，描述与上一场次的视觉、情绪、空间关系。

### Q: 如果视频生成失败怎么办？

A: 尝试使用 `--mode simple` 和 `--image-file` 作为备选方案，或调整提示词使其更简洁。

### Q: 如何调整单集时长？

A: 修改剧本中每个场次的时长标记（如 `{15秒}` → `{20秒}`），视频生成时会自动使用该时长。

### Q: 角色图需要为每集单独生成吗？

A: 不需要。角色图存放在 `assets/characters/` 公共目录，全剧共用，只需生成一次。

### Q: 如何优化单个场次？

A: 使用 `/优化场次 {集数} {场次号}` 命令，可以选择仅重新生成首尾帧（`--frames-only`）或仅重新生成视频（`--video-only`）。
