#!/usr/bin/env bash
#
# Remind the model to write what it has learned into the FAQ, at the two moments
# it is most likely to lose it.
#
# WHY A HOOK AND NOT A CLAUDE.md LINE
# A CLAUDE.md instruction is read once, at the top of the session, and then
# competes with everything that follows. The two moments that actually matter
# arrive late:
#
#   1. Just before compaction. Whatever was learned and not written down is
#      about to be summarised away. This is the single highest-value reminder
#      in the whole session, and nothing in the prompt fires at that point --
#      only the PreCompact hook does.
#   2. During a long session. An hour of work accumulates far more than anyone
#      remembers to flush at the end.
#
# USAGE
#   faq-reminder.sh precompact   # PreCompact hook: plain stdout IS the answer
#   faq-reminder.sh periodic     # UserPromptSubmit hook: JSON additionalContext,
#                                # and only once per interval
#
# Wire it up in a project's .claude/settings.json -- see hooks/README.md.
#
# Verified against Claude Code 2.1.330: `PreCompact` takes a trigger of
# "auto" or "manual" and treats plain text as the hook's answer;
# `UserPromptSubmit` injects `hookSpecificOutput.additionalContext`.

set -uo pipefail

# How long between periodic reminders. 60 minutes by default; set to 0 to
# disable the periodic one without unwiring it.
INTERVAL_MINUTES="${FAQ_REMINDER_INTERVAL_MINUTES:-60}"

# One stamp per project, so two repos open at once do not silence each other.
project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
state_dir="${XDG_STATE_HOME:-$HOME/.local/state}/faq-reminder"
stamp="$state_dir/$(printf '%s' "$project_dir" | tr -c 'A-Za-z0-9' '-').stamp"

# A reminder is worthless in a project with no FAQ tree: say nothing rather
# than nag about a directory that does not exist.
faq_dir=""
for candidate in "$project_dir/.claude/faqs" "$project_dir/faqs"; do
  if [ -d "$candidate" ]; then
    faq_dir="$candidate"
    break
  fi
done
[ -n "$faq_dir" ] || exit 0

message() {
  local when="$1"
  cat <<EOF
$when

Write anything learned this session into the FAQ at ${faq_dir#"$project_dir"/}
before it is lost: a new pitfall, a changed procedure, an approach that was
tried and rejected, an environment gotcha, a correction to an existing entry.

Do it now, in the same turn, rather than noting it for later:
  1. search_faqs("<the topic>") to find the entry that should hold it, or to
     confirm none does.
  2. Edit that file under ${faq_dir#"$project_dir"/}, or add one.
  3. Nothing to add is a fine answer. Say so in one line and carry on --
     do not invent an entry to satisfy this reminder, and do not rewrite an
     entry that is already correct.
EOF
}

case "${1:-}" in
  precompact)
    # PreCompact: plain text on stdout is the hook's answer. Always fires --
    # compaction is precisely when unwritten knowledge disappears.
    message "The conversation is about to be compacted."
    ;;

  periodic)
    [ "$INTERVAL_MINUTES" -gt 0 ] 2>/dev/null || exit 0
    now=$(date +%s)
    last=0
    [ -f "$stamp" ] && last=$(cat "$stamp" 2>/dev/null || echo 0)
    case "$last" in
      ''|*[!0-9]*) last=0 ;;
    esac
    # First prompt of a session sets the clock rather than firing immediately:
    # a reminder before any work has happened is pure noise.
    if [ "$last" -eq 0 ]; then
      mkdir -p "$state_dir" && printf '%s' "$now" > "$stamp"
      exit 0
    fi
    if [ $(( (now - last) / 60 )) -lt "$INTERVAL_MINUTES" ]; then
      exit 0
    fi
    mkdir -p "$state_dir" && printf '%s' "$now" > "$stamp"
    python3 -I -c '
import json, sys
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": sys.stdin.read(),
}}))
' <<< "$(message "It has been ${INTERVAL_MINUTES}+ minutes since the last FAQ check.")"
    ;;

  *)
    echo "usage: $0 {precompact|periodic}" >&2
    exit 2
    ;;
esac
