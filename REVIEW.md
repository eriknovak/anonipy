# REVIEW.md

How changes to this repo are reviewed. The `step-reviewer` agent reads this
file at every step checkpoint, and `dev-tools:code-review` reads it at the
branch-wide pass. The coding standards and the review checklist apply on top
of it; where this file speaks, it wins.

Edit any section by hand. `dev-tools:implement` appends to "Learned rules"
when the user answers a review stop with `ignore <n>` or `missed <what>`; the
PR diff is where those rules are approved.

## What to check

- **What a caller sees.** A changed signature, flag, file path, config key
  or output format, and every caller that still uses the old one.
- **What the step's plan line asked for.** A missing part, or a part nobody
  asked for.
- **Errors and edge cases.** An empty input, a missing file, a failed
  command, a second run over the same state.
- **Data and state that outlive the run.** A migration, a written file, a
  deleted path, a pushed commit: anything a rerun cannot undo.
- **Secrets.** A credential, token or personal detail in code, a log line or
  a committed file.

## What to ignore

- Anything the formatter, linter or type checker enforces.
- Style the repo's own standards endorse.
- A wording preference in prose or a comment that keeps the meaning.
- A speculative risk with no input that triggers it.

## How to report

Every finding is triaged three ways:

- **ignore**: a rule under "What to ignore", or an `ignore:` line under
  "Learned rules", drops it. It is counted, never shown.
- **agent-check**: the reviewer can decide it alone, by running a command
  (a test, a grep, a render, a script on a fixture) or by reading the code
  against a written rule. It reports only a confirmed failure, with its
  evidence. The implementer fixes it, with no stop.
- **human-verify**: only judgement or a resource the reviewer lacks can
  decide it (intent, taste, a live service, real data). The reviewer gives
  the `file:line`, the blast radius (what breaks and who notices), the
  severity and one thing to try.

Severity weighs what a wrong version costs, not how large the hunk is:

- **high**: users, data or other people's work suffer, and nothing
  downstream catches it before they do.
- **medium**: a caller or the user notices wrong behaviour, but it is
  recoverable or a later check would catch it.
- **low**: everything else. Counted, never shown.

Only medium and high human-verify items reach the user.

## How to test

The commands the reviewer may run for an agent-check, from the repo root.
The reviewer always runs `~/.claude/scripts/check.sh` on the range itself,
which detects the formatter, linter, type checker and tests; list here, one
per line, what it cannot find.

## Learned rules

One line per rule, newest last, written from the user's replies at a
review stop: `ignore <n>` writes an `ignore:` rule, `missed <what>` writes a
`check:` rule. An `ignore:` line drops items like "What to ignore"; a
`check:` line is checked like "What to check". The shape is
`- <ignore|check>: <the rule> · <date> <slug> step <n> · "<the user's
words>"`, the words being the user's reply for that item.
