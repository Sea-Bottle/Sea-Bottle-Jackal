#!/usr/bin/env python3
"""CI tasks."""
from functools import partial
import shutil
import glob


def task_pot():
    """Re-create .pot ."""
    return {
        "actions": ['pybabel extract -F locales/babel-mapping.ini -o jackalify.pot jackalify'],
        "file_dep": glob.glob('**/*.py', recursive=True),
        "targets": ['jackalify.pot'],
        "clean": True,
    }


def task_po():
    """Update translations."""
    return {
        "actions": ['pybabel update -D jackalify -d locales -i jackalify.pot'],
        "file_dep": ['jackalify.pot'],
        "task_dep": ['pot'],
        "targets": glob.glob("locales/**/*.po", recursive=True),
    }


def task_translations():
    """Compile translations."""
    languages = ['ru', 'en']
    actions = []
    for lang in languages:
        actions.append(f'pybabel compile -i locales/{lang}/LC_MESSAGES/jackalify.po -o jackalify/locales/{lang}/LC_MESSAGES/jackalify.mo -l {lang}')
    return {
        "actions": actions,
        "file_dep": glob.glob("locales/**/*.po", recursive=True),
        "task_dep": ['po'],
        "targets": glob.glob("jackalify/locales/**/*.mo", recursive=True) if glob.glob("jackalify/locales/**/*.mo", recursive=True) else ['.mo'],
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
        "actions": ['flake8 --extend-ignore=E501 jackalify'],
    }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        "actions": ['pydocstyle jackalify'],
    }


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
        "actions": ['python -m build -w'],
        "task_dep": ['translations'],
    }


def task_wheel():
    """Create source distribution."""
    return {
        "actions": ['python -m build -s'],
        "task_dep": ['gitclean'],
    }
