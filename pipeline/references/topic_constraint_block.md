# HARD TOPIC CONSTRAINT block

This is the on-topic guardrail. It must be injected into the user message of any LLM call that produces or revises paper content (stages 16, 17, 19, and review stages 18, 24). The pipeline's stage-prompt templates that take a `{topic_constraint}` placeholder fill it from this file.

---

## The block (verbatim)

```
=== HARD TOPIC CONSTRAINT ===

The paper MUST be about: {topic}

PROHIBITED content (unless user explicitly specifies case-study mode):

- Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution.

- Do NOT present debugging logs, system errors, or configuration issues as experimental findings.

- Do NOT drift to tangential topics not directly related to the stated topic.

- Every section MUST connect back to the core research question.

- The Abstract and Introduction MUST clearly state the research problem derived from: {topic}

- The Method section MUST describe a technical approach, not a workflow.

- The Results section MUST report quantitative outcomes of experiments, not environment status.

=== END CONSTRAINT ===
```

---

## Why this matters

LLMs writing about ML research, when given vague guidance, drift into one of two ditches:

1. **Workflow narration** — "First we set up the environment, then we encountered an error, then we resolved it..." — and present this as the paper's contribution.
2. **Tangent escalation** — the paper starts about "few-shot tabular classification" and three sections later is mostly about "transformer attention patterns".

The constraint block is short and explicit so the model rejects both failure modes before they enter the draft.

## When NOT to use this block

If the user explicitly says they're writing a **case study** (e.g. "this paper is *about* the engineering process of deploying a model in production at company X"), the prohibitions become wrong. In that case, omit the block from the prompt or replace the prohibited list with case-study-appropriate guardrails.

This is a rare exception — confirm with the user before opting out.
