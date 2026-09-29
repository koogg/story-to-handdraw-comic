---
name: article-illustration-planner
description: 深度分析文章脉络，精准规划插图点位与视觉意象，生成协同 280 种手绘风格与 36 种色彩画廊的高质量生图提示词。出具方案后主动引导用户进行【方式 A · 自主生图回填】或【方式 B · 全自动生图插入】，并支持将生成的配图精准自动排版回文章 Markdown。
---

# Article Illustration Planner (文章配图规划与插图回填)

Turn an article into a coherent visual-illustration plan and deliver the final illustrated article.

The user provides:

* An article text or local file path (e.g. `d:\path\to\article.md`);
* (Optional) A hand-drawn style number (`001`–`280`) and/or theme color (`C-01`–`C-36`). If omitted, the Skill automatically analyzes the article's mood, domain, and audience to recommend an optimal cohesive style and theme color combination;
* (Optional) Whitespace preference (`留白`: `正常` / `适中` / `多`). Default is `正常`;
* (Optional) Aspect ratio. Default is `4:3` (editorial reading standard). Note: Poster layout selection is strictly disabled for article illustrations.

The Skill decides:

* whether the article actually benefits from illustrations;
* where illustrations add the most value;
* how many illustrations are appropriate;
* what each image should communicate;
* whether an image should supplement, explain, replace, or reorganize part of the text;
* how to express each illustration in the selected or recommended visual style and theme color;
* how to guide the user seamlessly through image generation and automatic insertion into the article.

Do not mechanically illustrate every paragraph.

Do not distribute images at fixed intervals.

Do not force a predetermined number of illustrations.

The primary task is **visual editorial judgment**, not filling empty spaces with pictures.

---

# Core Principle

First determine:

> What does this article need visually?

Only then determine:

> What should each image contain?

The selected style number controls **how the image is drawn**.

It must not determine **what the image is about**.

Separate these two decisions:

1. visual communication strategy;
2. visual style and color palette.

---

# Default Behavior

Default to **Preserve mode**.

In Preserve mode:

* do not rewrite the article;
* do not delete article content;
* identify suitable insertion points;
* design illustrations that supplement the existing text.

Only modify, shorten, replace, or reorganize article text when the user explicitly requests or accepts **Visual Rewrite mode**.

The normal first response is an illustration plan, generation prompts, and the dual-track Call-to-Action (CTA).

---

# Inputs & Parameters

### 1. Article Content or File Path
- Direct text pasted in chat, or a local file path (e.g., `d:\path\to\article.md`).
- Always support absolute Windows paths cleanly.

### 2. Style & Color
- Style range: `#001`–`#280` from the local hand-drawn style library.
- Color palette: `C-01`–`C-36` from the 36 classic theme color gallery.
- Dynamic aesthetic reasoning: If user doesn't specify, analyze domain, mood, and tone to recommend the most expressive style and color palette.

### 3. Aspect Ratio (画幅比例)
- **Default: 4:3**. Editorial article illustrations naturally fit widescreen horizontal reading flow across Web, WeChat, Zhihu, and Markdown readers.
- Other supported ratios if user requests: `16:9`, `1:1`, `3:4`.
- **Layout Selection Disabled**: Poster layout selection (`SC-*`, `IG-*`, etc.) is disabled for article illustrations. Article illustrations are standalone editorial visuals integrated into prose.

### 4. Whitespace Control (留白控制)
- **正常 (Normal, Default)**: Standard compositional density. No additional whitespace keywords are appended.
- **适中 (Moderate)**: Appends `【大量留白】` / `[generous whitespace]` to the visual prompt.
- **多 (High)**: Appends `【大量留白，场景只显示必要部分，不要显示全】` / `[generous whitespace, show only essential elements of the scene, do not display the full context]` to the visual prompt.

---

# Modes

## Preserve Mode

Default mode.

Keep the article unchanged.

Illustrations may:

* establish atmosphere;
* create visual pauses;
* reinforce an important idea;
* make an abstract idea concrete;
* explain a difficult concept;
* visualize a process or relationship;
* create a visual transition;
* strengthen the ending.

The images supplement the article rather than replacing it.

---

## Visual Rewrite Mode

Use only when requested or clearly approved by the user.

The Skill may selectively:

* shorten repetitive passages;
* remove text that can be communicated more effectively through an image;
* convert explanatory prose into a visual relationship;
* turn long comparisons into visual comparisons;
* convert processes into visual sequences;
* reorganize a small section around an illustration.

Preserve the author's meaning, tone, and argument.

Do not rewrite the whole article simply because rewriting is allowed.

Prefer the smallest textual intervention that creates a meaningful improvement.

Never remove information whose precision is important and difficult to preserve visually (exact definitions, numbers, dates, legal or technical wording, important qualifications, source attribution, factual distinctions).

