---
name: pixel-sticker-pack
description: 生成 TRAE宝像素表情包工程（16 幕静态 PNG + 循环 GIF）。Use when the user gives a theme or prompt for a new sticker pack, asks for 表情包/贴纸/GIF 动图 generation from the verified pipeline, or wants to add or modify scenes in an existing pack. Do not use for AI image generation requests.
---

# 像素表情包锻造（TRAE宝流水线）

用已验证的「原图拆件 + 像素图形绘制 + Pillow 合成」流水线，从主题提示词生成完整表情包工程。**禁止使用任何生成模型画图或画字**——所有图形由程序确定性绘制，角色只用 `assets/parts/` 的拆件拼装。

## 执行流程

1. **脚手架**：把本技能 `assets/base/` 整目录复制为新工程（建议放当前工作区，目录名用英文短横线，如 `mood-stickers`）。基础件永不修改：`rig.py`、`gif_codec.py`、`lib_base.py`、`assets/parts/`、`assets/manifest.json`、`assets/props/`。
2. **先读** [references/pipeline.md](references/pipeline.md)（姿态/轨道/屏幕/道具创作手册 + 常见报错对照），再动笔。
3. **主题创作**（只写两个文件）：
   - `theme.py`：16 个屏幕表情模式（70×36 面板函数，见参考手册原语表）+ 主题专属道具 `NEW_PROPS`。文件内已内置「积分能量站」完整示例，可仿写。
   - `scenes.json`：16 幕 = 4 章 × 4 幕；每幕含 caption/action/screen/pose/tracks/props/effects；`design` 块填 overview 标题、chapter_tones、discipline（红/黄/蓝允许出现的幕 id 清单）。
4. **构建渲染**（工作目录 = 新工程）：
   ```bash
   python build_assets.py
   python render.py                 # 全量 PNG+GIF；--static-only 仅静态
   python test.py                   # 结构 + 成品双重验证
   ```
5. **目检**：Read `output/overview.png` 与 `output/keyframes-1/2.png`，核对姿势穿模、道具位置、屏幕内容；有问题改 `theme.py`/`scenes.json` 重跑，禁止手改输出图。
6. **交付**：按 `使用说明` 格式补一份 `使用说明.txt`（结构见 base 内示例工程 energy-stickers 同名文件的精神：成品清单/素材库/运行/复用）。

## 硬性规则

- 每幕至少 1 条关键帧轨道（屏幕动画不算数）：只靠屏幕动画时，静止段会被 GIF 编码器合并，实拍帧数可能掉到个位数，动作等于没有。由 test.py「每幕至少 1 条动作轨道」强制。
- 轨道 keys 覆盖 t∈[0,1]、严格递增、首尾同值——循环闭环由 test.py 强制。
- 屏幕与文案文字一律程序排版（`latin` 5×7 字模 / `cn_text` 系统字体栅格化），禁止生成模型画字。
- 红/黄/蓝是强调色，只允许出现在 `design.discipline` 登记的幕；audit 不过就改图形或改登记，不许放宽阈值。
- 道具主色不得与机身外壳 #2B3031 / 暗面 #454E50 大面积同色：贴胸摆放会糊成一片，只剩描边。test.py 会给出 WARN 提示。
- 构图安全边界：元素距边 ≥11px、不得侵入 y>536 文案区（render 会报错）。
- 成品规格：512×512 透明 PNG ×2 套（带字/无字）+ 3.2s/12.5fps/40 帧循环 GIF ×2 套；test.py 校验帧数 ≥24 且总时长等于 defaults.duration_ms。

## 常用命令

```bash
python render.py --only 09_xxx --text "新文案"   # 单幕试改
python render.py --static-only --no-preview      # 快速出静帧
python test.py --quick                           # 只跑结构检查
```

## 用户提示词 → 16 幕的映射方法

从主题提炼 4 章叙事弧（如 能量站=赚/花/危/友，保卫战=挣/花/空/回），每章 4 幕各配：1 个屏幕表情模式 + 1 个身体动作（轨道）+ 0-2 个道具/特效。幽默来自「抽象感受的像素化转译」。若用户只给短提示词，先按此结构提案 16 幕清单（幕名/动作/屏幕内容）请用户确认，再进第 3 步。
