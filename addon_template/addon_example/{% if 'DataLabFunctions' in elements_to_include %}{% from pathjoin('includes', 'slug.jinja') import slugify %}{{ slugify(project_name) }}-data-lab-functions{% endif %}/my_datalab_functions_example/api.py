import pandas as pd
from logging import Logger
from seeq import spy
from typing import Any


def combine(REQUEST: Any, LOG: Logger) -> str:
    # Get params from request body
    idA = REQUEST['body']['idA']
    idB = REQUEST['body']['idB']
    op = REQUEST['body']['op']
    workbook_id = REQUEST['body']['workbookId']
    worksheet_id = REQUEST['body']['worksheetId']

    # Create the formula to add the two signals
    metadata = pd.DataFrame([{
        'Name': f'Plugin Combined Signal',
        'Formula': f"$signalA.setUnits('') {op} $signalB.setUnits('')",
        'Formula Parameters': {
            'signalA': idA,
            'signalB': idB
        },
        'Type': 'Formula'
    }])

    # Push the formula to Seeq
    LOG.info(f"Pushing formula for 'Plugin Combined Signal' to workbook {workbook_id}")
    combined_signal = spy.push(workbook=workbook_id, metadata=metadata)

    include_inventory = True if spy.user.is_admin else False

    # Get the current worksheet
    workbook = spy.workbooks.pull(workbook_id, include_inventory=include_inventory)[0]
    worksheet = next((ws for ws in workbook.worksheets if ws.id == worksheet_id), None)

    # Add the combined signal if it's not already displayed on the worksheet
    combined_signal_id = combined_signal['ID'].values[0]
    if combined_signal_id not in worksheet.display_items['ID'].values:
        LOG.info(f"Adding signal {combined_signal_id} to worksheet {worksheet_id}")
        worksheet.display_items = pd.concat([worksheet.display_items, combined_signal]).reset_index()

    # Push the updated worksheet back to Seeq
    LOG.info(f"Updating worksheet {worksheet_id} in workbook {workbook_id}")
    results = spy.workbooks.push(workbook, include_inventory=include_inventory)
    return results.to_json()