---

# Article Understanding

Before selecting images, understand the article as a whole.

Internally identify:

* central idea;
* article type;
* major sections;
* argument or narrative progression;
* information-density changes;
* emotional changes;
* conceptual difficulty;
* places where prose becomes repetitive;
* places where a visual could communicate something words are currently carrying inefficiently.

Do not expose lengthy internal analysis unless the user asks for it.

The visible output should focus on useful editorial decisions.

---

# Article Types

Infer dominant visual needs:

### Reflective / philosophical
* Metaphor, symbolic scenes, emotional transitions, visual pauses, restrained narrative moments.
* Avoid merely drawing a literal person who is "thinking", "sad", or "happy" when a stronger visual metaphor is possible.

### Narrative / personal essay
* Key moments, environmental storytelling, objects with narrative meaning, shifts in relationship, place, time, or emotional state.

### Explanatory / educational
* Concept visualization, analogy, causal relationships, processes, systems, hierarchy, comparison, transformation over time.
* Hand-drawn explanatory illustration may combine objects, characters, spatial relationships, labels, and diagrams.

### Argumentative / analytical
* Contrasts, competing forces, cause and effect, hidden relationships, structural models, before-and-after states.

---

# Illustration Functions

For every proposed image, decide its primary purpose:

* `opening-visual` — establishes the article's visual premise;
* `metaphor` — translates an abstract idea into a visual situation;
* `narrative-scene` — depicts a meaningful moment or situation;
* `concept-explanation` — makes a difficult concept easier to understand;
* `relationship` — visualizes relationships among ideas or entities;
* `process` — visualizes sequence, causality, or transformation;
* `comparison` — contrasts two or more states or ideas;
* `visual-pause` — creates rhythm and emotional breathing room;
* `transition` — bridges two sections;
* `summary` — condenses a section or conclusion visually;
* `text-replacement` — carries information that would otherwise require substantial prose.

---

# Image Type

For every proposed image, choose one concise image-type keyword:

* `editorial illustration` — a broad, article-led visual that establishes or reinforces an argument;
* `conceptual diagram` — an explanatory relationship, system, or abstraction;
* `process diagram` — a sequence, causal chain, cycle, or transformation;
* `comparison diagram` — a contrast between states, groups, or outcomes;
* `narrative scene` — a concrete, meaningful moment or situation;
* `metaphorical illustration` — a symbolic visual situation for an abstract or emotional idea.

Use the same selected value in the illustration plan and both copyable prompts.

---

# Selecting Illustration Positions

Choose illustration positions according to editorial value:

* where the article introduces its central idea;
* where an abstract idea becomes important;
* where the reader must understand a relationship;
* where explanation becomes text-heavy;
* where a major emotional or argumentative turn occurs;
* where the article shifts from one conceptual section to another;
* where a concrete scene makes an idea memorable;
* where the ending benefits from visual resonance.

Do not choose positions merely because a paragraph is long.

Do not insert an image when it would interrupt a strong reading rhythm.

The number of images should emerge naturally from the article (typically 2 to 5 for standard articles, 1 to 2 for short essays).

---

# Prompt Writing

Each image prompt should be concise enough to leave meaningful creative freedom to the image model.

The prompt structure:
1. **图片类型 / Image type**: `图片类型：{image_type}。` / `Image type: {image_type}.`
2. **主题与核心视觉意象**: Dominant visual idea, key subjects, environmental storytelling.
3. **留白修饰**: If `适中`, append `【大量留白】` / `[generous whitespace]`. If `多`, append `【大量留白，场景只显示必要部分，不要显示全】` / `[generous whitespace, show only essential elements of the scene, do not display the full context]`.
4. **画风与色彩基调**: Hand-drawn style definition from `#001`–`#280` and theme color from `C-01`–`C-36`.

---

# Output Format

Start with a concise overall recommendation:
* Inferred article type;
* Visual strategy;
* Recommended number of illustrations;
* Recommended style number & name, theme color & name, aspect ratio (`4:3`), and whitespace setting.

Then provide each illustration in reading order:

```markdown
### Illustration N

**插入位置 / Insert after:**
`[引用目标小标题或紧邻的上文段落前/后 10-20 个字]`

**配图定位 / Purpose:**
解释该图在阅读流中的作用。

**图片类型 / Image Type:**
editorial illustration / metaphorical illustration / conceptual diagram ...

**视觉构思 / Visual Concept:**
描述核心视觉隐喻、主体与画面情绪。

**图文关系 / Relationship to Text:**
supplements text / explains text / visually summarizes text / replaces part of text

**画风与配色 / Style & Color:**
`#{style_number} · {style_name}` + `{color_id} · {color_name}`

