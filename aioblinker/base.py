import asyncio
import inspect
from weakref import WeakValueDictionary

import blinker

GLOBAL_DATA = {
    # Event loop используемый для вызова receiver. Нужен для поддержки
    # сопрограмм и чтобы receiver выполнялся в главном потоке, а не потоке
    # из которого вызывался сигнал (актуально для ситуации, когда сигнал
    # вызывается из дочернего потока, а обработчик должен отработать
    # в главном потоке).
    'loop': asyncio.get_event_loop()
}


def set_event_loop(loop):
    GLOBAL_DATA['loop'] = loop


def get_event_loop():
    return GLOBAL_DATA['loop']


class Signal(blinker.Signal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send(self, sender=None, **kwargs):
        """
        Отправляет сигнал от имени sender, передавая получателю **kwargs
        :param sender: Любой объект или None
        :param kwargs: данные, которые будут отправленны в receivers
        """
        if not self.receivers:
            return

        ret_value = []
        ret_value_append = ret_value.append

        for receiver in self.receivers_for(sender):
            if inspect.iscoroutinefunction(receiver):
                future = asyncio.run_coroutine_threadsafe(
                    receiver(sender, **kwargs),
                    GLOBAL_DATA['loop']
                )
                ret_value_append((receiver, future))
            else:
                callback_wrapper = GLOBAL_DATA['loop'].call_soon_threadsafe(
                    lambda receiver_=receiver: receiver_(sender, **kwargs)
                )
                ret_value_append((receiver, callback_wrapper))

        return ret_value


class NamedSignal(Signal):

    def __init__(self, name, doc=None):
        Signal.__init__(self, doc)

        self.name = name

    def __repr__(self):
        base = Signal.__repr__(self)
        return "%s; %r>" % (base[:-1], self.name)


class Namespace(dict):

    def signal(self, name, doc=None):
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


class WeakNamespace(WeakValueDictionary):

    def signal(self, name, doc=None):
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


signal = Namespace().signal
