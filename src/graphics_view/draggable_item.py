"""自定义 items
"""
from typing import Union, Callable

from PySide6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QMenu
from PySide6.QtGui import QPixmap, QPainterPath
from PySide6.QtCore import Qt

from .line import LineManager


class DragablePixmapItem(QGraphicsPixmapItem):
  """自定义可拖拽 PixmapItem

  注1 (拖拽逻辑):
      检测到 item 被左键点击以后, 进入可拖拽模式, 左键松开以后, 退出可拖拽模式.
    在可拖拽模式中时, 长按左键并移动鼠标, 每次鼠标移动事件触发, 将 item 更新的
    位置更新至事件触发的鼠标的位置.
      具体实现是, 按下左键以后, 会保存此时的 item 和鼠标的位置, 然后每次鼠标移动
    事件触发, 会将新的鼠标位置与最初按下鼠标的位置的差值, 叠加到 item 最初按下鼠标
    时的位置上, 并将这个叠加过的位置, 作为 item 的新位置, 并重新执行渲染.
  """


  def __init__(
    self, img_path: str, x: float, y: float,
    is_shape_rect: bool = True, line_manager: Union[LineManager, None] = None,
    parent=None
  ):
    QGraphicsPixmapItem.__init__(self, QPixmap(img_path), parent)
    self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)

    self.setPos(x, y)

    self.is_shape_rect = is_shape_rect # 是否将 item 的形状定义为矩形, 默认是, 方便拖拽

    self.is_dragging = False # item 是否处于可拖拽模式
    self.pressed_mouse_point = None # 存储按下左键时鼠标的位置
    self.pressed_item_point = None # 存储按下左键时 item 的位置

    self.line_manager = line_manager # 保存线条管理器的引用, 以便在 item 位置变动时更新相关线条

    self.menu = QMenu()


  def add_menu_action(self, name: str, action_func: Callable):
    """添加菜单栏子项

    Args:
     - name: 菜单栏子项名称
     - action_func: 子项对应的行为
    """
    action = self.menu.addAction(name)
    action.triggered.connect(action_func)


  def shape(self):
    """获取 PixmapItem 的形状

    注: 
        默认情况下, 图片的透明部分不会算作, 所以在拖拽时, 如果点击到图片透明区域, 
      拖拽会失效. 因此, 我默认重写了 PixmapItem 的形状为矩形,  如果有特殊需求, 
      可以指定通过设置 self.is_shape_rect=False 恢复默认行为.
    """
    if self.is_shape_rect:
      path = QPainterPath()
      path.addRect(self.boundingRect())
      return path
    else:
      return QGraphicsPixmapItem.shape(self)


  def get_center(self):
    rect = self.boundingRect()
    item_center = rect.center() + self.pos()
    return item_center.x(), item_center.y()


  def mousePressEvent(self, event): # 重写事件 pylint: disable=invalid-name
    if event.button() == Qt.MouseButton.LeftButton:

      # 判断事件触发区域是否超过了 item 的宽高, 超过则不触发.
      # 这样写主要是考虑到了在某些情况下, 会出现事件在范围以外触发的情况.
      # 怀疑是 PySide6 的某些机制我未理解, 或者是单纯的 Bug.
      if not 0 < event.pos().x() < self.pixmap().rect().width() \
        or not 0 < event.pos().y() < self.pixmap().rect().height():
        event.accept()
        return

      self.is_dragging = True
      self.pressed_mouse_point = event.pos() + self.pos()
      self.pressed_item_point = self.pos()
      event.accept()
    elif event.button() == Qt.MouseButton.RightButton:

      if self.menu.isEmpty(): # 如果菜单为空, 不处理
        event.accept()
        return

      self.menu.exec_(event.screenPos())

      # 清空拖拽的上下文, 防止冲突
      self.is_dragging = False
      self.pressed_mouse_point = None
      self.pressed_item_point = None

      event.accept()
    else:
      event.accept()


  def mouseMoveEvent(self, event): # 重写事件 pylint: disable=invalid-name
    if self.is_dragging:
      if self.pressed_mouse_point is None or self.pressed_item_point is None:
        raise ValueError('pressed_mouse_point or pressed_item_point is None!')
      point_offset = event.pos() + self.pos() - self.pressed_mouse_point
      new_item_point = self.pressed_item_point + point_offset
      self.setPos(new_item_point)
      self.scene().update()

      if self.line_manager is not None:
        self.line_manager.lines_update()

      event.accept()
    else:
      event.accept()


  def mouseReleaseEvent(self, event): # 重写事件 pylint: disable=invalid-name
    if event.button() == Qt.MouseButton.LeftButton:
      self.is_dragging = False
      self.pressed_mouse_point = None
      self.pressed_item_point = None
      event.accept()
    else:
      event.accept()
