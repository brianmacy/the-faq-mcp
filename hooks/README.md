# FAQ reminder hooks

A FAQ decays when the model learns something and the session ends before it is
written down. `CLAUDE.md` can say "keep the FAQ updated", but that line is read
once, at the start, and then competes with everything after it. These hooks fire
at the two moments the knowledge is actually about to be lost.

| Hook               | When it fires                                                                      | What it asks for                                                                                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreCompact`       | immediately before the conversation is compacted, `trigger` `"auto"` or `"manual"` | **write.** Everything learned and not written down is about to be summarised away — the highest-value reminder in a session, and nothing in the prompt fires here |
| `UserPromptSubmit` | on a prompt, at most once per interval (default 60 min)                            | **consult, then write.** More work is about to happen, and work started from a guess is what the FAQ exists to prevent                                            |

The FAQ is a two-way discipline, and the two hooks ask for different halves of
it. Mid-session the **read** half comes first — `search_faqs()` / `get_faq()`
for whatever is about to be done — because acting on training data when the
project has already documented the procedure is the expensive failure. At
compaction there is no "next thing" to look up, only knowledge about to be
lost, so that one asks to write.

There is no timer event in Claude Code, so "every hour" is done by stamping a
file and staying silent until the interval has passed.

## Wiring it up

Clone this repo (or vendor `hooks/faq-reminder.sh` into your own), then add to
the project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/the-faq-mcp/hooks/faq-reminder.sh precompact"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/the-faq-mcp/hooks/faq-reminder.sh periodic"
          }
        ]
      }
    ]
  }
}
```

`CLAUDE_PROJECT_DIR` is set by Claude Code, so the same absolute path works from
every project.

## Behaviour

- **Silent when there is nothing to remind about.** If the project has no
  `.claude/faqs/` (or `faqs/`) directory, both modes exit 0 with no output. A
  reminder pointing at a directory that does not exist is worse than none.
- **Silent on the first prompt of a session.** The periodic mode sets its clock
  instead of firing: a reminder before any work has happened is noise.
- **One stamp per project**, keyed on `CLAUDE_PROJECT_DIR` under
  `${XDG_STATE_HOME:-~/.local/state}/faq-reminder/`, so two repos open at once
  do not silence each other.
- **`FAQ_REMINDER_INTERVAL_MINUTES`** changes the interval; `0` disables the
  periodic reminder without unwiring it. `PreCompact` always fires.
- **The reminder says that "nothing to consult and nothing to add" is a correct
  answer.** Without that, a reminder pressures the model into inventing an
  entry, rewriting a correct one, or re-reading entries it already read this
  session — which is how a FAQ fills with noise and a session fills with
  pointless tool calls.

## Verifying it

```sh
# prints the reminder
CLAUDE_PROJECT_DIR="$PWD" hooks/faq-reminder.sh precompact

# silent the first time (sets the clock), silent again inside the interval
CLAUDE_PROJECT_DIR="$PWD" hooks/faq-reminder.sh periodic

# backdate the stamp to force it, then check the JSON is well formed
f=$(ls "${XDG_STATE_HOME:-$HOME/.local/state}"/faq-reminder/*.stamp | head -1)
printf '%s' "$(( $(date +%s) - 7200 ))" > "$f"
CLAUDE_PROJECT_DIR="$PWD" hooks/faq-reminder.sh periodic | python3 -m json.tool
```

## Contract notes

Verified against Claude Code **2.1.330**:

- On `PreCompact`, **plain text on stdout is the hook's answer** — it is not
  wrapped in JSON like most events. (A `PreCompact` hook can also _block_
  compaction; this one never does.)
- On `UserPromptSubmit`, text reaches the model as
  `hookSpecificOutput.additionalContext`, with `hookEventName` required
  alongside it.
- A hook that exits non-zero or prints malformed JSON is reported as a failure,
  so both modes exit 0 and print nothing when they have nothing to say.
