from PyQt5.QtCore import QObject, pyqtSignal


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kwagrs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwagrs)
        return _instance[cls]

    return _singleton


@Singleton
class Signal_Center(QObject):
    _text = pyqtSignal(str)
    _signal = pyqtSignal(str)
    _row_and_col = pyqtSignal(str)

    def trigger_text(self, text):
        self._text.emit(text)

    def trigger_signal(self, signal):
        self._signal.emit(signal)

    def trigger_row_and_col(self, row_and_col_number):
        self._row_and_col.emit(row_and_col_number)

