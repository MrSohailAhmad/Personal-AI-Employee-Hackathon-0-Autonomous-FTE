# Digital FTE — Personal AI Employee (Bronze Tier)

> *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

A **Bronze Tier** implementation of the Digital FTE hackathon project. Claude Code acts as the reasoning engine, Obsidian is the dashboard/memory, and a Python watcher monitors your inbox for new work.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI_Employee_Vault/                   │
│  ┌──────────┐  ┌──────────────┐  ┌──────┐  ┌───────┐  │
│  │  Inbox/  │→ │ Needs_Action/│→ │Done/ │  │Logs/  │  │
│  └──────────┘  └──────────────┘  └──────┘  └───────┘  │
│                                                         │
│  Dashboard.md          Company_Handbook.md              │
└─────────────────────────────────────────────────────────┘
         ↑                         ↑
  filesystem_watcher.py      Claude Code (Skills)
```

**Flow:**
1. Drop a file into `Inbox/` → watcher detects it
2. Watcher creates an action `.md` in `Needs_Action/`
3. Run `/process-inbox` → Claude reads rules, handles item
4. Run `/update-dashboard` → Dashboard.md is refreshed

---

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- [Claude Code](https://claude.com/product/claude-code)
- [Obsidian](https://obsidian.md) (open `AI_Employee_Vault/` as a vault)

### Install

```bash
# Install Python dependencies
uv sync

# Copy and configure environment
cp .env.example .env
# Edit .env as needed
```

### Open in Obsidian

Open Obsidian → "Open folder as vault" → select `AI_Employee_Vault/`

---

## Usage

### Start the File Watcher

```bash
# Dry-run mode (safe, no file moves)
DRY_RUN=true uv run python watchers/filesystem_watcher.py

# Live mode
uv run python watchers/filesystem_watcher.py
```

Or use the Agent Skill:
```
/start-file-watcher
```

### Process Inbox (Claude Code)

```
/process-inbox
```

### Update Dashboard (Claude Code)

```
/update-dashboard
```

---

## Bronze Tier Checklist

- [x] `AI_Employee_Vault/Dashboard.md`
- [x] `AI_Employee_Vault/Company_Handbook.md`
- [x] Folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] File system watcher script (`watchers/filesystem_watcher.py`)
- [x] Claude Code reads from and writes to the vault
- [x] Agent Skills: `/process-inbox`, `/update-dashboard`, `/start-file-watcher`

---

## Security

- All secrets in `.env` (never committed — see `.gitignore`)
- `DRY_RUN=true` by default — set to `false` only when ready
- No credentials stored in the Obsidian vault
- Human-in-the-loop approval for sensitive actions (approval request files)

---

## Project Structure

```
digital_fte/
├── AI_Employee_Vault/
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Done/
│   ├── Logs/
│   └── Briefings/
├── watchers/
│   ├── base_watcher.py
│   └── filesystem_watcher.py
├── .claude/
│   └── skills/
│       ├── process-inbox/SKILL.md
│       ├── update-dashboard/SKILL.md
│       └── start-file-watcher/SKILL.md
├── pyproject.toml
├── .env.example
└── README.md
```

---

*Built with Claude Code · Hackathon Bronze Tier*
