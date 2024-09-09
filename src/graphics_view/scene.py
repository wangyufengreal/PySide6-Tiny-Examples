"""自定义 scene
"""

from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import QEvent

class CustomGraphicsScene(QGraphicsScene):
  """自定义 QGraphicsScene, 方便未来的更多的自定义的行为
  """

  def __init__(self, x, y, w, h, parent=None):
    QGraphicsScene.__init__(self, x, y, w, h, parent)

  def eventFilter(self, obj, event): # 重写事件: pylint: disable=invalid-name

    if event.type() == QEvent.Type.GraphicsSceneMouseMove:
      pass
    elif event.type() == QEvent.Type.GraphicsSceneMousePress:
      pass
    elif event.type() == QEvent.Type.GraphicsSceneMouseRelease:
      pass

    return super().eventFilter(obj, event)
