#!/usr/bin/env python3
"""CI tasks."""
from functools import partial
import shutil
import glob


def task_translations():
    """Generate .mo translation files."""
    languages = ['ru', 'en']
    actions = []
    for lang in languages:
        actions.append(f'pybabel compile -D src -d locales -l {lang}')
    return {
        "actions": actions,
        "targets": glob.glob("*.mo"),
        "clean": True
    }


def task_html():
    """Make HTML documentation."""
    build_dir = 'docs/_build'
    clean_build = partial(shutil.rmtree, build_dir, ignore_errors=True)
    return {
        "actions": ['sphinx-build docs %(targets)s'],
        "file_dep": glob.glob("*.py") + glob.glob("*.rst"),
        "targets": [build_dir],
        "clean": [clean_build]
    }


def task_test():
    """Test code."""
    return {
        "actions": ['python -m unittest -v -f tests/*.py']
    }
