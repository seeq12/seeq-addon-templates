"""
This is a dummy file that contains some functions (it could be classes) to perform backend calculations
"""

import numpy as np
import pandas as pd
from seeq import spy


def create_new_signal(signal_a: np.array, signal_b: np.array, index: pd.Index, operation):
    """
    Creates resulting signal from the input signals

    Parameters
    ----------
    signal_a: pd.DataFrame
        First input signal
    signal_b: pd.DataFrame
        Second input signal
    index: pd.Index
        DataFrame index of the resulting signal
    operation: {'add', 'subtract', 'multiply', 'divide'}
        Determines the math operation applied to signal_a with signal_b

    Returns
    -------
    pd.DataFrame

    """
    if operation not in ['add', 'subtract', 'multiply', 'divide']:
        raise NameError(f"{operation} is not a supported math operator")
    return pd.DataFrame(getattr(np, operation)(signal_a, signal_b), index=index, columns=['Result'])


def pull_only_signals(url, grid='auto'):
    worksheet = spy.utils.get_analysis_worksheet_from_url(url)
    start = worksheet.display_range['Start']
    end = worksheet.display_range['End']

    search_df = spy.search(url, estimate_sample_period=worksheet.display_range, quiet=True)
    if search_df.empty:
        return pd.DataFrame()
    search_signals_df = search_df[search_df['Type'].str.contains('Signal')]

    df = spy.pull(search_signals_df, start=start, end=end, grid=grid, header='ID', quiet=True,
                  status=spy.Status(quiet=True))

    if df.empty:
        return pd.DataFrame()

    if hasattr(df, 'spy') and hasattr(df.spy, 'query_df'):
        df.columns = df.spy.query_df['Name']
    elif hasattr(df, 'query_df'):
        df.columns = df.query_df['Name']
    else:
        raise AttributeError(
            "A call to `spy.pull` was successful but the response object does not contain the `spy.query_df` property "
            "required for `seeq.addons.sosg")
    return df


def push_signal(df, workbook_id, worksheet_name):
    return spy.push(df, workbook=workbook_id, worksheet=worksheet_name, status=spy.Status(quiet=True), quiet=True)
