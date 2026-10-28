# 流水线创作手册

本文是 pixel-sticker-pack 技能的深度参考。坐标系统：640×640 工作画布，左右指观众视角，角度逆时针为正。

## 1. 角色骨架（rig）

- 脖颈锚点 `neck: [320, 310]`；肩位 = neck ± (89/90, +10)，即左肩 (231,320)、右肩 (410,320)。
- 手臂从肩起算可达 107px（含手）；`bent_arms` 两段：上臂 60px + 前臂 68px。
- **手臂角度语义**：0 = 垂直向下，wrist = shoulder + 107·(sin a, cos a)。正角把手腕甩向 +x。
  - 左臂向身体中线 = 正角；右臂向中线 = 负角。外侧上举 = 左负右正。
- 头部件 front_head 308×233，pivot (153,230)；屏幕区在头内 (49,72)-(259,180)，即 70×36 逻辑面板的 3×。
- 头顶 y≈80，手臂伸直最高只到 y≈215 —— **手够不到头顶**，"抱头"类动作用手贴脸颊替代。
- 腿部件在 (neck ∓35/36, ny+115)。

## 2. 已验证姿势配方（直接抄）

| 意图 | pose 写法 |
|---|---|
| 欢呼 | `{"arms":[-117,117]}` |
| 单手举旗/敬礼 | `{"arms":[0,146]}`（右）或 `[-146,0]`（左） |
| 招手 | `{"arms":[0,20]}` + `arms.1` 轨道 20→150→118→150→20 |
| 双手奉上/递物 | `{"arms":[62,-62]}`（手会合于胸前三四百像素处） |
| 叉腰 | `{"bent_arms":{"left":{"upper":-52,"lower":118},"right":{"upper":52,"lower":-118}}}` |
| 抱持（抱砖/抱瓜） | `{"bent_arms":{"left":{"upper":40,"lower":130},"right":{"upper":-40,"lower":-130}}}` |
| 合十/祈祷 | `{"bent_arms":{"left":{"upper":45,"lower":55},"right":{"upper":-45,"lower":-55}}}` |
| 按计算器（右手） | `{"bent_arms":{"right":{"upper":-35,"lower":-125}}}` + 道具 `anchor:"right_wrist"` |
| 抓狂贴脸 | `{"bent_arms":{"left":{"upper":-25,"lower":-155},"right":{"upper":25,"lower":155}}}` |
| 摊手/垂放 | `{"arms":[0,0]}` |
| 鞠躬 | `rotation` 轨道 0→17→17→0（正向 = 向观众右侧躬） |

镜像对称部件不可互换：left 永远用 front_arm_left，禁止水平翻转 right 冒充。

## 3. 关键帧轨道（tracks）

```json
{"path":"arms.0","keys":[[0,-45],[0.35,-128],[0.5,-128],[0.62,-70],[1,-45]]}
```

- path 相对 pose：支持 `arms.0/1`、`legs.0/1`、`offset.0/1`、`head_angle`、`rotation`、`bent_arms.right.lower` 等。
- 时间归一化 0–1，严格递增，**首尾必须同值**（循环闭环，test.py 强制）。
- 插值默认 cosine（缓入缓出）；`"interpolation":"linear"` 或 `"step"`（抖动/抽搐用 step）。
- 每幕至少 1 条轨道，否则 GIF 会被判「未产生动画」而报错。
- 常用节奏：小跳 `offset.1 [[0,0],[0.2,-26],[0.4,0],[0.6,-16],[1,0]]`；呼吸 `[0,0],[0.5,±5],[1,0]`；摇摆 `rotation ±4~5`；抽搐 `step` 多段 ±5。

## 4. 屏幕表情（theme.py 的 SCREENS）

