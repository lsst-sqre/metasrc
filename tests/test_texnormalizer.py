"""Tests for the metasrc.tex.texnormalizer module.
"""

import os
import re

import pytest

import metasrc.tex.texnormalizer as texnormalizer


def test_remove_comments_abstract():
    sample = ("\setDocAbstract{%\n"
              " The LSST Data Management System (DMS) is a set of services\n"
              " employing a variety of software components running on\n"
              " computational and networking infrastructure that combine to\n"
              " deliver science data products to the observatory's users and\n"
              " support observatory operations.  This document describes the\n"
              " components, their service instances, and their deployment\n"
              " environments as well as the interfaces among them, the rest\n"
              " of the LSST system, and the outside world.\n"
              "}")
    expected = (
        "\setDocAbstract{\n"
        " The LSST Data Management System (DMS) is a set of services\n"
        " employing a variety of software components running on\n"
        " computational and networking infrastructure that combine to\n"
        " deliver science data products to the observatory's users and\n"
        " support observatory operations.  This document describes the\n"
        " components, their service instances, and their deployment\n"
        " environments as well as the interfaces among them, the rest\n"
        " of the LSST system, and the outside world.\n"
        "}")
    assert texnormalizer.remove_comments(sample) == expected


def test_escaped_remove_comments():
    """Test remove_comments where a "%" is escaped."""
    sample = "The uncertainty is 5\%.  % a comment"
    expected = "The uncertainty is 5\%.  "
    assert texnormalizer.remove_comments(sample) == expected


def test_single_line_remove_comments():
    sample = "This is content.  % a comment"
    expected = "This is content.  "
    assert texnormalizer.remove_comments(sample) == expected


def test_remove_single_line_trailing_whitespace():
    sample = "This is content.    "
    expected = "This is content."
    assert texnormalizer.remove_trailing_whitespace(sample) == expected


def test_multi_line_trailing_whitespace():
    sample = ("First line.    \n"
              "Second line. ")
    expected = ("First line.\n"
                "Second line.")
    assert texnormalizer.remove_trailing_whitespace(sample) == expected


def test_read_tex_file():
    project_dir = os.path.join(os.path.dirname(__file__), 'data', 'texinputs')
    root_filepath = os.path.join(project_dir, 'LDM-nnn.tex')
    tex_source = texnormalizer.read_tex_file(root_filepath)

    # verify that input'd and include'd content is present
    assert re.search(r'\\setDocAbstract', tex_source) is not None
    assert re.search(r'\\section{Introduction}', tex_source) is not None


def test_replace_macros():
    sample = (
        r"\def \product {Data Management}" + "\n"
        r"\title    [Test Plan]  { \product\ Test Plan}" + "\n"
        r"\setDocAbstract {" + "\n"
        r"This is the  Test Plan for \product.}")

    expected = (
        r"\def Data Management {Data Management}" + "\n"
        r"\title    [Test Plan]  { Data Management Test Plan}" + "\n"
        r"\setDocAbstract {" + "\n"
        r"This is the  Test Plan for Data Management.}")

    macros = {r'\product': 'Data Management'}
    tex_source = texnormalizer.replace_macros(sample, macros)
    assert re.search(r'\\product', sample) is not None  # sanity check
    assert re.search(r'\\product', tex_source) is None
    assert tex_source == expected


@pytest.mark.parametrize(
    'sample,expected',
    [('\input{file.tex}', 'file.tex'),
     ('\input{dirname/file.tex}', 'dirname/file.tex'),
     ('\input {file}%', 'file'),
     ('\input file%', 'file'),
     ('\input file\n', 'file'),
     ('\input file \n', 'file'),
     ('\include{file.tex}', 'file.tex'),
     ('\include{dirname/file.tex}', 'dirname/file.tex'),
     ('\include {file}%', 'file'),
     ('\include file%', 'file'),
     ('\include file\n', 'file'),
     ('\include file \n', 'file')])
def test_input_include_pattern(sample, expected):
    match = re.search(texnormalizer.input_include_pattern, sample)
    assert match.group('filename') == expected