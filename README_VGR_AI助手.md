# VGR PRO AI 助手

这个仓库只管理代码、测试和 AI 生成的项目文档，不纳入你的业务数据、达人话术原稿和运行输出。

## 当前能力

- 读取 `个人达人建联表.xlsx`
- 判断达人当前合作阶段、优先级、是否需要寄样、是否属于老达人复投
- 生成英文跟进消息建议
- 输出 CSV、Markdown 跟进清单和本地 HTML 看板

## 项目结构

```text
vgr_ai_assistant.py        # 兼容入口，保留原有启动方式
vgr_assistant/             # 核心代码
tests/                     # 单元测试
docs/                      # AI 生成的设计、计划、说明文档
run_vgr_ai_assistant.bat   # Windows 启动脚本
```

## 代码模块

- `vgr_assistant/models.py`
  放数据结构和状态常量。
- `vgr_assistant/analysis.py`
  放达人阶段识别、授权分类、优先级判断和 Excel 读取。
- `vgr_assistant/messaging.py`
  放英文消息生成逻辑。
- `vgr_assistant/dashboard.py`
  放 HTML 看板渲染。
- `vgr_assistant/reporting.py`
  放 CSV、Markdown、HTML 文件输出。
- `vgr_assistant/cli.py`
  放命令行入口和分析流程编排。

## 运行方式

双击运行：

`[run_vgr_ai_assistant.bat](C:/Users/Latop/Desktop/VGR%20PRO/run_vgr_ai_assistant.bat)`

命令行运行：

```powershell
C:\Users\Latop\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe `
  C:\Users\Latop\Desktop\VGR PRO\vgr_ai_assistant.py analyze `
  --output-dir C:\Users\Latop\Desktop\VGR PRO\outputs
```

单独生成英文消息：

```powershell
C:\Users\Latop\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe `
  C:\Users\Latop\Desktop\VGR PRO\vgr_ai_assistant.py message `
  --intent "提醒他尽快申请样品，语气轻一点，顺便说我们会尽快审核" `
  --stage "待申请样品" `
  --whatsapp
```

## Git 边界

默认不纳入版本管理：

- `数据表/`
- `达人建联话术/`
- `outputs/`
- `__pycache__/`
- `node_modules/`

如果你后续要把某些 AI 生成文档长期保留，直接放进 `docs/` 即可。
