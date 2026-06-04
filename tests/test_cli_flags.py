"""Tests for CLI argument parsing in vibeship-optimizer."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vibeship_optimizer.cli import build_parser


class TestCliParser:
    """Verify the CLI argument parser."""

    def test_parser_created(self):
        p = build_parser()
        assert p is not None
        assert p.prog == "vibeship-optimizer"

    def test_init_subcommand(self):
        p = build_parser()
        args = p.parse_args(["init"])
        assert args.cmd == "init"

    def test_onboard_subcommand(self):
        p = build_parser()
        args = p.parse_args(["onboard"])
        assert args.cmd == "onboard"

    def test_snapshot_subcommand(self):
        p = build_parser()
        args = p.parse_args(["snapshot", "--label", "test"])
        assert args.cmd == "snapshot"
        assert args.label == "test"

    def test_compare_subcommand(self):
        p = build_parser()
        args = p.parse_args(["compare", "--before", "a.json", "--after", "b.json"])
        assert args.cmd == "compare"
        assert args.before == "a.json"
        assert args.after == "b.json"
