#!/usr/bin/env python3
"""CI tasks."""
from codecs import ignore_errors
from functools import partial
import shutil
import glob
import os
from doit.tools import create_folder
from doit.task import clean_targets

DOIT_CONFIG = {'default_tasks': ['translations']}


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
        actions.append((create_folder, [f'jackalify/locales/{lang}/LC_MESSAGES']))
        actions.append(f'pybabel compile -i locales/{lang}/LC_MESSAGES/jackalify.po -o jackalify/locales/{lang}/LC_MESSAGES/jackalify.mo -l {lang}')
    return {
        "actions": actions,
        "file_dep": glob.glob("locales/**/*.po", recursive=True),
        "task_dep": ['po'],
        "targets": glob.glob("jackalify/locales/**/*.mo", recursive=True) if glob.glob("jackalify/locales/**/*.mo", recursive=True) else ['.mo'],
        "clean": True,
    }


def task_translations_ru():
    """Compile translations ru."""
    languages = ['ru']
    actions = []
    for lang in languages:
        actions.append((create_folder, [f'jackalify/locales/{lang}/LC_MESSAGES']))
        actions.append(f'pybabel compile -i locales/{lang}/LC_MESSAGES/jackalify.po -o jackalify/locales/{lang}/LC_MESSAGES/jackalify.mo -l {lang}')
    return {
        "actions": actions,
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
        "actions": [],
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
        "actions": ['flake8 --max-line-length=120 jackalify'],
    }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        "actions": ['pydocstyle jackalify'],
    }


def rm_dir(dir):
    """Remove dir if empty, do nothing if not"""
    try:
        os.rmdir(dir)
    except:
        pass


def task_wheel():
    """Create binary wheel distribution."""
    clean_dist = partial(rm_dir, 'dist')
    clean_build = partial(shutil.rmtree, 'build', ignore_errors=True)
    clean_egg = partial(shutil.rmtree, 'jackalify.egg-info', ignore_errors=True)
    return {
        "actions": ['python -m build -w'],
        "verbosity": 2,
        "task_dep": ['translations'],
        "targets": glob.glob("dist/*.whl") if glob.glob("dist/*.whl") else ['.whl'],
        "clean": [clean_targets, clean_dist, clean_build, clean_egg],
    }


def task_source():
    """Create source distribution."""
    clean_dist = partial(rm_dir, 'dist')
    clean_egg = partial(shutil.rmtree, 'jackalify.egg-info', ignore_errors=True)
    return {
        "actions": ['python -m build -s'],
        "verbosity": 2,
        "targets": glob.glob("dist/*.tar.gz") if glob.glob("dist/*.tar.gz") else ['.tar.gz'],
        "clean": [clean_targets, clean_dist, clean_egg],
    }


def task_release():
    """Release wheel and source distribution to pypi"""
    return {
        "actions": ["python -m twine upload --repository pypi dist/*"],
        "task_dep": ['wheel', 'source']
    }
