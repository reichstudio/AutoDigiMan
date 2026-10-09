# 数字人口播生产页数据契约

三页由同一份**内存项目数据**生成。以 `assets/project-data.template.json` 作为字段参考，在内存或标准输入中填写项目数据，先运行 `scripts/validate_project_data.py -`，最后运行 `scripts/build_pages.py -`。**不得**在项目目录或交付物中创建 `project-manifest.json`；三张 HTML 内联的 `dh-project-data` 是唯一允许保留的项目数据副本。

```json
{
  "title": "项目名称",
  "subtitle": "可选页眉副标题",
  "page_titles": {
    "asset": "资产清单与生成提示词",
    "h3": "MiniMax H3 全片分镜提示词｜数字人口播版",
    "list": "分镜列表｜数字人口播版"
  },
  "package_mode": "digital_human",
  "audio_references": [
    {
      "id": "A1",
      "file": "A1.mp3（扩展名按实际音频文件自动保留）",
      "role": "voice_timbre_reference",
      "h3_label": "<Audio 1>",
      "speaker": "<Subject 1> (S1)"
    }
  ],
  "video_references": [
    {
      "id": "V1",
      "file": "V1.mp4（扩展名按实际视频文件自动保留）",
      "h3_label": "<Video 1>"
    }
  ],
  "source_documents": [
    {
      "path": "需求与台词.docx",
      "role": "production_requirements | locked_script | both",
      "status": "readable"
    }
  ],
  "production_requirements": [
    "从用户文档或对话确认后采用的制作要求摘要"
  ],
  "locked_script_source": {
    "kind": "document | conversation | ai_generated",
    "path": "需求与台词.docx；非文档来源时留空"
  },
  "total_duration_seconds": 96.5,
  "timing_note": "数字人分镜：时长由各镜 seconds 指定；range 固定为全零，仅供共用页面显示。",
  "aspect_ratio": "16:9",
  "resolution": "3840x2160",
  "language": "中文",
  "style_note": "写实演播室",
  "pacing_style": "normal 或 fast_cut（电商带货节奏风格，其他场景留空）",
  "assets": [
    {
      "id": "P1",
      "asset_id": "HOST-01",
      "name": "讲者或资产名称",
      "kind": "locked 或 generated",
      "reference_ids": [],
      "use": "它在 H3 中服务的镜头和用途",
      "prompt_en": "English GPT Image 2 自然语言提示词（正面陈述）",
      "prompt_zh": "中文自然语言工作版提示词"
    }
  ],
  "shots": [
    {
      "id": "H3-001",
      "range": "00:00:000–00:00:000",
      "seconds": 6.4,
      "section": "开场 / 引入",
      "title": "分镜名称",
      "mode": "speak | demo | broll | hold",
      "performer": "出镜讲者，或 画外音 / 插入画面",
      "voice_reference": "A1.mp3",
      "video_refs": ["V1.mp4"],
      "speech": "本镜锁定台词原文，或 本段无口播",
      "references": ["P1", "P2"],
      "camera": "全中文机位、构图、运镜与主动态",
      "scene": "全中文场景与用光",
      "action": "全中文完整动作叙事",
      "continuity": "硬切说明，或上一终帧到本首帧的连续关系和本镜终帧",
      "prompt_en": "完整 English Ref2VA prompt",
      "prompt_zh": "完整中文 H3 工作提示词"
    }
  ]
}
```

## 硬性约束

