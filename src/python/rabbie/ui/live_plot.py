from rabbie.database import DataBase
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.dates import date2num
from queue import Queue


class DataPlot:

    def __init__(self,
                 data_q: Queue=None,
                 update_interval: int=1000) -> None:
        self._data_in = data_q
        self.data = [(0.5, 0.5), (1, 1), (2, 2), (3, 3)]
        fig = plt.figure()
        ax = plt.axes()
        self.line, = ax.plot([], [], 'ro', animated=True)
        ani.FuncAnimation(self.fig,
                          self.update_plot,
                          interval=update_interval)
        plt.show()

    def init(self):
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, _):
        """
        Update data plot with new values
        """
        print('Updateing plot')
        self.ln.set_data([d[0] for d in self.data],
                         [d[1] for d in self.data], '-')

dp = DataPlot()
