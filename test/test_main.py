# (c) 2023 Michał Górny
# Released under the terms of the MIT license

import argparse
import sys
import types

import pytest

from flaggie.__main__ import (split_arg_sets, split_op,
                              namespace_into_token_group, main,
                              )
from flaggie.config import TokenType


@pytest.mark.parametrize(
    "args,expected",
    [(["+foo", "-bar"], [([], ["+foo", "-bar"])]),
     (["dev-foo/bar", "+foo"], [(["dev-foo/bar"], ["+foo"])]),
     (["dev-foo/bar", "baz", "-foo"],
      [(["dev-foo/bar", "baz"], ["-foo"])]),
     (["+foo", "dev-foo/*", "-foo"],
      [([], ["+foo"]), (["dev-foo/*"], ["-foo"])]),
     ([">=dev-foo/bar-11-r1", "+foo"], [([">=dev-foo/bar-11-r1"], ["+foo"])]),
     (["<bar-11", "+foo"], [(["<bar-11"], ["+foo"])]),
     (["~dev-foo/bar-21", "+foo"], [(["~dev-foo/bar-21"], ["+foo"])]),
     (["=bar-14*", "+foo"], [(["=bar-14*"], ["+foo"])]),
     ])
def test_split_arg_sets(args, expected):
    argp = argparse.ArgumentParser()
    assert list(split_arg_sets(argp, args)) == expected


@pytest.mark.parametrize(
    "args",
    [[""],
     ["dev-foo/bar"],
     ["dev-foo/*", "baz", "+flag", "pkg"],
     ])
def test_split_arg_sets_invalid(args):
    argp = argparse.ArgumentParser()
    with pytest.raises(SystemExit):
        list(split_arg_sets(argp, args))


@pytest.mark.parametrize(
    "op,expected",
    [("+foo", ("+", None, "foo")),
     ("-use::foo", ("-", "use", "foo")),
     ("%", ("%", None, None)),
     ])
def test_split_op(op, expected):
    assert split_op(op) == expected


@pytest.mark.parametrize(
    "arg,expected",
    [("use", (TokenType.USE_FLAG, None)),
     ("kw", (TokenType.KEYWORD, None)),
     ("PYTHON_TARGETS", (TokenType.USE_FLAG, "PYTHON_TARGETS")),
     ])
def test_namespace_into_token_group(arg, expected):
    assert namespace_into_token_group(arg) == expected


def test_main_falls_back_when_package_manager_init_fails(tmp_path,
                                                         monkeypatch):
    (tmp_path / "etc/portage").mkdir(parents=True)

    fake_gentoopm = types.SimpleNamespace(
        get_package_manager=lambda: (_ for _ in ()).throw(
            Exception("pm init failed")))
    monkeypatch.setitem(sys.modules, "gentoopm", fake_gentoopm)

    assert main("flagger",
                "--config-root", str(tmp_path),
                "--no-diff",
                "media-video/pipewire", "+use::sound-server") == 0
    assert ((tmp_path / "etc/portage/package.use/99local.conf")
            .read_text() == "media-video/pipewire sound-server\n")
