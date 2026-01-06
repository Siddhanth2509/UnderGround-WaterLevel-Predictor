# app/components/visual_3d.py

import plotly.graph_objects as go
import numpy as np

def groundwater_surface(z_value: float):
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    x, y = np.meshgrid(x, y)

    z = np.sin(x**2 + y**2) * 0.3 + z_value

    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorscale="Blues",
                showscale=False
            )
        ]
    )

    fig.update_layout(
        height=420,
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            xaxis_visible=False,
            yaxis_visible=False,
            zaxis_visible=False,
        ),
    )

    return fig
