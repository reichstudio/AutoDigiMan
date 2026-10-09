# Free 版生产页数据契约

三页由同一份 `project-manifest.json` 生成。复制 `assets/project-manifest.template.json` 后填写项目数据，先运行校验器，再运行页面构建器。

```json
{
  "title": "歌曲或项目名称",
  "subtitle": "可选页眉副标题",
  "page_titles": {
    "asset": "参考图片清单",
    "h3": "MiniMax H3 全片分镜提示词｜项目类型",
    "list": "分镜列表｜项目类型"
  },
  "master_audio": "绝对音频路径或空字符串",
  "audio_references": [
    {
      "id": "A1",
      "file": "绝对或相对音频路径",
      "role": "voice_timbre_reference | audio_reuse",
      "h3_label": "<Audio 1>",
      "speaker": "<Subject 1> (S1)"
    }
  ],
  "master_duration_seconds": 0,
  "performance_ratio_note": "已确认的表演/剧情比例或临时说明",
  "assets": [
    {
      "id": "P1",
      "asset_id": "用户提供图片的资产名",
      "name": "参考图名称",
      "kind": "locked",
      "use": "在 H3 中的用途"
    }
  ],
  "shots": [
    {
      "id": "H3-001",
      "range": "00:00:000–00:06:400",
      "section": "段落",
      "title": "分镜名称",
      "mode": "sing | group | dance | duet | narrative | hold",
      "performer": "演唱、口播、舞蹈成员或剧情镜头",
      "audio_slice": "音频切片或临时口播区间",
      "lyrics": "精确歌词/台词，或 本段无歌词",
      "references": ["P1"],
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

## 约束

- `assets` 只包含用户提供的可用参考图，`kind` 为 `locked` 或 `provided`；不包含 `generated` 条目，也不填写图片生成提示词。
- `range` 使用 `MM:SS:ddd–MM:SS:ddd`。每个镜头最多九个 `references`；本地 `<Picture N>` 按数组顺序推导。
- `audio_references` 的 `A#` 是项目级音频 ID，`h3_label` 是本镜 H3 的 `<Audio N>` 标签。音色参考必须在 `subject_definitions` 单独定义 `<Audio N>` 并绑定 `<Subject N> (Sx)`，`summary` 使用 `audio reference`，`retention_analysis` 使用 `reference`；只有复制音频信号时才使用 `audio reuse` 与 `fully_copy` 或 `partially_copy`。
- 每个 `lyrics` 必填；无歌词填写精确文本 `本段无歌词`。
- 三个 `page_titles` 必填，分别用于参考图片清单、H3 页和中文分镜列表的浏览器标题与可见标题。
- 用户可见项目输出只生成三份 HTML；不输出 Markdown 文件。

## 命令

```powershell
py -3.12 C:\Users\wangfan\.codex\skills\feihou-mv-storyboard-prompts-free\scripts\validate_mv_manifest.py F:\项目\project-manifest.json
py -3.12 C:\Users\wangfan\.codex\skills\feihou-mv-storyboard-prompts-free\scripts\build_mv_pages.py F:\项目\project-manifest.json F:\项目\视频制作包
```
