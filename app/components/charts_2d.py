import numpy as np
import plotly.graph_objects as go

def groundwater_surface(predicted_level):
    """
    Creates a smooth 3D surface representing groundwater depth
    """

    # Create grid
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)

    # Surface depth influenced by prediction
    Z = predicted_level + 0.4 * np.sin(X) * np.cos(Y)

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=Z,
                colorscale="Blues",
                showscale=False
            )
        ]
    )

    fig.update_layout(
        title="3D Groundwater Depth Visualization",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Water Level (m)",
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig
