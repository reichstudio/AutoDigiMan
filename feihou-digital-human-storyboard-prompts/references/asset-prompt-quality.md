# 资产提示词：画面定义与双语质量

正式编写或修改生图资产提示词前阅读本文件。以下是本技能的制作标准，不是模型厂商的接口保证。适用于所有执行模型；不通过强制切换模型、堆画质词或规定统一字数解决质量问题。

## 先决定这张图到底是什么

每张资产在内存中先明确：服务的镜头、参考来源各自提供什么、目标构图、唯一的可见状态、必须看清的部位。然后写成自然语言段落，不将这份规划另存为确认文件或塞入提示词管理字段。

- **引用有分工**：如“@P1 提供人物身份与制服，@P4 提供座椅、织带与锁扣结构”。指出要保留的可见特征及本次变化；不要只说“参考已有图片”“保持一致”。不知道的结构不能假称在参考图中可见。
- **一张静态图对应一个时刻**：明确是动作前准备态、中途瞬间、完成态，还是纯身份/环境参考。不能让一张单幅图同时完成插入、拉紧、解开。连续动作留给 H3；用户明确要求多格步骤图时才做多格，并逐格定义状态。
- **从后续用途选择状态**：供“收桌板”动作起始参考时应显示打开的桌板；供“收好后检查”时应显示已收起。不能只因终态更整洁就改变已确认的资产用途。
- **明确构图边界**：写出景别、视角、画面裁到哪里、主体位于哪里、哪些关键部位完整入画。焦段仅在确有取景意义时写；“35 mm、4K、电影感”不能代替构图。
- **具体交互**：涉及手与道具时写清哪只手握哪一部分、掌指接触点、部件朝向及相互位置。需要区分时分别使用“人物的右手”和“画面左侧”。间距可用清楚的相对关系，避免无依据的毫米精度。
- **空间可实现**：近景不能兼得不在视线内的远端出口；收起的桌板不充当水平操作台；遮挡关键机构时应调整手位或视角。保留实际空间，不为展示所有要点而凭空扩大座椅间距。

## 依资产类型选择细节

| 类型 | 必须明确的画面信息 | 不要机械附加 |
|---|---|---|
| 人物身份/主讲姿态 | 身份来源、可见服装特征、表情视线、手位、身体裁切、人物与背景位置 | 不可见的鞋子细节、无依据的年龄或新配饰 |
| 手部与机构近景 | 零件结构来源、一个明确状态、左右手接触点、开合/扣合关系、清楚可见的操作部位、材质 | 与画面无关的面部毛孔、完整全身装束 |
| 环境与操作区 | 前中后景、相机所在方向、设备位置、可用动作区和通路、被保留的地理关系 | 空间不支持的视线、必不可少却被裁掉的通道 |
| 示意图/平面图 | 图形数量、相对位置、方向、标记与图例、二维或三维形式、文字、视觉层级 | 人物皮肤、五指、发丝轮廓光、摄影景深；确有立体渲染需求才描述照明 |
| 手机/卡片/界面 | 屏幕或卡片朝向、可读区域、精确标题、开关当前状态、手指是否遮挡、反光控制 | 未确定的密集文字、只说“清楚的图标”却不说明其状态 |

照片类布光根据当前构图写主光方向与软硬、必要补光及材质高光控制。只有可见且有用的分离光才写。不能给所有资产复制相同的皮肤、金属、五指、窗光和轮廓光尾段。保持统一风格不等于使用同一段无差别描述。

## 中英文都是完整可执行稿

先完成其中一种语言，再逐项对齐另一种语言。中文不是英文摘要；两栏独立复制后应得到相同的主体、参考分工、构图、状态、交互、光色及画面文字。

- 相同 `reference_ids` 与 `@P#`；相同左右关系、机位、裁切、开合状态、文字和尺寸。
- 允许自然表达差异，不要求逐字直译；不允许一栏省去另一栏的关键画面条件。
- 写实照片英文使用 `photorealistic`，中文说明写实摄影质感；示意图按自己的媒介描述。
- 分辨率写为 `3840×2160` 或 `3840x2160` 等项目指定规格，不能拼成 `38402160`；目标交付规格不等于承诺接口一定支持该尺寸。
- 需要渲染的文字，两栏都使用英文双引号包住相同原文。`@P#` 是参考标记，不是要印在图上的文字。
- 提示词中不夹带资产 ID 标题、优先级、服务镜头清单、生成状态或复制说明；这些保留在资产卡管理信息中。

## 写法对照

### 手部机构图：从动作概述改为可见状态

不足：“生成安全带特写，空姐插入锁扣并拉紧，机构清楚、五指自然、4K。”

