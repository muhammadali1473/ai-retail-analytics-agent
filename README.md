# Retail Analytics Copilot

A fully local AI agent that answers retail analytics questions by combining RAG over local markdown documents and SQL execution over a Northwind SQLite database.

## Setup

1.  Install dependencies: `pip install -r requirements.txt`
2.  Ensure Ollama is running with `phi3.5:3.8b-mini-instruct-q4_K_M`.
3.  Create database views:
    ```bash
    python create_views.py
    ```

## Optimization

To optimize the DSPy modules (e.g., SQL Generator), run:

```bash
python optimize_dspy.py
```

This will run the BootstrapFewShot optimizer and report results.

## Usage

Run the agent with the evaluation file:

```bash
python run_agent_hybrid.py --batch sample_questions_hybrid_eval.jsonl --out outputs_hybrid.jsonl
```
