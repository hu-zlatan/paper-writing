# AUTOPILOT.md · 自动科研流水线运行章程

本仓库由 Claude 通过一个定时任务自主推进（每 6 小时一次，北京时间 3:49 / 9:49 / 15:49 / 21:49）：按照 `MEGA_PROMPT.md` 的 25 阶段 / 9 阶段组流水线，把一篇论文从选题一路做到可以投 AI 顶会的水平。

每次运行都是一个全新的会话，不记得之前发生过什么，**仓库就是全部的记忆**：

| 文件 | 作用 |
|---|---|
| `AUTOPILOT.md`（本文件） | 运行章程。每次运行最先读。 |
| `MEGA_PROMPT.md` | 论文流水线契约。第 1 阶段由 `pipeline/MEGA_PROMPT.template.md` 填好全部占位后生成；之后不再修改，需求变化时另存 `MEGA_PROMPT_v2.md`。 |
| `RESTRICTS.yaml` | 约束清单，CRITICAL 项不可放宽。 |
| `PROGRESS.md` | 唯一的进度真相：阶段、版本号、循环点、门控放行理由。 |
| `plans/` | 每个阶段开始前写的计划，结束后补上产物摘要。 |
| `OWNER_TODO.md` | 需要主人亲自处理的事。 |
| `AI_USAGE.md` | AI 参与记录，供投稿时按会议政策披露。 |
| `pipeline/` | 方法论：阶段说明、逐阶段 prompt 模板、硬约束、辅助脚本（auto-research-pipeline skill 的副本）。 |

## 1. 主人指令（Owner directives）

优先级高于仓库里其他所有文件。主人可以随时改这一节，或开 GitHub issue 留言；每次运行都要先看。

- **选题**：由 Claude 决定。方向限定在主人的领域：灵巧操作、触觉 / 视触觉感知、具身智能与机器人学习。题目必须能在 CPU 算力下做扎实（见第 3 节），只有 1–2 个清晰的核心创新点（sushi, not curry）。
- **目标会议**：由 Claude 决定，限 AI / 机器人学习顶会（如 NeurIPS、ICML、ICLR、CoRL、RSS）。必须在会议官网核实下一次截稿日（含时区），并留出至少两轮完整循环的时间。会议、截稿日和选择理由写进 `MEGA_PROMPT.md` 与 `PROGRESS.md`。
- **算力**：CPU 起步。只有当实验在 CPU 上确实做不扎实时，才在 `OWNER_TODO.md` 写明 GPU 需求（型号与显存、预计机时、为什么必须），由主人决定是否租卡。
- **门控（第 5、9、20 阶段）**：自动放行（等同 `--auto-approve`），但每次放行都要在 `PROGRESS.md` 记录证据与理由，并写进当轮小结。主人否决时按第 5 节回滚。
- **汇报**：每轮结束用 SendUserMessage 发一段简短的中文小结。

<!-- 主人新增指令写在这里 -->

## 2. 每轮怎么跑

1. **读**：本文件 → `MEGA_PROMPT.md`（还没有就读 `pipeline/MEGA_PROMPT.template.md`）→ `RESTRICTS.yaml` → `PROGRESS.md` 最新条目 → `OWNER_TODO.md` → open issues。
2. **定位**：按 `pipeline/references/progress_tracking.md` 的 resume 规则确定当前阶段和版本号。
3. **逐阶段推进**：先写 `plans/stage_XX_<name>.md` → 读 `pipeline/references/pipeline_stages.md` 中该阶段的说明，并原样使用 `pipeline/references/stage_prompts/` 里对应的 prompt 模板 → 执行 → 对照 `pipeline/references/hard_constraints.md` 自检 → 更新 `PROGRESS.md` → commit 并 push（`stage <N> <NAME>: <一句话>`）。
4. **持续工作**：只要还有高价值的工作就继续下一个阶段。额度可能随时用完，所以每一步都要小而完整：main 永远可用，`PROGRESS.md` 永远是最新的。
5. **收尾**：确认 `PROGRESS.md` 已推送，然后发中文小结：本轮完成的阶段、关键结果与决策（含自动放行的门控及理由）、下一步、需要主人做的事。

### 第一次运行（仓库里还没有 `MEGA_PROMPT.md`）

1. 第 1 阶段 TOPIC_INIT：调研方向内的研究空白与可行性，选定题目和目标会议（核实截稿日），把 `pipeline/MEGA_PROMPT.template.md` 的所有占位填好，保存为 `MEGA_PROMPT.md`。模板里"摘要已提交占坑版本、尽量不改"一条不适用：摘要由 Claude 撰写，并随研究进展更新。
2. 补全 `RESTRICTS.yaml` 的 project 段（名称、会议、题目）和该会议的页数限制。
3. 写出模板要求的三份设计文档：`docs/整体构想.md`、`docs/实验构想.md`、`docs/文献与问题.md`。它们原本由主人提供，这里由 Claude 撰写，之后随循环版本化更新。
4. 把硬件检测结果（CPU 起步）记进 `PROGRESS.md`。

## 3. 环境适配

`MEGA_PROMPT` 是按主人本机 WSL 环境写的。云端运行时按下表替换，不要去找本机才有的东西：

