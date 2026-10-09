# 资产页与无限画布的引用协议

项目数据继续内联在 HTML 的 `dh-project-data` 中，不新增项目 JSON 文件。默认图片使用相对 HTML 的路径，直接指向用户现有图片位置。用户只拖入 HTML，不需要粘贴目录路径或拖入整个文件夹。

```json
{
  "assets": [
    {"id": "P1", "name": "已有产品图", "kind": "locked", "file": "../P1.png", "original_file": "P1.png", "reference_ids": []},
    {"id": "P2", "name": "已有人物图", "kind": "locked", "file": "../P2.jpg", "original_file": "P2.jpg", "reference_ids": []},
    {
      "id": "P3", "name": "人物手持产品", "kind": "generated", "reference_ids": ["P1", "P2"],
      "prompt_zh": "保持 @P1 的产品外观以及 @P2 的人物身份与服装，呈现人物手持产品。",
      "prompt_en": "Preserve the product appearance from @P1 and the person's identity and clothing from @P2. Show the person holding the product."
    }
  ]
}
```

- `id` 是唯一、稳定的 P#，共享图片复用同一编号。
- `file` 为相对资产 HTML 的真实图片路径，使用 `/`，例如 `../P1.png`；可用 `original_file` 记录源文件名。默认不使用 Base64。
- 直接引用现有图片，不复制或移动图片，也不新建素材目录。用相对 HTML 的路径（可通过 `../` 指向父目录），避免绝对路径；校验时解析到实际文件。待生成且没有文件的资产省略 `file`，不编造图片。移动制作包时保持 HTML 与参考图片的相对位置。
- `reference_ids` 是有序图片引用列表，也是未来画布导入器的连线依据。无引用时明确写 `[]`。旧 `source_refs` 转为此字段，不保留两份可能冲突的依赖列表。
- 两种语言正文均使用 `@P#` 说明每张参考图的角色，出现的编号集合必须与列表一致。顺序由 `reference_ids` 决定，正文可以按自然语言组织，避免残留含糊的“图1 / Image 1”。资产自身编号只出现在卡片管理信息中，除非确实引用自身；自身引用属于循环，应拒绝。
- 待生成上游可以被下游引用，但页面须显示“待生成上游”；先生成、检查上游，再上传给下游。不能把它表示为已存在的图片。
- 拒绝重复 ID、未知引用、自引用/循环引用、正文与列表不一致；构建时检查 `file` 对应图片实际存在。
- 卡片显示相对路径与图片预览、引用顺序和可跳转的来源资产名称。中英文复制按钮复制完整正文，包括 `@P#` 和引号。提示词不放入未正确转义的 HTML 属性。
- H3 的 `shots.references` 与局部 `<Picture N>` 仍按分镜上传顺序使用；本协议的 `reference_ids` 只描述生图资产的依赖。

## 导入能力边界

用户只拖入 HTML；本地画布导入器需要取得该 HTML 的来源目录，以此解析 `file` 相对路径，读取图片后依据 `reference_ids` 连线，并将正文 `@P#` 映射到画布节点。导入动作不要求粘贴文件夹路径或拖入整个文件夹。

HTML 和技能负责输出引用协议，不修改或假称已实现画布导入器。普通浏览器的拖放 File 对象不保证提供来源目录读取能力；仅能读取 HTML 文本的导入器还需接入本地宿主的路径和文件读取能力。页面预览能够显示图片不等于画布导入已经成功。
