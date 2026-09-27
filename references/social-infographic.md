# 社媒卡与信息图

用于 social-card / 社媒卡和 infographic / 信息图。复用主技能的画风解析、人物参考和生图流程，但不加载漫画分镜目录或单张图文的禁止分区规则。

## 选择排版

从 [排版目录](social-infographic-catalog.md) 读取对应类型；用户指定编号时直接定位该条。画风编号与 SC-/IG- 排版编号是独立维度，可以任意搭配。保留用户指定的排版；SC-013 在来源中不存在，遇到无效编号说明并提供相近选项，不自行补造。

- 社媒卡：围绕短文案、观点或社交分享组织层级。文字主导可选 SC-002/007/009/016；上下图文可选 SC-001/008；双区对照可选 SC-003/004/010/015；主视觉与标签可选 SC-011/014/017/018/019/020。依据实际内容选一种，不为凑版式添加无关信息。
- 信息图：先识别知识关系。比较可选 IG-003/004/011，流程 IG-008，时间轴 IG-009，层级 IG-001/010/012，分类 IG-016，思维导图 IG-017，循环 IG-019，数据比例 IG-024。其余需求从目录匹配；不要用箭头暗示原文没有的因果、顺序或依赖。

“一张图”是输出数量，可包含多个信息区；“不分镜”允许信息分区，但不是连续剧情。明确要求不分区时选择兼容的版式，若与指定编号冲突则澄清。默认一张竖版，明确比例、数量和平台优先。来源提示词中的“小红书”只表示原示例用途，不自动添加小红书发布套餐、标识或水印。

预览已全部保存在本地，可通过目录或[离线排版画廊](../assets/handraw-style/skills/handdraw-style-prompter/gallery/layouts.html)按需查看，仅参考布局。预览不可用时可依据目录文字继续，并如实说明未查看预览。若把预览附给生图工具，先检查图片并标为 LAYOUT，仅用于位置、比例、层级和阅读顺序，不复制其文字、角色、内容或画风；与 STYLE、PERSON 分别标明用途。

## 表现力优先

社媒卡和信息图默认把每张图当作独立视觉作品：围绕本页内容选择最有力的主体、动作、场景、尺度、视觉隐喻和排版，不自动复用同一人物、服装、场景或构图。多页只共享已选画风及用户明确要求的品牌或系列锚点；用户未要求统一版式时，可为不同内容选择不同但合适的 SC-/IG- 机制。

SC-/IG- 编号规定的是关键结构、层级、信息关系和阅读顺序，不是必须机械执行的坐标或百分比。只在文字安全区、数据比较或用户明确尺寸要求确有必要时写精确比例。逐字文字只锁定文字，不能据此锁死画面；避免为统一而添加固定主角、固定服装、固定背景或与内容无关的连续性设定，也避免堆叠不会改变结果的长串禁止项。

信息图的表现力不得牺牲事实：数值、单位、排序、因果、分类、比例与连线关系仍是硬约束；人物和场景一致性通常不是。社媒卡则优先形成鲜明主视觉和图文张力，只在用户明确要求套系一致时收紧变化范围。

## 文本与信息组织

社媒卡可按主技能的创作性改编生成有表现力的短文案；逐字保留和指定文字仍优先。双区卡是观点、前后或对照关系，不强制编成漫画故事。

两类都必须尊重解析后的画风，并主动保留创意空间：排版规定关键结构和阅读关系，不锁死主体、姿态、局部位置、留白与图文呼应。信息图也可使用新颖的解释角度、视觉隐喻、图标和场景化表达，让信息更容易理解；类比不能冒充事实，创意不能改变数据含义。逐字保留只锁定文字，不取消画面创意。排版样图的画风不能覆盖用户选择的画风。

信息图默认忠实提炼：允许压缩措辞、分类和调整呈现顺序，不得自由改写事实、数量、时间、单位、排名、因果或结论。保留来源和必要口径；缺少支撑的数据不能为了填满版式而编造。示例数据仅在用户要求时使用并显著标注。涉及数据的图形比例、排序、轴含义与标签必须一致；没有依据时选择定性布局或索取必要数据。

先列出最终标题、标签、说明及其对应视觉元素和关系，再安排到版式中。不要机械填满目录建议的槽位；以可读性和用户信息为准。内容放不下时精简非锁定文字；不得擅自增页或删掉必需信息，必要时询问取舍。

## 生图提示词与验收

输出计划为 **画风 → 类型 → 文本 → 排版**，同时说明语调与已选可选项；排版写明编号、名称、阅读顺序和信息区，不输出分镜字段。仅要求展示方案而不要求写入提示词文件时止于此；要求写入提示词文件或要求出图时，均需按 [rendering.md](rendering.md) 继续执行。

每张图的提示词必须遵循以下契约结构进行组装，以保持输出稳定性：

```text
Asset type: {social-card or infographic}
Canvas and audience: {ratio; intended readers/destination if supplied}.
Style: #{number} · {generation_name}; {resolver-required positive traits}.
Theme color: {optional matched prompt from colors.json, or omit}.
Layout mechanism: {SC-/IG- ID and name}; {its spatial structure and reading order from the catalog}.
Core idea and tone: {retained broad meaning or factual relationship; selected attitude}.
Information zones & display text:
- Zone 1 ({placement/role}): "{text}"
- Zone 2 ({placement/role}): "{text}"
(List all zones with exact adapted copy or checked factual text. Identify explicitly LOCKED spans.)
Visual concept & hierarchy: {how elements and empty space are arranged; mobile legibility}.
Explicit must-keeps: {only user-required elements, or omit}.
Style reference instruction: {when a style image accompanies the prompt, write exactly “以该图作为艺术风格参考。”; otherwise omit}.
Other reference mapping: {only PERSON or LAYOUT relationships required to understand the supplied images; otherwise omit}.
Render the specified layout mechanism. Do not hallucinate unrequested facts, data, or decorative text.
```

检查文字、信息完整性、编号对应的布局特征、图文对应关系、阅读顺序及事实/数值/连线准确性。多区社媒卡和信息图不能套用 single-graphic 的“必须无分区”检查。共用 rendering 的每图重试上限，不因切换类型重置。无法可靠呈现精确文字或数据时标记待排版/待修正，不宣称成品准确。保存名可用 social-card-01.png、infographic-01.png；工具不可用时保存对应的完整提示词文件。

提示词模式面向 ChatGPT 网页时，不把本地画风路径、文件名、STYLE 标签、输入序号、附件角色表或上传说明写入 Markdown；若使用画风参考图，每个可复制提示词仅加入一次“以该图作为艺术风格参考。”。直接调用生图工具时才按工具要求传递和标记附件。
