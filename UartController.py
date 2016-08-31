import serial
import io
import threading
import time
import logging
from multiprocessing import Queue
from multiprocessing import RLock

class uart:

    def __init__(self, port = 1, baudrate = 115200,  log =  False):
        self.__keywords = []
        self.monitor_string = None
        self.__port = port
        self.__serial = serial.serial_for_url(
        "COM{num}".format(num = self.__port),
        baudrate,
        parity = 'N',
        rtscts = False,
        xonxoff = False,
        timeout = 1,
        do_not_open = True)
        self.__serial.open()
        self.__serial_io = io.TextIOWrapper(io.BufferedRWPair(self.__serial, self.__serial))
        self.__cmd_queue = Queue()
        self.__rx_thread = threading.Thread(target = self.__read_thread, name = "rx_thread")
        self.__rx_thread.setDaemon(True)
        self.__rx_thread.start()
        self.__tx_thread = threading.Thread(target = self.__write_thread, name = "tx_thread")
        self.__tx_thread.setDaemon(True)
        self.__tx_thread.start()
        self.__mutex = RLock()
        self.__log = log
        self.__is_monitor_rx_enable = False
        self.__echo_method = None
        if log is True:
            ltime = time.localtime(time.time())
            logging.basicConfig(filename = "log_{mon}_{date}_{h}_{m}_{s}.txt".format(mon = str(ltime.tm_mon).zfill(2), date =str(ltime.tm_mday).zfill(2), h =  str(ltime.tm_hour).zfill(2), m = str(ltime.tm_min).zfill(2), s = str(ltime.tm_sec).zfill(2)),
                level = logging.DEBUG)

    def set_echo_function(self, method):
        self.__echo_method = method
    def __read_thread(self):
        while(True):
            data = self.__serial_io.readline()
            if (len(data)):
                #print(data)
                if self.__echo_method is not None:
                    self.__echo_method(data)
                if self.__log is True:
                    logging.info("[RX]"+str(data))
            self.__monitor_rx_string_method(data)

    def __write_thread(self):
        while(True):
            if not self.__cmd_queue.empty():
                send_data = self.__cmd_queue.get()
                self.__serial_io.write(send_data)
                self.__serial_io.flush()
                if self.__log is True:
                    logging.info("[TX]"+str(send_data))
            time.sleep(0.05)

    def __monitor_rx_string_method(self, data):
        self.__mutex.acquire()
        if self.__is_monitor_rx_enable is True:
            if self.__isMatchString(data) is True:
                self.__is_monitor_rx_enable = False
        self.__mutex.release()

    def __isMatchString(self, data):
        is_hit_string = False
        for keyword in self.__keywords:
            if re.search(keyword, data):
                is_hit_string = True
                break
        return is_hit_string

    def Send(self, content, wait_string_list = [], wait_string_timeout = 0):
        assert isinstance(content, str) is True, 'content is not string'
        assert type(wait_string_list) is list, 'wait_string_list must be list'
        if len(wait_string_list) > 0:
            self._update_keywords(wait_string_list)
            self.__cmd_queue.put(content)
            start_time = time.time()
            while self.__is_monitor_rx_enable is True:
                if timeout is not 0:
                    if (time.time() - start_time >= timeout):
                        break
            if self.__is_monitor_rx_enable is True:
                self.__mutex.acquire()
                self.__is_monitor_rx_enable = False
                self.__mutex.release()
                return False
            return True
        else:
            self.__cmd_queue.put(content)
            return True

    def Connect(self):
        if (self.__serial.isOpen() == False):
            self.__serial.open()

    def Disconnect(self):
        self.__serial.close()

    def _update_keywords(self, string_list):
        self.__mutex.acquire()
        self.__keyworks = string_list
        self.__is_monitor_rx_enable = True
        self.__mutex.release()

    def WaitString(self,  string_list, timeout = 0):
        assert type(string_list)  is list, 'string_list must be list'
        assert len(string_list) > 0, 'what string you want to wait'
        assert self.__is_monitor_rx_enable is False, '__is_monitor_rx_enable is True'
        start_time = time.time()
        self._update_keywords()
        while self.__is_monitor_rx_enable is True:
            if timeout is not 0:
                if (time.time() - start_time >= timeout):
                    break
        if self.__is_monitor_rx_enable is True:
            self.__mutex.acquire()
            self.__is_monitor_rx_enable = False
            self.__mutex.release()
            return False
        return True
