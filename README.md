# paper-writing

An experiment in autonomous research: every 6 hours, Claude (Anthropic's AI model) advances a 25-stage research pipeline on this repository — choosing a topic, reviewing the literature, writing and running experiments, analysing results and drafting a paper — aiming for the standard of a top AI conference submission.

一个自主科研实验：Claude 每 6 小时在这个仓库上推进一次 25 阶段的科研流水线——选题、文献调研、写代码跑实验、分析结果、撰写论文，目标是达到 AI 顶会的投稿水平。

- **Progress / 进度**: [`PROGRESS.md`](PROGRESS.md)
- **How the runs work / 运行章程**: [`AUTOPILOT.md`](AUTOPILOT.md)
- **The pipeline / 流水线方法论**: [`pipeline/`](pipeline/)
- **AI involvement / AI 参与记录**: [`AI_USAGE.md`](AI_USAGE.md)

Everything here is produced by the AI pipeline unless noted otherwise. Every number in the paper must trace back to real runs of the code in this repository, and every citation to a verified, existing paper.

除特别说明外，本仓库内容均由 AI 流水线生成。论文中的每个数字都必须能追溯到本仓库代码的真实运行结果，每条引用都必须是核验过的真实文献。

## Layout / 目录

| Path | Contents |
|---|---|
| `docs/` | Stage artifacts: topic, problem tree, literature, synthesis, hypotheses, experiment plan |
| `code/` | Experiment code |
| `data/` | Experiment inputs and their provenance |
| `results/` | Structured results, logs, analyses and decisions, versioned per loop |
| `paper/` | Conference template and the manuscript |
| `plans/` | The plan written before each stage |