问题：混合两个动作阶段，未说明取景、手位、扣合程度和参考来源。下面以“插入前准备态”为例；实际状态以已确认资产清单为准。

中文成稿：

> 在 @P4 的蓝色客舱座椅环境中，拍摄 @P1 空姐下肋至大腿上部的正面近景，人物身份及可见的印花衣袖、深蓝裙装沿用 @P1，织带与抬扣式锁扣结构沿用 @P4。安全带处于尚未扣合的准备状态：人物右手在画面左侧握住金属插片的后端，左手在画面右侧托稳锁扣外壳，插片前端对准锁扣入口并留出清楚间隙。双手、完整插片、锁扣入口和两侧带身均在画内，手指避开接合处，五金正面略朝镜头。采用写实培训片摄影，焦点落在接合机构，背景座椅轻微柔化。画面左侧柔和窗光照亮手背与织带，右侧弱反射补光保留锁扣内侧层次，金属高光清楚而不遮盖结构；深蓝织带、银色五金和原制服色彩保持一致。单张 16:9 横版参考图，目标规格 3840×2160。

English:

> In the blue passenger-seat setting from @P4, photograph a frontal close view of the attendant from @P1, cropped from the lower ribs to the upper thighs. Retain her identity and the visible patterned sleeves and navy skirt from @P1, using @P4 for the webbing and lift-lever buckle structure. The belt is in an unfastened preparation state: her right hand at frame left grips the rear end of the metal tongue, while her left hand at frame right supports the buckle housing. The tongue tip aligns with the buckle opening across a clearly visible gap. Include both hands, the complete tongue, the buckle opening and webbing on both sides; fingers leave the connection point visible, with the hardware face angled slightly toward the lens. Use photorealistic training-production photography, focusing on the connection mechanism with the seat background gently softened. Soft window light from frame left illuminates the backs of the hands and the webbing; weak bounce fill from frame right retains detail inside the buckle. Controlled metal highlights preserve its structure. Keep the navy webbing, silver hardware and original uniform colors consistent. Create one 16:9 landscape reference image for a 3840×2160 target deliverable.

### 示意图：明确结构，不套用人像摄影尾段

仅当已确认文稿与布局要求为四出口时使用本示例；不能从单张舱门照片推断整架飞机出口数。

中文成稿：

> 绘制单张 16:9 横版二维客舱位置示意图。@P2 仅提供蓝色座椅与浅灰内饰配色，@P3 仅提供红色出口标记样式；出口数量与位置采用本项目已确认的四出口布局。客舱长轴在画面中由上至下，中央一条过道分开两侧座椅组，四个红色出口分别位于前左、前右、后左、后右，并与座椅符号留有明确间隔。上端标注 "前部"，下端标注 "后部"，每个出口标注 "EXIT"。用浅象牙色底、深蓝座椅符号与红色出口建立清楚层级，线宽一致，文字横向正读。正交俯视、图形边界锐利，目标规格 3840×2160。

English:

> Create one 16:9 landscape, two-dimensional cabin-location diagram. Use @P2 only for the blue-seat and light-gray interior palette and @P3 only for the red exit-marker styling; take the exit count and positions from this project's confirmed four-exit layout. The cabin's long axis runs vertically, with a central aisle separating two seat banks. Place four red exit markers at the front-left, front-right, rear-left and rear-right, clearly separated from the seat symbols. Label the upper end "前部", the lower end "后部", and each exit "EXIT". Establish a clear hierarchy with an ivory background, navy seat symbols and red exits; keep line weights consistent and all lettering upright and horizontally readable. Use an orthographic top view with crisp graphic boundaries, targeting 3840×2160.

## 提交前逐项自检，失败则改写本资产

1. 不看卡片标题，只读任一栏正文，能否判断主体、用途对应的可见状态和构图？
2. 能否据文字画出主体位置、手部接触点与关键部件关系？没有交互的资产不强加手部要求。
3. 是否把连续动作、互斥状态或多个不相容机位塞入一张静态图？
4. 两种语言是否同样包含参考分工、状态、机位、关键细节、适用的光色和文字？逐项比对，不以字数相近代替语义检查。
5. 是否有删除后完全不影响该图的通用尾段，或与资产类型冲突的皮肤、手指、布光描述？有则删改。
6. `@P#` 与 `reference_ids` 是否一致，尺寸、左右方向、文字和文件引用是否准确？

这是语义审核，不宣称现有结构校验器能够判断画面质量。现有脚本验证数据、路径和引用；写作者仍需完成上述自检。技能修订时只审阅示例，不自动改写用户未授权修改的历史页面。
