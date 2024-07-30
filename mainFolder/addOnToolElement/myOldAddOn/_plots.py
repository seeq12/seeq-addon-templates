import pandas as pd

pd.options.plotting.backend = "plotly"


def df_plot(df):
    """
    This function makes a plot of the dataframe that is passed into the
    function and modifies some layout settings of the plot layout.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be plotted

    Returns
    -------
    matplotlib.axes.Axes

    """
    if df.empty:
        return None
    fig = df.plot()
    fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'
    fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
    fig.layout.dragmode = "select"
    fig.layout.modebar = {
        'bgcolor': 'rgba(0, 0, 0, 0)',
        'color': 'rgba(221, 221, 221, 1)',
        'activecolor': 'rgba(0, 121, 96, 1)'
    }
    return fig

