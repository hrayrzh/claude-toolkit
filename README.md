<div align="center">

![claude-toolkit](assets/banner.png)

# claude-toolkit

**Reusable [Claude Code](https://www.claude.com/product/claude-code) plugins — hooks and skills.**
Install only the pieces you want; each is a separate, self-contained plugin.

![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-c6743a)
![License: MIT](https://img.shields.io/badge/License-MIT-5fb47e)
![Plugins](https://img.shields.io/badge/plugins-2-9fb4cd)

</div>

---

## Plugins

| Plugin | Type | What it does |
|---|---|---|
| [**auto-approve-permissions**](plugins/auto-approve-permissions/) | hook | Auto-approves read-only / inspection commands and web search, so Claude Code stops asking permission for every `ls`, `grep`, `cat` — while still prompting for anything that writes, deletes, or calls an external service. |
| [**house-modeler**](plugins/house-modeler/) | skill | Turns hand-drawn or photographed floor plans into accurate 2D plans (SVG) **and** an interactive, walkable 3D model (Three.js), from one source of truth. Walls, doors, windows, areas, furniture clearances, plot, levels, sun-by-latitude, roofs — plus a friendly interview for non-coders. |

## Install

Add the source once, then install whichever plugins you want:

```bash
/plugin marketplace add hrayrzh/claude-toolkit
/plugin install auto-approve-permissions@claude-toolkit
/plugin install house-modeler@claude-toolkit
```

Each plugin is enabled and disabled independently — nothing else is pulled in.

> *Marketplace* is simply Claude Code's term for a plugin source. This is a free,
> open-source collection — there is nothing to buy.

## Repository layout

```
claude-toolkit/
├── .claude-plugin/marketplace.json     # the plugin catalog
└── plugins/
    └── <name>/
        ├── .claude-plugin/plugin.json  # plugin manifest
        ├── hooks/        hooks.json + scripts   (hook plugins)
        ├── skills/       <name>/SKILL.md        (skill plugins)
        └── README.md
```

## Manual install

Each plugin folder is self-contained. Instead of the plugin system you can copy a
plugin's `hooks/` script into `~/.claude/hooks/` (global) or `<project>/.claude/hooks/`
(per-project) and register it in the matching `settings.json` — see the plugin's own README.

## License

MIT © [hrayrzh](https://github.com/hrayrzh)
