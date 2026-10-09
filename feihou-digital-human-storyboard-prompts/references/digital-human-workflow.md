# Digital-Human Presenter Workflow

Use this reference for every project this skill handles: a visible presenter speaking a locked script, tutorial, interview, explanation, commentary, or narration. Planning stays speech-led; singing, dance, lyric cards, and beat analysis belong to the separate music-video skill.

## Foundation rules (always apply)

- Read the official generic H3 prompt-writing skill and the selected mode guide first. With uploaded pictures or voice references, use Ref2VA and retain its six official fields and label semantics.
- Inspect each supplied image before describing it. `P#` is the project asset ID; `<Picture N>` is the shot-local upload position. Map them in upload order and cite visual references where they appear.
- Keep the supplied script verbatim, use a stable speaker ID, put performed words only in `<d>[Language] ...</d>`, and keep every `<Audio N>` separate from visual subjects.
- Treat all transitions as concrete visual decisions. Tie lenses, camera routes, action state changes, and cut times to what the viewer can see.
- Keep pages self-contained and ensure that the rendered copy button returns the entire prompt string.

## What is specific to a digital presenter

1. **Speech sets the pacing.** Use user-provided recorded-voiceover duration and cue times when available; otherwise mark boundaries `预估` and derive them from the scenario's speaking-rate tier (fast 240–260, medium 200–240, steady 160–200 chars/min, per scenario-rules.md; IP-replication takes the measured rate from reference-video analysis). Timing and script text come from the user as locked inputs; the pacing source is speech density.
2. **Make the supplied environment operational.** For every scene reference, identify concrete visible anchors—such as a desk, screen, console, corridor, cabinet, door, seating, or display—and give the presenter a plausible, simple interaction or route using those anchors. Preserve the scene's actual viewpoint, layout, equipment, and spatial depth in the prompt body; scene images are not merely lighting or mood references.
3. **Design body performance with the framing.** Choose wide, full-body, medium, and close shots according to the action and information being delivered. A close view suits facial emphasis; a wider view suits walking, object use, or environmental interaction. Match the framing to the point being delivered.
4. **Use economical spoken-action choreography.** Give each unit a small, legible progression: a route or interaction, a few natural gestures tied to the spoken point, and an outcome/next-state. Keep gesture lists, lighting paragraphs, and preservation language to what affects generation.
5. **Treat internal cuts as the default framing change.** Target 10–15-second H3 units approaching the 15-second cap, with duration following content; keep each unit a single continuous shot by default and realize framing, camera, or scene changes through `[Shot N] At MM:SS.mmm` internal cuts. Fast-cut style is a cut-density choice, not shorter units: for e-commerce projects, confirm with the user between normal pacing (1–2 internal cuts per unit) and fast cutting (a dense internal cut every 2–3 seconds inside the same ~15-second unit), and record the choice in `pacing_style`. State whether dialogue and lip sync continue across the cut.
6. **Write chronological prompt prose, not appended warnings.** State reference-derived composition, movement, interaction, speaking, and cut result in playback order. Describe a final visual state naturally as part of the last action. Prompt bodies consist of direct target statements.
7. **Audio roles stay precise.** For a voice-timbre file, use a standalone line such as `<Audio 1> is the voice-timbre reference for <Subject 1> (S1), sourced from "filename.mp3".` Use `[reference generation + audio reference]` and `<Audio 1>: reference` when timbre/delivery guides the target voice; use an audio-reuse relationship when the signal itself is copied. Each H3 unit carries at most three `<Audio N>` entries.

## 真人IP复刻的参考视频分析

用途为真人IP复刻时，先从用户提供的参考视频中提取讲者特征，再动笔分镜与提示词：

- **外观**：脸型与发型、常用着装与配饰、体态与站姿；
- **动作习惯**：手势幅度与频率、标志性手势、头部与肩部动作、走位范围；
- **表情与眼神**：讲话时的表情变化、眼神方向（直视镜头或交流感）；
- **语速与节奏**：平均语速、停顿习惯、语气起伏与强调方式；
- **镜头习惯**：常用景别、与镜头的距离关系。

分析结论写入讲者主体定义（外观与体态特征）与表演描述（动作、表情、语速）。H3 上传时按官方规则引用参考视频：复用可见内容（人物、动作）在 `<Subject N>` 定义内引用视频来源；镜头运动或节奏结构参考以 `<Video N>` 标注；`retention_analysis` 按实际保留程度给出 `fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`。用户以多角度考图加文字描述替代视频时，走简化复刻方案并在交付中注明与视频复刻的差异。

## Deliverable language and page behavior

- The English H3 pane is the copy-ready official prompt and remains in English except for the locked dialogue inside `<d>`.
- The Chinese pane is a working translation: retain required H3 field names and reference tokens, and write all descriptive prose in Chinese.
- For a spoken-video project, write `non_diegetic_music:` followed by `N/A.` unless the user requests a score; a requested score is described as audience-only music.
- Use `本段口播` or `本段台词` as the speech row label on review pages.
- When a prompt is stored in an HTML attribute for copy, escape `&`, `<`, `>`, `"`, and `'`, or use a text-node/clipboard source that preserves the full string. Test a rendered copy button with a prompt containing dialogue quotes and `<Audio 1>` before delivery.

## Review checklist

- Every prompt body identifies the actual scene-reference composition and visible anchors, together with palette or atmosphere.
- Presenter framing, movement, prop/surface interaction, and gestures serve the spoken point.
- Internal cuts have valid local timestamps, a visual reason, and explicit speech/lip-sync continuity when speech crosses them.
- The Chinese prose reads as fully translated narrative; a no-score spoken unit uses `N/A.`.
- Prompt prose is concise and reproducible; each constraint in it earns its place by affecting generation.
- All timing is user-supplied or clearly labeled `预估`, and the basis is stated in the delivery notes.
