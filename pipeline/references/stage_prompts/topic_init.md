# Stage 1 — TOPIC_INIT

## Purpose
Turn a topic string into a SMART research goal in markdown.

## Mode
- LLM: strongest model.
- json_mode: false.
- max_tokens: default.

## Prompt template

**System:**
```
You are a rigorous research planner.
```

**User:**
```
Create a SMART research goal in markdown.

Topic: {topic}

Domains: {domains}

Project: {project_name}

Quality threshold: {quality_threshold}

Required sections: Topic, Scope, SMART Goal, Constraints, Success Criteria, Generated.
```

## Placeholders to fill

- `{topic}` — the research topic, one sentence.
- `{domains}` — comma-separated list (e.g. "ML optimization, neural networks, federated learning").
- `{project_name}` — the project's directory name (no trailing `-paper`).
- `{quality_threshold}` — usually 7.5 for top-tier conferences.

## Output

Save to `docs/00_topic_init.md`. Verify all 6 required sections are present before moving on.
