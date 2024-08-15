from urllib.parse import urlparse, unquote, parse_qs


def parse_url(url):
    unquoted_url = unquote(url)
    return urlparse(unquoted_url)


def get_worksheet_url(jupyter_notebook_url):
    parsed = parse_url(jupyter_notebook_url)
    params = parse_qs(parsed.query)
    return f"{parsed.scheme}://{parsed.netloc}/workbook/{params['workbookId'][0]}/worksheet/{params['worksheetId'][0]}"


def get_workbook_worksheet_workstep_ids(url):
    """
    Gets the workbook, worksheet, and worksteps IDs from the URL
    Parameters
    ----------
    url: str
        Seeq URL

    Returns
    -------
    tuple
    """
    parsed = parse_url(url)
    params = parse_qs(parsed.query)
    workbook_id = None
    worksheet_id = None
    workstep_id = None
    if 'workbookId' in params:
        workbook_id = params['workbookId'][0]
    if 'worksheetId' in params:
        worksheet_id = params['worksheetId'][0]
    if 'workstepId' in params:
        workstep_id = params['workstepId'][0]
    return workbook_id, worksheet_id, workstep_id