- 每个模式是 `fn(t) -> 70×36 RGBA 面板`；**t=0 必须等于静态帧**（所有偏移用 `osc`/`blink`，天然 t=0 归零）。
- 眼位 cx=22/47，默认眼基线 cy≈19；眼睛原语：`eyes_default/happy/star/heart/plead/half/power/seed`。
- 文字：`latin('OK+100%…')` 5×7 点阵（字符集见 lib_base.GLYPHS，缺字符会报错）；中文用 `cn_text('来！','green')`（系统字体栅格化 1-bit 字模）。
- 常用小件：`sparkle(d,x,y,t)` 星光、`shape(ROWS,color)` ASCII 图案、`polygon_im` 多边形、`panel()` 底板。
- SCREENS 四元组 `(id, name, brief, colors, fn)`；id 即 scenes.json 的 `screen` 字段。

## 5. 道具与特效（props/effects/behind）

- 条目：`{"asset":"名","center":[x,y],"scale":1,"angle":0}` 或 `{"asset":"名","anchor":"left_wrist","offset":[dx,dy]}`（跟随手腕，随轨道摆动）。
- 循环动画 `anim`：`blink`(freq,duty)、`pulse`/`flicker`(freq,amount)、`bob`(freq,amp)、`sway`(freq,amp)。
- 渲染层级：behind → 角色 → props → effects（前景道具会盖住身体）。
- 新道具：`theme.py` 里写 builder（原生整数像素、1px 墨黑轮廓、透明留白、无抗锯齿），登记进 `NEW_PROPS`；build_assets.py 负责落盘与目录登记，**未经登记的图片路径 render 会拒绝**。
- 注意 anchor 用未整体旋转前的舞台坐标；若人物整体 rotation/offset，道具位置需同步调整。

## 6. 色彩纪律与 design 块

- 基色：墨黑 #101313 / 机身 #2B3031 / 暗面 #454E50 / 白 / 纸白 #EEF3EE；强调色：绿 #5ADB97 / 薄荷 #A9E6CC / 金 #F4CD70 / 红 #EC6269 / 蓝 #316BCA。
- 红/黄/蓝是稀缺强调色：只允许出现在 `design.discipline` 里登记的幕（如 `{"red":["12_crashed"],...}`）；审计扫描渲染结果（α≥128 的像素），违规即渲染失败。
- 章节色 `chapter_tones` 只影响总览标签；`chapters` 字符串用于「四章各 4 幕」校验。

## 7. 成品与校验

- 输出四套：png / no-text（512×512 透明 PNG）+ gif / gif-no-text（3.2s 循环，12.5fps，40 帧）。
- GIF 编码（gif_codec.py）：统一调色板 + 独立透明索引 + disposal=2 防残影 + 逐帧解码比对；`distinct_frames < 2` 会报错。
- 文案区：画面元素不得越过 y=536；底部白边 8px 由 render 自动加。
- test.py 十项检查全过才算完成；任何 FAIL 修数据/修图形，不许绕过检查。

## 8. 常见报错与修法

| 报错 | 原因与修法 |
|---|---|
| `构图超出安全边界` | 道具/姿态出界：减 scale、挪 center、减轨道幅度 |
| `道具侵入文案安全区` | 元素最低点 y>536：整体上移 |
| `违反色彩纪律` | 强调色出没：改色，或把幕 id 加进 design.discipline |
| `字模缺少字符` | latin() 用了不在 GLYPHS 的字符：换字符或加字模，中文用 cn_text |
| `GIF 未产生动画` | 缺轨道或屏幕无 t 变化：加一条 track 或屏幕动画 |
| `GIF 只有个位数帧` | 该幕只有屏幕动画、没有身体轨道，静止段被编码器合并：按第 3 节给 pose 补 2–4 条连续轨道（振幅 ≥5°，避免被判定为相同帧） |
| 道具贴在身上看不清 | 道具主色与机身同色（占面积 >50% 时最严重）：换亮色面（如 paper 纸白）+ 暗面棱，保留 1px 墨黑轮廓；细长剪影有描边可容忍 |
| `素材不在统一库内` | 引用未登记 PNG：先进 NEW_PROPS 并跑 build_assets.py |
| `关键帧需要覆盖 0–1 且首尾值相同` | 轨道 keys 首尾不等：补齐端点 |
| `屏幕库目录与 theme 注册表不一致` | 改了 SCREENS 忘跑 build_assets.py |
