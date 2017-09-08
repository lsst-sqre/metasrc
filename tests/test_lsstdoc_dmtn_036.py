"""Test LsstDoc using sample data from DMTN-036.tex.
"""

import os
import pytest
from metasrc.tex.lsstdoc import LsstDoc

TITLE = (
    "jointcal: Simultaneous Astrometry \\& Photometry for thousands "
    "of\nExposures with Large CCD Mosaics"
)

SHORT_TITLE = "jointcal"

HTML_TITLE = (
    "jointcal: Simultaneous Astrometry &amp; Photometry for thousands of "
    "Exposures with Large CCD Mosaics\n"
)

HTML_SHORT_TITLE = "jointcal\n"

AUTHORS = [
    "John Parejko (University of Washington)",
    "Pierre Astier (LPNHE/IN2P3/CNRS Paris)"
]

HTML_AUTHORS = [
    "John Parejko (University of Washington)",
    "Pierre Astier (LPNHE/IN2P3/CNRS Paris)"
]

HTML_ABSTRACT = (
    "<p>The jointcal package simultaneously optimizes the astrometric and "
    "photometric calibrations of a set of astronomical images. In "
    "principle and often in practice, this approach produces distortion "
    "and thoroughput models which are more precise than when fitted "
    "independently. This is especially true when the images are deeper "
    "than the astrometric reference catalogs. In the “Astromatic” "
    "software suite, this simultaneous astrometry functionality is "
    "fulfilled by “SCAMP”. The code we describe here has similar aims, "
    "but follows a slightly different route. Jointcal is built on top of "
    "the the LSST Data Management software stack.</p>\n"
)

IS_DRAFT = True

HANDLE = 'DMTN-036'

SERIES = 'DMTN'

SERIAL = '036'

ATTRIBUTES = [
    ('title', TITLE),
    ('short_title', SHORT_TITLE),
    ('html_title', HTML_TITLE),
    ('html_short_title', HTML_SHORT_TITLE),
    ('authors', AUTHORS),
    ('html_authors', HTML_AUTHORS),
    ('html_abstract', HTML_ABSTRACT),
    ('is_draft', IS_DRAFT),
    ('handle', HANDLE),
    ('series', SERIES),
    ('serial', SERIAL),
]


@pytest.fixture
def lsstdoc():
    tex_path = os.path.join(os.path.dirname(__file__), 'data', 'DMTN-036.tex')
    return LsstDoc.read(tex_path)


@pytest.mark.parametrize('attribute,expected', ATTRIBUTES)
def test_attribute(lsstdoc, attribute, expected):
    assert getattr(lsstdoc, attribute) == expected
