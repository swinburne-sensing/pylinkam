# -*- coding: utf-8 -*-
import os

from pylinkam import util


def test_add_path_prepends(monkeypatch) -> None:
    monkeypatch.setenv('PATH', os.pathsep.join(['existing-a', 'existing-b']))

    util.add_path('new-path')

    assert os.environ['PATH'] == os.pathsep.join(['new-path', 'existing-a', 'existing-b'])
