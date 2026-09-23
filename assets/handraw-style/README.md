# 本地手绘风格库

当前收录 **001–277 种手绘风格**和 **30 种经典单色主题色**，与本地参考图一同打包。主 Skill 通过解析器读取资源，无需联网或重新安装上游仓库。

- [排版与分镜画廊](skills/handdraw-style-prompter/gallery/layouts.html)：19 种社媒卡、32 种信息图、68 种分镜，预览与提示词均可离线查看。
- [色彩画廊](skills/handdraw-style-prompter/gallery/colors.html)：30 种经典单色主题色及可复制提示词。
- [编号画廊](skills/handdraw-style-prompter/gallery/index.html)：查看和选择画风；已知编号时直接解析。
- [风格目录](styles_200_reorganized.md)：名称和视觉特征的权威源。
- [提示词 Skill](skills/handdraw-style-prompter/SKILL.md)：独立使用时输出双语提示词，支持纯图和图文模式；明确要求时生图。
- [海报 Skill](skills/poster-prompt-generator/SKILL.md)：用八个结构化字段生成图文一体海报提示词，复用本地画风、主题色与模型能力矩阵。
- [新增画风](.agents/skills/style-library-importer/SKILL.md)：本地参考图与文字描述入库，先预检再追加编号。

生图模型未暴露时使用 unknown 策略；名称和特征不足以激活画风时附加编号参考图。完整规则由上述 Skill 与解析器维护。

保留整个目录使用，不能只复制嵌套 Skill。维护与校验命令从此目录执行：

```sh
python -B -X utf8 skills/handdraw-style-prompter/scripts/build_library.py
python -B -X utf8 skills/handdraw-style-prompter/scripts/validate_library.py
```

第一条仅在修改风格目录后重建派生索引和画廊；第二条只读校验。

## 风格图片

### A · 国际社论漫画 / 幽默手绘（001–035）

![A 001–016](images/A_001-016.webp)

![A 017–032](images/A_017-032.webp)

![A 033–035](images/A_033-035.webp)

### B · 国际绘本 / 叙事型手绘（036–054）

![B 036–048](images/B_036-048.webp)

![B 049–054](images/B_049-054.webp)

### C · 现代平面 / 艺术化人物体系（055–082）

![C 055–070](images/C_055-070.webp)

![C 071–082](images/C_071-082.webp)

### D · 日本作者 / 当代插画体系（083–123）

![D 083–098](images/D_083-098.webp)

![D 099–114](images/D_099-114.webp)

![D 115–123](images/D_115-123.webp)

### E · 中国作者 / 当代插画体系（124–154）

![E 124–139](images/E_124-139.webp)

![E 140–154](images/E_140-154.webp)

### F · 通用网感 / 媒介 / 地域手绘（155–200）

![F 155–170](images/F_155-170.webp)

![F 171–186](images/F_171-186.webp)

![F 187–200](images/F_187-200.webp)

### G · 附件新增 / 中国当代插画补充（201–216）

![G 201–216](images/G_201-216.webp)

### H · 其他（217–277）

![H 217–232](images/H_217-232.webp)

![H 233–248](images/H_233-248.webp)

![H 249–264](images/H_249-264.webp)

![H 265–277](images/H_265-277.webp)

授权：[本库许可证](LICENSE) · [第三方授权](THIRD_PARTY_NOTICES.md)。
