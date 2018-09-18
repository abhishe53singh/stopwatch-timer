from tkinter import *
import time


class StopWatch(Frame):
    """ Implements a stop watch frame widget.

    Implementing a new widget is almost always best done by subclassing Frame

    """
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.entry = 0
        self.scrollbar = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d-%b-%Y-%H-%M-%S", time.localtime())

    def makeWidgets(self):
        """ Make the Laps and File Labels. """
        filelable = Label(self, text='File Name')
        filelable.pack(fill=X, expand=NO, pady=1, padx=2)

        self.entry = Entry(self)
        self.entry.pack(pady=2, padx=2)

        lable = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        lable.pack(fill=X, expand=NO, pady=3, padx=2)

        laplable = Label(self, text='Laps')
        laplable.pack(fill=X, expand=NO, pady=46, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.scrollbar = Listbox(selectmode=EXTENDED, height=5,
                         yscrollcommand=scrollbar.set)
        self.scrollbar.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.scrollbar.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

    def Lap(self):
        '''Makes a lap, only if started'''
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.scrollbar.insert(END, self.laps[-1])
            self.scrollbar.yview_moveto(1)
            self.lapmod2 = self._elapsedtime

    def Save(self):
        '''Get the timer name and create a file to save the laps'''
        archive = str(self.entry.get()) + 'stopwatch'
        with open(archive + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))


def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)    # Enables always on top
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Lap', command=sw.Lap).pack(side=LEFT)
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Save', command=sw.Save).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)

    root.mainloop()


if __name__ == '__main__':
    main()
