from PyQt5.QtCore import QObject,pyqtSignal


def Singleton(cls):
    _instance={}
    def _singleton(*args,**kwagrs):
        if cls not in  _instance:
            _instance[cls]=cls(*args,**kwagrs)
        return _instance[cls]
    return _singleton

@Singleton
class Signal_Center(QObject):
    _Tedit_chat = pyqtSignal(str)
    _Ledit_input = pyqtSignal(str)
    _ComboBox_select_target = pyqtSignal(str)
    _StatusBar_signal = pyqtSignal(str)
    _flag = pyqtSignal(str)
    _send_info_c_to_c = pyqtSignal(str)
    _update_server_id = pyqtSignal(str)
    _send_info = pyqtSignal(str)

    def trigger_Tedit_chat(self,chat_str):
        self._Tedit_chat.emit(chat_str)

    def trigger_Ledit_input(self,info_str):
        self._Ledit_input.emit(info_str)

    def trigger_ComboBox_select_target(self,host_name_str):
        self._ComboBox_select_target.emit(host_name_str)

    def trigger_StatusBar_signal(self,message_str):
        self._StatusBar_signal.emit(message_str)

    def trigger_flag(self,flag):
        self._flag.emit(flag)

    def trigger_send_info_c_to_c(self,info):
        self._send_info_c_to_c.emit(info)

    def trigger_update_server_id(self,old_and_new_id):
        self._update_server_id.emit(old_and_new_id)

    def trigger_send_info(self,info):
        self._send_info.emit(info)