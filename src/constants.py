from PySide2.QtGui import QColor
import os
from pathlib import Path
RESOURCE_PATH = os.path.join(Path(os.path.dirname(__file__)).parent, "resources")

class Color:
    DARK_GREY = QColor(40, 40, 40)
    LIGHT_GREY = QColor(138, 138, 138)
    WHITE = QColor(255,255,255)