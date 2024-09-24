import matplotlib.pyplot as plt
import base64
from io import BytesIO
import ipyvuetify as v


def matplotlib_figure_to_vuetify_widget(fig):
    # Convert Matplotlib figure to PNG image
    png_image = BytesIO()
    fig.savefig(png_image, format='png')

    # Encode PNG image to base64 string
    png_image_base64 = base64.b64encode(png_image.getvalue()).decode('utf8')

    # Return ipyvuetify Html widget with the base64 string as the source of an img tag
    return v.Html(tag='img', children=[], attributes={'src': f'data:image/png;base64,{png_image_base64}'})


def create_matplotlib_widget(df):
    fig, ax = plt.subplots()
    ax.set_visible(True)
    if not df.empty:
        df.plot(ax=ax)
    return matplotlib_figure_to_vuetify_widget(fig)
