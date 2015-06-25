import sys

from PyQt4 import QtCore
from PyQt4 import QtGui


class BezierLine(QtGui.QWidget):
	"""A bezier line connecting two points."""
	def __init__(self, start, end, parent=None):
		"""Initialize a bezier path.

		:param start: The start point.
		:param end: The end point.
		"""
		super(BezierLine, self).__init__(parent)
		self._start = start
		self._end = end
		self._generatePath()

	def _generatePath(self):
		self._path = QtGui.QPainterPath()
		self._path.moveTo(self._start)
		self._pen_width = 5
		center_x = (self._start.x()+self._end.x())*0.5
		self._path.cubicTo(
			QtCore.QPointF(center_x, self._start.y()),
			QtCore.QPointF(center_x, self._end.y()),
			self._end)
		self.setMinimumSize(
			abs(self._start.x()-self._end.x())+self._pen_width*2,
			abs(self._start.y()-self._end.y())+self._pen_width*2)

	def setStartPoint(self, start):
		self._start = start
		self._generatePath()
		self.update()

	def setEndPoint(self, end):
		self._end = end
		self._generatePath()
		self.update()

	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)
		pen = QtGui.QPen()
		pen.setCapStyle(QtCore.Qt.RoundCap)
		pen.setWidth(self._pen_width)
		painter.setPen(pen)
		painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
		painter.drawPath(self._path)
		painter.end()


class Container(QtGui.QWidget):
	"""Item Container."""
	def __init__(self, parent=None):
		super(Container, self).__init__(parent)
		self._line = BezierLine(QtCore.QPointF(10, 10), QtCore.QPointF(600, 400), self)
		self._line.move(0, 0)
		self.adjustSize()

	def mouseMoveEvent(self, event):
		if event.buttons() == QtCore.Qt.LeftButton:
			self._line.setStartPoint(event.pos())
		elif event.buttons() == QtCore.Qt.RightButton:
			self._line.setEndPoint(event.pos())


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		scroll_area = QtGui.QScrollArea()
		self.setCentralWidget(scroll_area)
		scroll_area.setWidget(Container())
		scroll_area.setWidgetResizable(False)


def main():
	app = QtGui.QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
