# TradingAgents CLI — Usage & Arguments

Complete reference for running the TradingAgents CLI, including every
command-line flag, the environment variables that configure a run, and where
output is written.

The CLI runs in two modes: an interactive wizard, or a non-interactive one-shot
driven by command-line flags.

## Invoking the CLI

```bash
tradingagents                            # installed command
python -m cli.main                       # run directly from source
docker compose run --rm tradingagents    # Docker (flags go after the service name)
```

All three accept the same options. Under Docker, put the flags **after** the
service name, e.g. `docker compose run --rm tradingagents --ticker SPCX`.

## Interactive mode

Run with no flags to launch the wizard. It walks through eight steps — ticker,
analysis date, output language, analyst team, research depth, LLM provider,
thinking models, and provider-specific reasoning — then streams the analysis and
prompts to save the report at the end.

```bash
docker compose run --rm tradingagents
```

## Non-interactive (one-shot) mode

Pass `--ticker` to run the whole pipeline unattended. Every step you do not set
with a flag (or a `TRADINGAGENTS_*` environment variable) falls back to its
default, no prompts appear, and the report is auto-saved.

```bash
# installed command
tradingagents --ticker SPCX --date 2026-06-28

# Docker
docker compose run --rm tradingagents --ticker SPCX --date 2026-06-28

# short forms
docker compose run --rm tradingagents -t SPCX -d 2026-06-28
```

## Command-line options

All options belong to the default command, so they work whether you call
`tradingagents`, `python -m cli.main`, or `docker compose run --rm tradingagents`.

| Flag | Short | Value | Description |
| --- | --- | --- | --- |
| `--ticker` | `-t` | symbol | Ticker to analyze (e.g. `SPCX`, `0700.HK`, `BTC-USD`). Passing it triggers the unattended run described above. |
| `--date` | `-d` | `YYYY-MM-DD` | Analysis date. Defaults to today. Cannot be in the future. |
| `--analysts` | `-a` | comma list | Analyst team to run: `market`, `social`, `news`, `fundamentals` (e.g. `-a market,news`). Omit for all available. Crypto tickers drop `fundamentals` automatically. |
| `--research-depth` | `-r` | depth | `shallow` (1), `medium` (3), `deep` (5) debate + risk rounds. A positive integer sets a custom count. Higher is more thorough but slower. |
| `--language` | `-l` | name | Output language for reports and the decision (e.g. `English`, `Chinese`, `Spanish`). Defaults to English. |
| `--checkpoint` / `--no-checkpoint` | | flag | Enable or disable checkpoint-resume (save state after each node so a crashed run can resume). Omit to honor `TRADINGAGENTS_CHECKPOINT_ENABLED`. |
| `--save` / `--no-save` | | flag | Save or skip the final consolidated report. Omit to auto-save in unattended `--ticker` runs, or to ask in interactive runs. |
| `--clear-checkpoints` | | flag | Delete all saved checkpoints before running (force a fresh start). |
| `--help` | | | Show all options and exit. |

Each of `--ticker`, `--date`, `--analysts`, `--research-depth`, and `--language`
also works on its own in interactive mode: providing one pre-fills that step and
skips its prompt, while the remaining steps still prompt. Only `--ticker` turns
the entire run unattended.

The provider, thinking models, and backend URL are not flags; set them with the
environment variables below (or pick them in the wizard).

### Accepted values

- **`--analysts`** — any comma-separated subset of: `market`, `social`
  (Sentiment), `news`, `fundamentals`. Order does not matter; duplicates are
  ignored. For crypto tickers, `fundamentals` is dropped automatically.
- **`--research-depth`** — `shallow` (1 round), `medium` (3 rounds),
  `deep` (5 rounds), or any positive integer for a custom debate + risk round
  count.
- **`--language`** — any language name the models understand
  (e.g. `English`, `Chinese`, `Japanese`, `Korean`, `Spanish`, `French`,
  `German`, `Arabic`, `Russian`, `Hindi`, `Portuguese`, or a custom name).

## Examples

```bash
# Full unattended run, all defaults except ticker
docker compose run --rm tradingagents -t AAPL

# Pick a subset of analysts and a deeper debate
docker compose run --rm tradingagents -t NVDA -a market,news,fundamentals -r deep

# Crypto, Chinese-language report, medium depth
docker compose run --rm tradingagents -t BTC-USD -l Chinese -r medium

# Historical date, fresh start (ignore any saved checkpoints)
docker compose run --rm tradingagents -t SPY -d 2026-01-15 --clear-checkpoints

# Run unattended but skip the final consolidated report tree
docker compose run --rm tradingagents -t SPY --no-save

# Pre-fill just the ticker but keep the wizard for everything else
docker compose run --rm tradingagents --ticker TSLA   # still unattended (— ticker triggers it)
```

