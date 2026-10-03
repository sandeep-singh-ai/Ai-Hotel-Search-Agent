# AI Hotel Search Agent

A [CrewAI](https://crewai.com) app that looks up hotels near a place you name and writes a short guide to `report.md`.

Two agents run in sequence:

1. **Travel agent** searches for hotels in the location and radius you enter, including ratings and reviews from the search results.
2. **Tourist guide** turns that research into a short markdown guide.

Search uses [Serper](https://serper.dev) through CrewAI's `SerperScrapeWebsiteTool`. The model call uses OpenAI.

## Prerequisites

- Python **3.10, 3.11, 3.12, or 3.13** (`>=3.10,<3.14`)
- [uv](https://docs.astral.sh/uv/) for installs
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Serper API key](https://serper.dev/api-key)

## Setup

Clone the repo and move into it:

```bash
git clone https://github.com/sandeep-singh-ai/Ai-Hotel-Search-Agent.git
cd Ai-Hotel-Search-Agent
```

Install uv if you do not already have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS you can use Homebrew instead: `brew install uv`.

Install the project and its lockfile into a local `.venv`:

```bash
uv sync
```

Create your env file from the example and fill in both keys. `.env` stays on your machine and is listed in `.gitignore`.

```bash
cp .env.example .env
```

```bash
MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...
```

`MODEL` is the chat model the crew calls. `gpt-4o-mini` is the default in `.env.example`. Change it if you want a different OpenAI model.

## Run

From the project root:

```bash
uv run crewai run
```

The same entry point is available as:

```bash
uv run hotel_research
```

The CLI asks for two inputs:

| Prompt | Example |
| --- | --- |
| Location | `San Francisco, CA` |
| Miles (search radius) | `5` |

When the crew finishes, open `report.md` in the project root. That file is generated on each run and is not committed.

## Project layout

```text
src/hotel_research/main.py              prompts for location and miles, then starts the crew
src/hotel_research/crew.py              agents, tools, and task order
src/hotel_research/config/agents.yaml   travel agent and tourist guide
src/hotel_research/config/tasks.yaml    research task and guide task
knowledge/user_preference.txt           optional CrewAI user context
```

To change who the agents are or what they produce, edit the YAML files. To change tools or how tasks are wired, edit `crew.py`.

## Notes

- Do not commit `.env`. Only `.env.example` belongs in git.
- `uv.lock` is committed so `uv sync` installs the same dependency set.
- CrewAI docs: https://docs.crewai.com
