#!/bin/bash

case "$1" in
  gateway)
    python3 "$MAGIC_LOC"/magic/bin/magic-network "$@"
    ;;
  payment|privacy)
    python3 "$MAGIC_LOC"/magic/bin/magic-network "$@"
    ;;
  *)
    # The command is something like bash, not an magic subcommand. Just run it in the right environment.
    "$@"
    ;;
esac

