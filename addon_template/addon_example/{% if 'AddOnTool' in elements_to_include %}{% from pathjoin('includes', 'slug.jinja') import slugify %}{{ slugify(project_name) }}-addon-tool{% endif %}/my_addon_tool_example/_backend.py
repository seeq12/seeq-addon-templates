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
            "required for this Add-on")
    return df


def push_signal(df, workbook_id, worksheet_id):
    combined_signal = spy.push(df, workbook=workbook_id, status=spy.Status(quiet=True), quiet=True)
    include_inventory = True if spy.user.is_admin else False

    # Get the current worksheet
    workbook = spy.workbooks.pull(workbook_id, include_inventory=include_inventory)[0]
    worksheet = next((ws for ws in workbook.worksheets if ws.id == worksheet_id), None)

    # Add the combined signal if it's not already displayed on the worksheet
    combined_signal_id = combined_signal['ID'].values[0]
    if combined_signal_id not in worksheet.display_items['ID'].values:
        worksheet.display_items = pd.concat([worksheet.display_items, combined_signal]).reset_index()

    # Push the updated worksheet back to Seeq
    spy.workbooks.push(workbook, include_inventory=include_inventory)
