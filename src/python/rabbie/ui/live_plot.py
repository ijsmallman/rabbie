import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.dates import date2num
from queue import Queue, Empty
from typing import Tuple, List
from threading import Thread


from rabbie.database import DataBase


class LivePlot(Thread):
    """
    An animated time series scatter plot using matplotlib.animations.FuncAnimation
    """

    def __init__(self, 
                 data_buffer: Queue,
                 data_label: str='',
                 interval: int=200) -> None:
        """
        Create a live time series scatter plot using matplotib gui
        
        Parameters
        ----------
        data_buffer: queue.Queue
            (threadsafe) data input buffer
        data_label: str
            data label for plot
        interval: int
            time interval in ms between graph redraws
            (default: 200 ms)
        """
        super().__init__(target=self.show)
        self.daemon = True
        self.data_label = data_label
        self.data_buffer = data_buffer
        self.stream = self.data_stream()

        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('close_event', self.handle_close)
        self.ani = ani.FuncAnimation(self.fig, self.update, interval=interval, 
                                     init_func=self.setup_plot, blit=True)

        # This next variable is a work around for self.setup_plot being called twice
        self.initilized_plot = False

    def setup_plot(self) -> None:
        """
        Initial drawing of the scatter plot
        """
        if not self.initilized_plot:
            entries = next(self.stream)
            t, v = self.entries_to_plot_values(entries)
            self.scat, = self.ax.plot_date(t, v, '-', animated=True)
            self.scat.set_xlabel('Timestamp (UTC)')
            self.scat.set_ylabel(self.data_label)
            self.ax.autoscale(enable=True, axis='both')
            self.ax.relim()
            self.initilized_plot = True

        return self.scat,

    def entries_to_plot_values(self, entries: List[dict]) -> Tuple[Tuple[int], Tuple[float]]:
        """
        Convert database entries to two lists of values to be plotted
        
        Parameters
        ----------
        entries: List[dict]
            list of database entries where each entry contains the fields: 'measure-at' and 'value'

        Returns
        -------
        timestamps: Tuple[int]
            timestamps in unix time
        values: Tuple[float]
            values to be plotted
        """
        if entries:
            t, v = zip(*[(date2num(e['measured-at']), e['value']) 
                         for e in entries])
            return t, v
        else:
            return (), ()

    def data_stream(self) -> List[dict]:
        """
        Pull data from the data buffer to be plotted
        
        Returns
        -------
        entries: List[dict]
            database entries to be plotted
        """
        while True:
            try:
                data = self.data_buffer.get(block=False)
            except Empty:
                data = []
            yield data

    def update(self, _):
        """
        Update the scatter plot
        """
        entries = next(self.stream)

        if entries:
            t, v = self.entries_to_plot_values(entries)
            self.scat.set_data(t, v)
            self.ax.autoscale(enable=True, axis='both')
            self.ax.relim()
            #self.ax.xaxis_date()
            plt.draw()

        return self.scat,

    def handle_close(self, evt) -> None:
        pass

    def show(self) -> None:
        plt.show()