- `page_titles` 必填。`asset`、`h3`、`list` 分别是资产页、H3 提示词页和中文分镜页的浏览器标题与页面主标题；模板的标题由这三个字段统一设定。
- 数字人项目必须写 `package_mode: "digital_human"`。不得写 `master_audio`，不提供分段试听或背景音轨。
- `source_documents`、`production_requirements` 与 `locked_script_source` 为可选的内存来源记录：扫描到并采用文档时，记录实际相对路径、用途与可读状态；制作要求是已经决定资产、分镜和提示词的约束摘要；`locked_script_source.kind` 为 `document`、`conversation` 或 `ai_generated`。这些字段可被三页内联数据保留，但不得另行写成 `project-manifest.json`。任何“稍后提供”的素材/文档不得记录为已读或已引用。
- 每个数字人镜头只有两个时间字段：`range` 固定为 `00:00:000–00:00:000`，只为与 MV 共用页面模板而显示；`seconds` 是 0.2–30 的数值，是页面时长与 H3 生成时长的唯一来源。不得写 `audio_slice`，也不得用 `range` 推导时长。
- `references` 是全局 `P#`（人物、场景、产品/道具合计）。每个镜头最多九项；H3 中的 `<Picture N>` 严格按该数组顺序换算。
- `audio_references` 中的 `A#` 是项目级音色资产 ID，`h3_label` 是当前 H3 单元的 `<Audio N>` 标签；`A#` 服务项目查找，`<Audio N>` 服务单元上传。每个镜头最多三个参考音色。音色参考在每个受影响单元的 `subject_definitions` 中单独定义 `<Audio N>` 并绑定 `<Subject N> (Sx)`，在 `summary` 标明 `audio reference`，在 `retention_analysis` 使用 `reference`；原始信号不复用。
- 音频参考文件按输入顺序命名为 `A1`、`A2`、`A3`，视频参考文件按输入顺序命名为 `V1`、`V2`、`V3`；复制到制作包时保留原文件扩展名，例如 `A1.mp3`、`A2.wav`、`V1.mp4`、`V2.mov`。不得另起任意文件主名。页面必须展示实际带扩展名的 `file` 值。
- `video_references` 中的 `V#` 是项目级视频资产 ID，`h3_label` 是当前 H3 单元的 `<Video N>` 标签；每镜的 `video_refs` 填写实际带扩展名的文件名，如 `V1.mp4`。每镜最多三个参考视频。
- 数字人项目的 `audio_references` 只允许 `voice_timbre_reference`。每镜可用 `voice_reference` 指向其中的文件；它不含任何时间字段，不作为口播、背景音、环境声、配乐、歌词、节拍或剪辑依据，节点以整段音色参考加载且不自动裁切。
- 每个 `speech` 必填；无口播时填写精确文本 `本段无口播`。口播台词与锁定脚本逐字一致。
- `mode` 取值：`speak`（出镜口播）、`demo`（出镜演示/操作）、`broll`（画外音插入画面）、`hold`（静置/空镜）。
- `prompt_en` 必须是可复制的六字段 Ref2VA 提示词；`prompt_zh` 保持相同字段顺序。
- 资产卡 `prompt_en` / `prompt_zh` 为自然语言段落式图像提示词，按官方顺序组织（场景→主体→细节→风格→构图→用光→色彩→文字→正面约束），全部为正面陈述；用途、类型、`P#` 等管理信息留在卡片展示层。
- `camera`、`scene`、`action`、`continuity` 同时服务全中文分镜列表，页面之间共享同一套内容。
- 时长估算依据记录在 `timing_note`；总时长记录在 `total_duration_seconds`；用途记录在项目说明或 `subtitle`，并体现在 `page_titles` 后缀中。
- `pacing_style` 仅电商带货项目必填：`normal`（每单元 1–2 个内部切镜）或 `fast_cut`（约 15 秒单元内 2–3 秒一次高密度切镜），由启动确认确定；其他场景留空。
- 四个项目定义项随启动确认一并核对：各镜时长与估算依据记录在 `seconds`、`total_duration_seconds` 与 `timing_note`（`timing_note` 同时记录语速档位，如：预估，稳档 160–200 字/分钟），画幅与分辨率记录在 `aspect_ratio` 与 `resolution`（写入 GPT Image 2 资产卡与分镜 meta），口播语言记录在 `language`（决定 `<d>[Language]` 标签），视觉风格基调记录在 `style_note`（决定 H3 提示词开头风格句与资产风格栏）。用户未提供时使用默认值——预估时长、3840×2160 16:9 横版、中文、写实演播室——并写进启动确认清单供用户调整。

## 生成命令

`<技能包目录>` 指本技能的安装位置（Windows 下通常为 `C:\Users\<用户名>\.agents\skills\feihou-digital-human-storyboard-prompts`）；`<输出目录>` 为三张 HTML 的交付目录。以下演示以 PowerShell 内存字符串传递数据，**不创建项目 JSON 文件**。

```powershell
$projectData = @'
{ ...符合本页数据契约的 JSON... }
'@
$projectData | py -3.12 <技能包目录>\scripts\validate_project_data.py -
$projectData | py -3.12 <技能包目录>\scripts\build_pages.py - <输出目录>
```

生成器输出：

1. `TITLE_GPT_Image2_资产清单.html`
2. `TITLE_MiniMaxH3_Shotlist.html`
3. `TITLE_全中文分镜列表.html`

## 资产图片路径与依赖

按照 [asset-reference-contract.md](asset-reference-contract.md) 写入每项资产的 `reference_ids`、已有图片的 `file` 和正文 `@P#` 标记。默认 `file` 使用相对 HTML 的图片路径（如 `../P1.png`），不内嵌 Base64；构建前图片应已位于对应位置；执行 `validate_project_data.py - --asset-root <输出目录>` 可同时检查文件存在。H3 shots.references 不承担生图资产之间的连线含义。

## 资产正文质量

`assets[].prompt_en` 与 `prompt_zh` 均为完整提示词，不能把中文字段填成摘要。正式写作按 [asset-prompt-quality.md](asset-prompt-quality.md) 逐项核对参考分工、单一静态状态、构图与交互、资产类型适配及双语一致性。该语义检查由写作者执行，不由现有结构校验器代替。
