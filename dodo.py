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
        "file_dep": glob.glob("**/*.po", recursive=True),
        "targets": glob.glob("**/*.mo", recursive=True) if glob.glob("**/*.mo", recursive=True) else ['.mo'],
        "clean": True,
    }


def task_html():
    """Make HTML documentation."""
    build_dir = 'docs/_build'
    clean_build = partial(shutil.rmtree, build_dir, ignore_errors=True)
    return {
        "actions": ['sphinx-build docs %(targets)s'],
        "file_dep": glob.glob("**/*.py", recursive=True) + glob.glob("**/*.rst", recursive=True),
        "task_dep": ["translations"],
        "targets": [build_dir],
        "clean": [clean_build],
    }


def task_test():
    """Perform all tests."""
    return {
        "actions": ['python -m unittest -v -f test/*.py'],
        "task_dep": ["unittest", "style", "docstyle"],
    }


def task_unittest():
    """Perform unittests."""
    return {
        "actions": ['python -m unittest -v -f test/*.py'],
        "task_dep": ["translations"],
    }


def task_style():
    """Check style against flake8."""
    return {
        "actions": ['flake8 --extend-ignore=E501 src'],
    }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        "actions": ['pydocstyle src'],
    }