## Configuration via environment variables

Any `TRADINGAGENTS_*` variable below overrides the matching default in
`tradingagents/default_config.py`. Set them in `.env` (Docker loads it
automatically) or export them in your shell. When one is set, the CLI also skips
the matching wizard step, which is what makes fully unattended runs possible.
A command-line flag, when given, takes precedence over the corresponding
variable for that run.

| Variable | Controls | Example |
| --- | --- | --- |
| `TRADINGAGENTS_LLM_PROVIDER` | LLM provider | `openai`, `glm`, `deepseek`, `ollama` |
| `TRADINGAGENTS_DEEP_THINK_LLM` | Deep-thinking model | `gpt-5.5`, `glm-5.2` |
| `TRADINGAGENTS_QUICK_THINK_LLM` | Quick-thinking model | `gpt-5.4-mini`, `glm-5-turbo` |
| `TRADINGAGENTS_LLM_BACKEND_URL` | OpenAI-compatible endpoint | `http://localhost:8000/v1` |
| `TRADINGAGENTS_OUTPUT_LANGUAGE` | Report language | `English`, `Chinese` |
| `TRADINGAGENTS_MAX_DEBATE_ROUNDS` | Bull/bear debate rounds | `1`, `3`, `5` |
| `TRADINGAGENTS_MAX_RISK_ROUNDS` | Risk discussion rounds | `1`, `3`, `5` |
| `TRADINGAGENTS_TEMPERATURE` | Sampling temperature | `0.0` |
| `TRADINGAGENTS_OPENAI_REASONING_EFFORT` | OpenAI reasoning effort | `low`, `medium`, `high` |
| `TRADINGAGENTS_GOOGLE_THINKING_LEVEL` | Gemini thinking level | `high`, `minimal` |
| `TRADINGAGENTS_ANTHROPIC_EFFORT` | Claude effort | `low`, `medium`, `high` |
| `TRADINGAGENTS_CHECKPOINT_ENABLED` | Checkpoint-resume default | `true`, `false` |
| `TRADINGAGENTS_BENCHMARK_TICKER` | Alpha benchmark ticker | `SPY` |
| `TRADINGAGENTS_RESULTS_DIR` | Where reports and logs are written | `/home/appuser/.tradingagents/logs` |
| `TRADINGAGENTS_CACHE_DIR` | Data cache directory | `/home/appuser/.tradingagents/cache` |
| `TRADINGAGENTS_MEMORY_LOG_PATH` | Decision-memory log file | `/home/appuser/.tradingagents/memory/trading_memory.md` |

Setting both `TRADINGAGENTS_MAX_DEBATE_ROUNDS` and `TRADINGAGENTS_MAX_RISK_ROUNDS`
is equivalent to choosing a research depth, and lets the wizard skip that step.

### Precedence

For any given setting, the value is resolved in this order (first wins):

1. A command-line flag (e.g. `--research-depth`, `--language`).
2. The matching `TRADINGAGENTS_*` environment variable.
3. The built-in default in `tradingagents/default_config.py`.

## Output location

Two things are written per run:

- Per-section reports and the message/tool log, under
  `<TRADINGAGENTS_RESULTS_DIR>/<ticker>/<analysis_date>/` (defaults to
  `~/.tradingagents/logs/...`).
- The consolidated final report. In an unattended run it auto-saves to
  `reports/<ticker>_<timestamp>/` under the working directory unless you pass
  `--no-save`; in interactive mode you are prompted for the path unless you pass
  `--save` or `--no-save`.

Under Docker, bind-mount a host directory so these survive the container and are
visible on the host. For example, add a `docker-compose.override.yml`:

```yaml
services:
  tradingagents:
    volumes:
      - ./output:/home/appuser/.tradingagents   # logs + per-section reports
      - ./output:/home/appuser/app/reports       # final consolidated report
```

Then results appear under `./output/` on the host. Point the
`TRADINGAGENTS_RESULTS_DIR` / `TRADINGAGENTS_CACHE_DIR` / `TRADINGAGENTS_MEMORY_LOG_PATH`
variables at paths inside a mounted directory to relocate them further.

## Note for Docker users

The CLI code is baked into the image at build time. After changing anything
under `cli/`, rebuild so the installed command picks it up:

```bash
docker compose build tradingagents
```
