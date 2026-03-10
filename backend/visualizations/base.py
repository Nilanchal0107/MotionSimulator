"""
Visualization Base
Shared matplotlib setup and base64 export utility used by all graph modules.
"""

import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Apply a consistent style across all graphs
plt.style.use('seaborn-v0_8-darkgrid')

DEFAULT_DPI = 100
DEFAULT_FIGSIZE = (8, 6)


def fig_to_base64(fig, dpi: int = DEFAULT_DPI) -> str:
    """
    Convert a matplotlib Figure to a base64-encoded PNG data URI.

    Args:
        fig: The matplotlib Figure object
        dpi: Image resolution

    Returns:
        Data URI string: 'data:image/png;base64,...'
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_b64}"
