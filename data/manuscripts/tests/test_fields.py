import pytest

import data.manuscripts.field as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)


@pytest.mark.skip('Skipping cause not done')
def test_get_fld_names():
    assert isinstance(mflds.get_fld_names(), list)