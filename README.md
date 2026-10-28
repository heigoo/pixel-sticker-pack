# pixel-sticker-pack

TRAE宝像素表情包锻造流水线（Trae Skill）。

用已验证的「原图拆件 + 像素图形绘制 + Pillow 合成」流水线，从主题提示词生成完整表情包工程：**16 幕静态 PNG + 循环 GIF**。所有图形由程序确定性绘制，角色只用拆件拼装，**禁止任何生成模型画图或画字**。

## 特性

- **确定性渲染**：角色、道具、屏幕表情全部程序绘制，可复现、可调参。
- **角色一致性**：方头、屏幕脸、短四肢、无嘴，沿用原始灰阶与粗黑轮廓拆件拼装。
- **程序排版文字**：中文用系统字体栅格化 1-bit 字模，英文用 5×7 点阵，不依赖生成模型。
- **成品规格**：512×512 透明 PNG ×2 套（带字/无字）+ 3.2s / 12.5fps / 40 帧循环 GIF ×2 套。
- **自动校验**：`test.py` 十项检查（轨道闭环、色彩纪律、构图安全边界、GIF 动画帧数等）强制通过。

## 目录结构

```text
pixel-sticker-pack/
├── SKILL.md                    # 技能说明（Trae 加载入口）
├── references/
│   └── pipeline.md             # 创作手册：骨架/姿态/轨道/屏幕/道具 + 常见报错对照
└── assets/base/                # 完整脚手架（新工程从这复制）
    ├── build_assets.py         # 素材库构建（拆件 + NEW_PROPS 落盘）
    ├── render.py               # 全量渲染 PNG + GIF
    ├── test.py                 # 结构 + 成品双重验证
    ├── gif_codec.py            # GIF 编码器（稳定调色板 + disposal=2 防残影）
    ├── lib_base.py             # 屏幕表情原语（eyes/latin/cn_text/sparkle…）
    ├── rig.py                  # 角色骨架与姿态拼装
    ├── theme.py                # 16 个屏幕表情模式 + 主题专属道具 NEW_PROPS
    ├── scenes.json             # 16 幕配置（caption/action/screen/pose/tracks/props/effects）
    ├── requirements.txt
    └── assets/
        ├── manifest.json       # 部件注册表
        ├── parts/              # 角色拆件（头/躯干/四肢 × 左右）
        └── props/              # 通用道具库（coin/fireworks/bolt/receipt…）
```

## 安装

### 方式一：Git 克隆（推荐，可后续更新）

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.trae-cn\skills" | Out-Null
git clone https://github.com/heigoo/pixel-sticker-pack.git "$env:USERPROFILE\.trae-cn\skills\pixel-sticker-pack"
```

重启 Trae 后，`pixel-sticker-pack` 即出现在可用技能中。

更新：

```powershell
cd "$env:USERPROFILE\.trae-cn\skills\pixel-sticker-pack"
git pull
```

### 方式二：GitHub ZIP 下载

1. 打开 [pixel-sticker-pack](https://github.com/heigoo/pixel-sticker-pack) → **Code → Download ZIP**。
2. 解压后把 `pixel-sticker-pack` 文件夹整体放到 `~/.trae-cn/skills/`（Windows 即 `$env:USERPROFILE\.trae-cn\skills\`）。
3. 重启 Trae。

> 注意：ZIP 解压后目录内需直接包含 `SKILL.md`（不要多套一层 `pixel-sticker-pack-main`）。

### 验证安装

```powershell
Test-Path "$env:USERPROFILE\.trae-cn\skills\pixel-sticker-pack\SKILL.md"
# 输出 True 即安装成功
```

## 使用方法

1. **脚手架**：把 `assets/base/` 整目录复制为新工程（目录名用英文短横线，如 `mood-stickers`）。基础件永不修改。
2. **先读** `references/pipeline.md`，再动笔。
3. **主题创作**（只写两个文件）：
   - `theme.py`：16 个屏幕表情模式（70×36 面板函数）+ 主题专属道具 `NEW_PROPS`。
   - `scenes.json`：16 幕 = 4 章 × 4 幕；每幕含 caption/action/screen/pose/tracks/props/effects；`design` 块填 overview 标题、chapter_tones、discipline。
4. **构建渲染**（工作目录 = 新工程）：

```bash
python build_assets.py
python render.py                 # 全量 PNG+GIF；--static-only 仅静态
python test.py                   # 结构 + 成品双重验证
```

5. **目检**：Read `output/overview.png` 与 `output/keyframes-1/2.png`，核对姿势穿模、道具位置、屏幕内容；有问题改 `theme.py`/`scenes.json` 重跑，禁止手改输出图。
6. **交付**：补一份 `使用说明.txt`（成品清单/素材库/运行/复用）。

### 常用命令

```bash
python render.py --only 09_xxx --text "新文案"   # 单幕试改
python render.py --static-only --no-preview      # 快速出静帧
python test.py --quick                           # 只跑结构检查
```

## 硬性规则

- 每幕至少 1 条关键帧轨道（屏幕动画不算数），否则 GIF 被判「未产生动画」。
- 轨道 keys 覆盖 t∈[0,1]、严格递增、首尾同值（循环闭环）。
- 屏幕与文案文字一律程序排版，禁止生成模型画字。
- 红/黄/蓝是强调色，只允许出现在 `design.discipline` 登记的幕。
- 道具主色不得与机身外壳 #2B3031 / 暗面 #454E50 大面积同色。
- 构图安全边界：元素距边 ≥11px、不得侵入 y>536 文案区。
- 成品规格：512×512 透明 PNG + 3.2s/12.5fps/40 帧循环 GIF；test.py 校验帧数 ≥24 且总时长等于 defaults.duration_ms。

## 用户提示词 → 16 幕的映射方法

从主题提炼 4 章叙事弧（如 能量站=赚/花/危/友，保卫战=挣/花/空/回），每章 4 幕各配：1 个屏幕表情模式 + 1 个身体动作（轨道）+ 0-2 个道具/特效。幽默来自「抽象感受的像素化转译」。若用户只给短提示词，先按此结构提案 16 幕清单（幕名/动作/屏幕内容）请用户确认，再进入主题创作。

## 示例项目

本技能产出的两个完整示例，见 [pixel-sticker-pack-examples](https://github.com/heigoo/pixel-sticker-pack-examples)：

- **摸鱼日常（moyu-stickers）**：16 款「打工人摸鱼」表情——周一摸鱼、开小差、装忙、被逮到、下班、TGIF 等。
- **AI 编程搭档（coding-stickers）**：16 款「程序员的日常」表情——新需求、自动补全、复制粘贴、编译失败、代码评审、冲突、上线、下班等。

每个示例都包含完整工程（拆件 + 素材库 + 16 幕配置 + 渲染成品总览），可作为主题创作的参照模板。

## 许可

[MIT License](LICENSE) · Copyright (c) 2026 heigoo

允许自由使用、修改、分发（含商用），需保留版权声明；软件按「AS IS」提供，无任何明示或默示担保。
