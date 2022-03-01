import numpy as np
import pandas as pd
import pytest

from seeq.addons import {{cookiecutter.project}}


@pytest.mark.backend()
def test_cross_correlations():
    samples = 10
    df = {{cookiecutter.project}}.create_new_signal(np.ones(samples) * 2,
                                np.ones(samples),
                                pd.Index(np.linspace(1, samples, samples)),
                                'add')
    assert len(df.columns) == 1
    assert len(df) == samples
