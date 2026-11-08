# AI Hotel Search Agent

A [CrewAI](https://crewai.com) app that looks up hotels near a place you name and writes a short guide to `report.md`.

Two agents run in sequence:

1. **Travel agent** calls `hotel_search_tool` for your location and dates, filters hotels to your radius, and ranks them with price, Google rating, reviews, distance, amenities and link.
2. **Tourist guide** turns that ranked list into a markdown guide with a top pick and two runner-ups. It has no tools and only uses the travel agent's results.

Search uses [SerpAPI](https://serpapi.com): the Google Hotels engine for listings and the Google Maps engine to find the location's center, so distances are computed in code. The model call uses OpenAI.

## Prerequisites

- Python **3.10, 3.11, 3.12, or 3.13** (`>=3.10,<3.14`)
- [uv](https://docs.astral.sh/uv/) for installs
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [SerpAPI key](https://serpapi.com/manage-api-key)

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
SERPAPI_API_KEY=...
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

The CLI asks for these inputs:

| Prompt | Example | Default |
| --- | --- | --- |
| Location | `San Francisco, CA` | required |
| Miles (search radius) | `5` | required |
| Check-in date | `2026-12-20` | tomorrow |
| Check-out date | `2026-12-22` | one night after check-in |
| Preferences | `under $250, gym, quiet` | balance price, rating and distance |

The radius filter only covers the first page of Google Hotels results, so a very small radius can return no hotels.

When the crew finishes, open `report.md` in the project root. That file is generated on each run and is not committed.

## Project layout

```text
src/hotel_research/main.py              prompts for and validates inputs, then starts the crew
src/hotel_research/crew.py              agents and task order
src/hotel_research/tools/hotel_search.py  SerpAPI hotel search, geocoding and radius filter
src/hotel_research/config/agents.yaml   travel agent and tourist guide
src/hotel_research/config/tasks.yaml    research task and guide task
```

To change who the agents are or what they produce, edit the YAML files. To change tools or how tasks are wired, edit `crew.py`.

## Notes

- Do not commit `.env`. Only `.env.example` belongs in git.
- `uv.lock` is committed so `uv sync` installs the same dependency set.
- CrewAI docs: https://docs.crewai.com
