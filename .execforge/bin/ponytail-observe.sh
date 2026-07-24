#!/bin/sh
# User-triggered observation job for the ponytail pilot (Plan B in the
# 2026-07-17 ExecForge decision). Two modes:
#   record <task-slug> <on|off> [note]  — snapshot current diff stats for a task
#   report                              — compare ponytail-on vs ponytail-off runs
set -eu

LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/runs/20260717T0400042436000Z-f2f06790-ponytail-adoption"
LOG="$LOG_DIR/pilot-log.tsv"

case "${1:-}" in
  record)
    slug="${2:?usage: ponytail-observe.sh record <task-slug> <on|off> [note]}"
    mode="${3:?specify on or off}"
    note="${4:-}"
    stat=$(git diff HEAD --shortstat)
    files=$(printf '%s' "$stat" | awk '{print $1+0}'); files=${files:-0}
    ins=$(printf '%s' "$stat" | grep -o '[0-9]* insertion' | awk '{print $1}'); ins=${ins:-0}
    del=$(printf '%s' "$stat" | grep -o '[0-9]* deletion' | awk '{print $1}'); del=${del:-0}
    [ -f "$LOG" ] || printf 'date\ttask\tponytail\tfiles\tinsertions\tdeletions\tnote\n' > "$LOG"
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$slug" "$mode" "$files" "$ins" "$del" "$note" >> "$LOG"
    echo "recorded: $slug ponytail=$mode files=$files +$ins/-$del"
    ;;
  report)
    [ -f "$LOG" ] || { echo "no pilot runs recorded yet ($LOG)"; exit 0; }
    column -t -s "$(printf '\t')" "$LOG"
    echo
    awk -F'\t' 'NR>1 {n[$3]++; ins[$3]+=$5; f[$3]+=$4}
      END {for (m in n) printf "ponytail=%s: %d runs, avg insertions %.0f, avg files %.1f\n", m, n[m], ins[m]/n[m], f[m]/n[m]}' "$LOG"
    ;;
  *)
    echo "usage: ponytail-observe.sh record <task-slug> <on|off> [note] | report"
    exit 1
    ;;
esac
