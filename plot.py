import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class ScrollingPlot:
    def __init__(self, qplot, plot_type, sample_rate=1):
        self.q = qplot
        self.type = plot_type
        self.xd = 0
        self.sample_rate = sample_rate
        self.xlabel = None
        self.ylabel = None
        self.xunit = None
        self.yunit = None
        self.xunit_prefix = None
        self.yunit_prefix = None
        self.yd = np.empty(100)
        self.time_elapsed = 0
        self.ctime = 0
        if self.type == 'accumulate':
            self.update = self._accumulate_update
            self.setup = self._accumulate
        elif self.type == 'move':
            self.update = self._move_update
            self.setup = self._move

    def set_label(self, axis, text=None, unit=None, unit_prefix=None):
        """ axis: x/y"""
        if axis == 'x':
            self.xlabel = text
            self.xunit = unit
            self.xunit_prefix = unit_prefix
        elif axis == 'y':
            self.ylabel = text
            self.yunit = unit
            self.yunit_prefix = unit_prefix
        else:
            print 'ERROR: axis can only be x/y'

    def _accumulate(self):
        self.plt.setDownsampling(mode='peak')
        self.plt.setClipToView(True)
        self.plt.setLabel('left', text=self.xlabel, units=self.xunit)
        self.plt.setLabel('bottom', text=self.ylabel, units=self.yunit)
        self.curve = self.plt.plot(pen='y')

    def _move(self):
        self.curve = self.plt.plot(pen='y')

    def _accumulate_update(self):
        while not self.q.empty():
            data = self.q.get()['data']
            #print data
            self.yd[self.xd] = data
            self.xd += 1
            if self.xd >= self.yd.shape[0]:
                y_tmp = self.yd
                self.yd = np.empty(self.yd.shape[0] * 2)
                self.yd[:y_tmp.shape[0]] = y_tmp
            # Used for finding sample rate
            #self.time_elapsed = self.ctime
            #self.ctime = time.time()
            #self.time_elapsed = self.ctime - self.time_elapsed
            #print self.time_elapsed
            #self.curve.setPos(0, self.xd/20)
            self.xdd = np.linspace(1, self.xd, num=self.xd)/self.sample_rate
            self.curve.setData(self.xdd[:self.xd], self.yd[:self.xd])

    def _move_update(self):
        while not self.q.empty():
            data = self.q.get()['data']
            self.yd[:-1] = self.yd[1:]
            self.yd[-1] = data
            self.xd += 1
            self.curve.setData(self.yd)

    def _plot(self):
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Plot')
        self.plt = self.win.addPlot()
        self.setup()

    def run(self):
        self._plot()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start()

        QtGui.QApplication.instance().exec_()

"""
class StaticPlot:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def add_overlayplot(self, data1, data2):
        win = pg.GraphicsWindow()
        win.setWindowTitle()
        plt1 = win.addPlot()
        plt2 = win.addPlot()
        plt1.plot(data1, pen='y')
        plt2.plot(data2, pen='r')

    def add_newplot(self, data1, data2):
        win = pg.GraphicsWindow()
        win.setWindowTitle()
        plt.plot(data1, pen='y')

    def run(self, data1, data2, plot_type='overlay'):
        self.add_newplot(data1, data2)

        QtGui.QApplication.instance().exec_()
"""
