#!/usr/bin/env python3
"""
PreToolUse hook — auto-approve read-only operations.
Write / delete / modify / external-API commands still require user permission.
"""
import sys, json, re

data = json.load(sys.stdin)
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

# --- Web research tools: always approve ---
if tool_name in ("WebSearch", "WebFetch"):
    print(json.dumps({"decision": "approve"}))
    sys.exit(0)

if tool_name != "Bash":
    sys.exit(0)  # other tools: normal permission flow

command = tool_input.get("command", "")

# --- Patterns that indicate write / modify / delete / launch ---
UNSAFE = [
    # File system mutations
    r'\brm\s',
    r'\brmdir\b',
    r'\bchmod\b',
    r'\bchown\b',
    r'\bdd\b\s',
    r'\bmv\b',
    r'\bcp\b',
    r'\btouch\b',
    r'\bmkdir\b',
    r'\bln\s',
    # Process control
    r'\bsudo\b',
    r'\bkill\b',
    r'\bpkill\b',
    r'\bfuser\b.*-k',
    r'\bnohup\b',
    r'\bsetsid\b',
    r'\s&\s*$',           # background job (&  at end)
    # Service management
    r'\bsystemctl\b.+\b(start|stop|restart|reload|enable|disable|mask|unmask)\b',
    # Git write operations
    r'\bgit\b.+\b(commit|push|fetch|pull|merge|rebase|reset|add|stash|restore|switch|tag)\b',
    r'\bgit\b.*branch\s+-',
    # Package managers
    r'\bpip3?\s+(install|uninstall|download)\b',
    r'\bnpm\s+(install|uninstall|ci|update)\b',
    r'\bapt(-get)?\s+(install|remove|purge|autoremove|upgrade)\b',
    r'\bbun\s+(install|add|remove|upgrade)\b',
    # curl / wget write calls — [^;|&]* so the match can't cross a shell
    # separator into another command (e.g. `tr -d` after a pipe is not curl -d)
    r'\bcurl\b[^;|&]*\s(-X\s*(POST|PUT|DELETE|PATCH)|--request\s+(POST|PUT|DELETE|PATCH)|--data\b|-d\s+|-F\s+|--upload-file)',
    r'\bwget\b[^;|&]*\s-[Oo]\s',
    # Python scripts (running .py files can do anything)
    r'\bpython3?\s+\S+\.py\b',
    # python3 -c with dangerous operations
    r"\bpython3?\s+-c\b.*\bopen\s*\(.*['\"]w",         # write to file
    r'\bpython3?\s+-c\b.*\bos\.(remove|unlink|rmdir|makedirs|mkdir)\b',
    r'\bpython3?\s+-c\b.*\bsubprocess\b',
    r'\bpython3?\s+-c\b.*\bshutil\b',
    r'\bpython3?\s+-c\b.*\burllib\.request\b',
    r'\bpython3?\s+-c\b.*\brequests\.(get|post|put|delete|patch)\b',
    r'\bnode\b\s+\S+\.js\b',
    # SQLite mutations
    r'\bsqlite3\b.*\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|REPLACE)\b',
]


def has_file_write(cmd):
    """Redirect to a real file (not /dev/null or /tmp)."""
    # Strip string literal contents so > inside regex patterns or strings
    # (e.g. python3 -c "re.search(r'[^>]+>', ...)") don't false-positive.
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', cmd)
    s = re.sub(r"'(?:[^'\\]|\\.)*'", "''", s)
    s = re.sub(r'\d?>>?\s*/dev/null', '', s)
    s = re.sub(r'>>\s*/tmp/\S+', '', s)
    s = re.sub(r'>\s*/tmp/\S+', '', s)
    return bool(re.search(r'(?<![<&2])[>](?![>=])', s))


def has_heredoc(cmd):
    """Heredoc — likely writing a file or running a script inline."""
    return bool(re.search(r"<<\s*['\"]?EOF", cmd, re.IGNORECASE))


def is_unsafe(cmd):
    for pattern in UNSAFE:
        if re.search(pattern, cmd, re.IGNORECASE):
            return True
    if has_file_write(cmd):
        return True
    if has_heredoc(cmd):
        return True
    return False


if not is_unsafe(command):
    print(json.dumps({"decision": "approve"}))
