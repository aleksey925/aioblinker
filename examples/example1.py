# Пример использования aioblinker в PyQt приложении для обмена данными между
# разными потоками
import asyncio
import sys
import threading
import time

from PyQt5 import QtWidgets
from aioblinker import signal, set_event_loop
from quamash import QEventLoop


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


@thread
def processing():
    """
    Эмулирует затратную по времени операцию
    """
    print('worker thread: ', threading.current_thread().getName())
    res = [i for i in 'some data']
    time.sleep(5)
    signal('worker_complete').send(data=res)


class MyWidget(QtWidgets.QWidget):

    worker_complete = signal('worker_complete')

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.but_start = QtWidgets.QPushButton('Начать обработку данных', self)
        self.mainLayout.addWidget(self.but_start)

        self.but_start.clicked.connect(lambda i: processing())

        # Обработчик сигнала
        self.worker_complete.connect(self.worker_handler)

    def worker_handler(self, sender, data):
        print('handler thread: ', threading.current_thread().getName())
        print('Получены данные: ', data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)

    # aioblinker должен знать в каком event loop работает приложение
    asyncio.set_event_loop(loop)
    set_event_loop(loop)

    print('main thread: ', threading.current_thread().getName())

    window = MyWidget()
    window.show()

    with loop:
        loop.run_forever()
