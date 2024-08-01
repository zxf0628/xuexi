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
    _Tedit_chat = pyqtSignal(str)
    _ComboBox_select_target = pyqtSignal(str)
    _StatusBar_signal = pyqtSignal(str)
    _QMessageBox = pyqtSignal(str)

    def trigger_Tedit_chat(self, chat_str):
        self._Tedit_chat.emit(chat_str)

    def trigger_ComboBox_select_target(self, host_name_str):
        self._ComboBox_select_target.emit(host_name_str)

    def trigger_StatusBar_signal(self, message_str):
        self._StatusBar_signal.emit(message_str)

    def trigger_QMessageBox(self,hint):
        self._QMessageBox.emit(hint)