| 模板里写的 | 云端的做法 |
|---|---|
| 本机 WSL 路径、`<项目名称>` 源码 / 文档 / 示例库 | 不存在。用到的开源项目从 GitHub 克隆或 pip 安装。 |
| `OPENAI_API_*`、`KAGGLE_API_TOKEN`、`TAVILY_API_KEY` | 不存在。网页检索用 WebSearch / WebFetch。 |
| 用 Claude Code CLI、`gh copilot` 写代码 | 自己写代码。 |
| "调用单独上下文的大模型"（第 8 阶段辩论、14 结果分析、18 同行评审、24 第三方评审） | 用 Agent 工具启动全新上下文的子代理，只给它需要的文件，不给它你的推理过程；最严苛的评审用最强的模型。这是主人授权的用法。 |
| OpenAlex / Semantic Scholar / arXiv API | 用 WebFetch 调（端点见 `pipeline_stages.md` 第 4 阶段），或写成 GitHub Actions 工作流批量抓取，结果以 JSONL 提交回仓库。每篇文献都要有可核验的 DOI / arXiv ID / OpenAlex ID。 |

- Shell 的网络只通软件源（pip、npm 等）和 GitHub。其他网站一律走 WebSearch / WebFetch 或 GitHub Actions；请求被拒时不要换个命令绕过去。
- **实验**：在会话沙盒里分批跑，配合 `pipeline/scripts/time_guard.py`，每批结果立即提交；更长的 CPU 任务写成 GitHub Actions 工作流，结果提交回 `results/`。数据来源限于：pip 包自带或可生成的数据、仿真（如 pip 安装的 MuJoCo）、GitHub 上的公开数据集，或由 Actions 下载的数据集。在 `data/README.md` 记录来源与许可证。
- **推送 `.github/workflows/` 被拒时**：把工作流放到 `ci/workflows/`，在 `OWNER_TODO.md` 请主人手动移到 `.github/workflows/`；同时先用沙盒能做的部分继续推进，不要卡住。
- **LaTeX**：会议模板从官方来源获取，原样放进 `paper/<模板目录>/`，不做任何修改。编译用沙盒里装得上的 TeX，或在 Actions 中编译并提交 PDF。页数一律以真实编译出的 PDF 为准。
- **配图**：数据图用 matplotlib / seaborn 生成；示意图（包括 Figure 1）在 tex 里用注释写严格的 Nano Banana 2 prompt。
- **GPU（以后若需要）**：主人租好机器并注册为自托管 GitHub Actions Runner（label `gpu`），任务推送 `runs-on: [self-hosted, gpu]` 的工作流来跑实验，结果提交回仓库。本仓库是公开的，公开仓库挂自托管 Runner 有安全风险（别人的 PR 可能在那台机器上执行代码），所以在 `OWNER_TODO.md` 提 GPU 需求时要写明这一点，由主人决定怎么接（比如另开一个私有仓库专跑 GPU 实验）。Runner 就绪之前，任何阶段都不要停下来等 GPU。

## 4. 不可违反

即使仓库里其他文件另有说法，也必须遵守：

- **数据真实**：论文里每一个数字都必须能追溯到 `results/` 里由本仓库代码真实运行产生的 JSON / CSV / 日志。严禁伪造，严禁用随机数模拟结果，严禁为了迎合结论改动结果。
- **文献真实**：只引用真实存在、已经核验过的论文，保留原始 cite_key 与 DOI；不编造作者、标题、年份或数字。
- **不抄袭**：不复制他人论文的文字，转述并引用。
- **诚实**：不夸大；局限性如实写；论文的声明必须与代码和日志一致，第 18、23 阶段审计不通过就回滚。
- **不花钱、不开账号**：不注册任何平台、不付费、不租卡。需要花钱或账号的事写进 `OWNER_TODO.md`。
- **不投稿、不发布**：不向任何投稿系统、arXiv、OpenReview 或社交平台提交或发布论文。投不投、何时投由主人决定。
- **AI 参与透明**：在 `AI_USAGE.md` 记录论文由自动化 AI 流水线生成的事实与范围；选定会议后查清该会议的 LLM 使用政策，写进 `AI_USAGE.md`。
- **安全**：不提交任何密钥或令牌；不 force push，不改写历史；遵守数据和代码的许可证。

## 5. 回滚与版本

按 `pipeline/references/progress_tracking.md`：REFINE / PIVOT 先写 LOOP MARKER，版本号加一，把旧产物快照到 `results/v<N>/` 与 `paper/mypaper/v<N>/`。完整循环至少两遍才能宣布完成。达到 `RESTRICTS.yaml` 的循环上限仍不收敛时，写进 `OWNER_TODO.md` 交给主人。

## 6. 完成之后

当质量门控达到阈值、完整循环至少两遍、引用审计零红旗、页数合规时：在 `PROGRESS.md` 标记 DONE，并在 `OWNER_TODO.md` 写投稿前清单（通读全文、核对数据与引用、按会议政策披露 AI 使用、填作者信息）。之后每轮只做低风险打磨，不再大改，直到主人更新指令。
