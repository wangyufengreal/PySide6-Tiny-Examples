"""线条相关
"""

import enum
from typing import List

from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsScene
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt


class LineTrackWay(enum.IntEnum):
  """线的存在方式的定义
  """

  TWO_POINT = 0 # 两个固定点确定一条直线
  ITEM_WITH_PINED_POINT = 1 # item 和一个固定点确定一条直线
  TWO_ITEM = 2 # 两个 item 确定一条直线

  UNDEFINED = 99 # 未定义


class StraightLineItem(QGraphicsLineItem):
  """直线 item, 在 GraphicsScene 中作为直线

  注 1: 通过 LineTrackWay 定义线的存在方式.

  Args:
    **kwargs:

      LineTrackWay.TWO_POINT 方式所需参数
      - start_point (list or tuple): 起始点
      - end_point (list or tuple): 结束点

      LineTrackWay.ITEM_WITH_PINED_POINT 方式所需参数
      - start_item (DragablePixmapItem): 可拖拽的 item, 作为起始
      - end_point (list): 结束点

      track_way == LineTrackWay.TWO_ITEM 方式所需参数
      - start_item (DragablePixmapItem): 可拖拽的 item, 作为起始
      - end_item (DragablePixmapItem): 可拖拽的 item, 作为结束
  """

  def __init__(
    self, track_way: LineTrackWay = LineTrackWay.TWO_POINT, parent=None,
    **kwargs
  ):
    super().__init__(parent)
    # 线风格定义
    self.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))

    # //////////////////////////////
    ### 功能支持 1: 线的存在方式 ###
    # ///////////////////////////
    self.track_way = track_way

    # 存储必须的信息
    self.start_point = None
    self.end_point = None
    self.start_item = None
    self.end_item = None

    # 线条的信息获取与初始化
    if track_way == LineTrackWay.TWO_POINT: # 两个固定点确定一条直线
      self.start_point = kwargs.get('start_point', None)
      self.end_point = kwargs.get('end_point', None)

      if not isinstance(self.start_point, (list, tuple)):
        raise ValueError('LineTrackWay.TWO_POINT 起始点坐标 (start_point) 不正确!')
      if not isinstance(self.end_point, (list, tuple)):
        raise ValueError('LineTrackWay.TWO_POINT 结束点坐标 (end_point) 不正确!')

      self.setLine(
        self.start_point[0], self.start_point[1],
        self.end_point[0], self.end_point[1]
      )

    elif track_way == LineTrackWay.ITEM_WITH_PINED_POINT: # item 和一个固定点确定一条直线
      self.start_item = kwargs.get('start_item', None)
      self.end_point = kwargs.get('end_point', None)

      if not isinstance(self.start_item, QGraphicsItem):
        raise ValueError(
          'LineTrackWay.ITEM_WITH_PINED_POINT 起始 item (start_item) 不正确!'
        )
      if not isinstance(self.end_point, (list, tuple)):
        raise ValueError(
          'LineTrackWay.ITEM_WITH_PINED_POINT 结束点坐标 (end_point) 不正确!'
        )

      self.setLine(
        self.start_item.get_center()[0], self.start_item.get_center()[1],
        self.end_point[0], self.end_point[1]
      )

    elif track_way == LineTrackWay.TWO_ITEM: # 两个 item 确定一条直线
      self.start_item = kwargs.get('start_item', None)
      self.end_item = kwargs.get('end_item', None)

      if not isinstance(self.start_item, QGraphicsItem):
        raise ValueError(
          'LineTrackWay.TWO_ITEM 起始 item (start_item) 不正确!'
        )
      if not isinstance(self.end_item, QGraphicsItem):
        raise ValueError(
          'LineTrackWay.TWO_ITEM 结束 item (end_item) 不正确!'
        )

      self.setLine(
        self.start_item.get_center()[0], self.start_item.get_center()[1],
        self.end_item.get_center()[0], self.end_item.get_center()[1],
      )

    else:
      raise ValueError('Unsupported Line Track Way!')


  def line_update(self):

    if self.track_way == LineTrackWay.TWO_POINT:
      self.setLine(
        self.start_point[0], self.start_point[1],
        self.end_point[0], self.end_point[1],
      )

    elif self.track_way == LineTrackWay.ITEM_WITH_PINED_POINT:
      self.setLine(
        self.start_item.get_center()[0], self.start_item.get_center()[1],
        self.end_point[0], self.end_point[1],
      )

    elif self.track_way == LineTrackWay.TWO_ITEM:
      self.setLine(
        self.start_item.get_center()[0], self.start_item.get_center()[1],
        self.end_item.get_center()[0], self.end_item.get_center()[1],
      )

    else:
      raise ValueError('Unsupported Line Track Way to perform update ops!')

    self.scene().update()


class LineManager:
  """线条管理器

  描述: 添加, 更新线条
  """

  def __init__(self):

    self.lines: List[StraightLineItem] = []


  def add_line(self, scene: QGraphicsScene, line: StraightLineItem):
    scene.addItem(line)
    scene.update()
    self.lines.append(line)


  def lines_update(self):
    for line in self.lines:
      line.line_update()