**生图提示词 (Prompt):**
- **中文提示词**:
```text
图片类型：{image_type}。{visual_concept}。{whitespace_clause}画风：{style_prompt}。色彩：{color_prompt}。画幅比例 4:3。
```
- **English Prompt**:
```text
Image type: {image_type}. {visual_concept_en}. {whitespace_clause_en} Style: {style_prompt_en}. Color palette: {color_prompt_en}. Aspect ratio: 4:3.
```
```

---

# Post-Planning Call-to-Action (CTA)

Immediately following the illustration plan, the Skill **MUST** output the standardized dual-track delivery CTA block:

```markdown
---

💡 **插图方案已规划完成！接下来您可以选择以下两种交付方式：**

1. **【方式 A · 自主生图回填】**：
   复制上方提示词，前往您常用的生图工具出图。生成完成后，将图片文件直接拖入对话，或发送本地图片路径（如 `D:\path\to\illus1.png`），我会帮您将配图精准插入到文章对应位置中！

2. **【方式 B · 全自动生图插入】**：
   直接对我说 **“全自动生图”** 或 **“帮我生成所有配图并插入”**，我将全自动调用生图工具批量绘制配图，并自动排版回填到文章对应锚点中，输出完整的图文定稿！
```

---

# Dual-Track Delivery Workflow (双轨交付流程)

## Track A · 自主生图回填 (Manual Generation & Back-fill)

When the user chooses Track A and provides images:
1. **Image Receipt**: User pastes images into chat, or supplies local image file paths / URLs.
2. **Anchor Matching**: The Skill matches each received image to the corresponding Illustration N (`Illustration 1`, `Illustration 2`, etc.) based on visual content or user specification.
3. **Local File Management**:
   - If the user provided a local article path (e.g. `D:\path\to\my_article.md`):
     - Create an assets folder: `D:\path\to\images\` (relative `images/`).
     - Save/copy the received image into `D:\path\to\images\illus_01.webp` (or `.png`/`.jpg`).
     - Use relative path `images/illus_01.webp` in Markdown.
   - If the article was provided as chat text:
     - Store images in the conversation artifact directory or working directory, using clean markdown syntax.
4. **Markdown Insertion Standard**:
   Insert the image block immediately after the designated anchor point:
   ```markdown
   ![插图N: 说明](images/illus_0N.webp)
   *▲ 图N：说明*
   ```
5. **Output**:
   - For local file: Write the illustrated article to `D:\path\to\my_article_illustrated.md` (or update original if requested by user).
   - For chat text: Output the full illustrated article Markdown ready to copy.

---

## Track B · 全自动生图插入 (Fully Automated Generation & Insertion)

When the user triggers Track B (e.g. "全自动生图", "帮我生成并插入", "自动完成"):
1. **Execution Verification**: Confirm the target article location (file path `d:\path\to\article.md` or in-memory draft).
2. **Automated Image Generation**:
   - For each planned Illustration N in sequential order:
     - Call the image generation tool (`generate_image`) using the finalized prompt.
     - Specify aspect ratio `4:3` (unless customized by user).
     - Maintain strict style `#001`–`#280` and color consistency.
3. **Asset Organization**:
   - Save each generated image to `<article_dir>/images/illus_01.webp`, `illus_02.webp`, etc.
4. **Automatic Insertion & Assembly**:
   - Read the original article markdown.
   - Accurately locate each anchor point (`Insert after:` heading or sentence excerpt).
   - Insert the formatted image link and caption:
     ```markdown
     ![插图N: 说明](images/illus_0N.webp)
     *▲ 图N：说明*
     ```
   - Save the finalized document as `[article_name]_illustrated.md` (or write in-place if requested).
5. **Final Presentation**:
   - Provide a brief summary table of generated illustrations.
   - Present the path to the newly created illustrated article, or display the illustrated article directly.

---

# Automation Helper Script

The Skill provides a deterministic Python helper script located at:
`skills/article-illustration-planner/scripts/insert_illustrations.py`

Usage:
```bash
python -X utf8 skills/article-illustration-planner/scripts/insert_illustrations.py \
  --article "D:\path\to\article.md" \
  --manifest "D:\path\to\illustrations_manifest.json" \
  --output "D:\path\to\article_illustrated.md"
```

The manifest format:
```json
[
  {
    "index": 1,
    "anchor": "### 1. 概念起源",
    "position": "after",
    "image_path": "images/illus_01.webp",
    "caption": "图1：概念起源与核心意象"
  }
]
```

The script cleanly preserves indentation, headings, code blocks, and math formulas without touching unintended text.

---

# Design Philosophy

This Skill should remain intentionally lightweight and high-taste.

Prefer:
* visual editorial judgment over rules;
* meaning over generic templates;
* article-specific visual thinking over clichés;
* clean dual-track execution over tedious back-and-forth;
* seamless integration from prompt planning to final illustrated Markdown delivery.
