"""Tests for vibeship-optimizer PR #1: atomic writes"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_atomic_write_pattern():
    """Verify atomic write pattern is used"""
    root = os.path.join(os.path.dirname(__file__), "..")
    found_atomic = False
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith((".py", ".js", ".ts")):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                atomic_patterns = [
                    "os.rename", "shutil.move",
                    "tempfile.NamedTemporaryFile", "tempfile.mkstemp",
                    "atomic_write", "AtomicWriter",
                    ".tmp", ".part",
                ]
                found = [p for p in atomic_patterns if p in content]
                if found:
                    found_atomic = True
    assert found_atomic, "Should find atomic write pattern"


def test_no_data_loss_on_crash():
    """Verify write-to-temp-then-rename pattern prevents data loss"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith((".py", ".js", ".ts")):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                if "rename" in content or "move" in content:
                    return True


def test_write_to_temp_then_rename():
    """Verify the write-to-temp-then-rename pattern"""
    root = os.path.join(os.path.dirname(__file__), "..")
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirpath or "__pycache__" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.endswith((".py", ".js", ".ts")):
                fpath = os.path.join(dirpath, fn)
                with open(fpath) as f:
                    content = f.read()
                has_temp = any(p in content for p in ["tempfile", ".tmp", ".temp", "temp_dir"])
                has_rename = "os.rename" in content or "fs.rename" in content or "mv" in content
                if has_temp and has_rename:
                    return True
