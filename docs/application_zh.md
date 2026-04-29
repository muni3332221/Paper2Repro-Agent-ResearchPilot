# 中文申请表描述草稿

## 项目简介

我构建了 Paper2Repro Agent，一个面向科研论文复现的 AI Agent 工具。它能够读取论文 PDF，自动提取论文贡献、方法概述、数据集、baseline、评价指标、训练超参数和复现实验风险，并生成一套可执行的复现计划，包括 Markdown 报告、JSON 结构化结果、实验 checklist 以及 Python/PyTorch 项目骨架。

## 核心痛点

论文复现的主要困难不在于单纯阅读摘要，而在于实验细节分散在方法、实验、附录、表格和开源代码中。研究者通常需要花数小时手动整理模型结构、数据预处理、baseline、评价指标、训练参数和复现验证步骤。Paper2Repro Agent 将这些步骤拆成多 Agent 流程，降低从“读懂论文”到“开始复现实验”的准备成本。

## 核心逻辑流

1. PDF Parser 解析论文 PDF，提取标题、摘要、章节和正文。
2. Summary Agent 提取研究问题、核心贡献、方法概述、假设和局限。
3. Experiment Agent 识别数据集、baseline、指标、超参数、算力需求和实现注意事项。
4. Code Agent 根据论文内容生成复现实验项目骨架，包括 `requirements.txt`、`config.py`、`data.py`、`model.py`、`train.py` 和 `evaluate.py`。
5. Validation Agent 生成复现 checklist、预期产物和高风险项，帮助用户验证复现是否可信。
6. Reporter 输出 `repro_plan.md` 和 `repro_plan.json`，方便人工阅读、版本管理和后续自动化处理。

## 可量化成果

项目支持离线启发式模式和 LLM 模式。离线模式无需 API key，可以快速生成初步复现计划；LLM 模式预计每篇论文消耗约 5 万到 20 万 tokens，取决于论文长度和代码生成深度。对于一篇中等长度论文，工具可以将初步复现准备时间从数小时缩短到约 20 分钟，并使复现实验的任务拆解更结构化、可追踪、可提交到 GitHub。

## Token Plan

- PDF 解析与章节整理：0 tokens，本地完成。
- Summary Agent：约 1 万到 4 万 tokens。
- Experiment Agent：约 2 万到 8 万 tokens。
- Code Agent：约 1 万到 6 万 tokens。
- Validation Agent：约 5 千到 2 万 tokens。
- 总计：约 5 万到 20 万 tokens / 篇论文。

## 一句话版本

Paper2Repro Agent 是一个把科研论文自动转换为复现实验计划和代码骨架的多 Agent 系统，能够显著降低论文复现前期的信息整理成本。
