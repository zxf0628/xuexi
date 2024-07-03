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
    _databases_name = pyqtSignal(str)
    _datalabel_name = pyqtSignal(str)
    _datalabel_column_name = pyqtSignal(str)
    _present_data = pyqtSignal(str)
    _statusBar = pyqtSignal(str)

    def trigger_databases_name(self, databases_name):
        print("Signal_Center->trigger_databases_name->触发信号中心信号 参数:{}".format(databases_name))
        self._databases_name.emit(databases_name)

    def trigger_datalabel_name(self, datalabel_name):
        print("Signal_Center->trigger_datalabel_name->触发信号中心信号 参数:{}".format(datalabel_name))
        self._datalabel_name.emit(datalabel_name)

    def trigger_datalabel_column_name(self, datalabel_column_name):
        print("Signal_Center->trigger_datalabel_column_name->触发信号中心信号 参数:{}".format(datalabel_column_name))
        self._datalabel_column_name.emit(datalabel_column_name)

    def trigger_present_data(self, data_text):
        print("Signal_Center->trigger_present_data->触发信号中心信号 参数:{}".format(data_text))
        self._present_data.emit(data_text)

    def trigger_statusBar(self, hint):
        print("Signal_Center->trigger_statusBar->触发信号中心信号 参数:{}".format(hint))
        self._statusBar.emit(hint)
