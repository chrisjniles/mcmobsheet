"""Guards that man/mcmobsheet.1 stays in sync with mcmobsheet._docs.MANUAL.

If this fails, someone edited MANUAL without re-running
scripts/generate_man.py before committing.
"""

import pathlib

from mcmobsheet._docs import render_man

MAN_PAGE = pathlib.Path(__file__).resolve().parent.parent / "man" / "mcmobsheet.1"


def test_man_page_matches_generator_output():
    assert MAN_PAGE.read_text() == render_man()
