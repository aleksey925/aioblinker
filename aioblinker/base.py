import asyncio
import threading
from functools import lru_cache
from inspect import iscoroutinefunction
from weakref import WeakValueDictionary

import blinker

GLOBAL_DATA = {
    # Event Loop is used for call receiver.
    'loop': asyncio.get_event_loop(),
    'loop_thread': threading.current_thread(),
}


def set_event_loop(loop):
    GLOBAL_DATA['loop'] = loop
    GLOBAL_DATA['loop_thread'] = threading.current_thread()


def get_event_loop():
    return GLOBAL_DATA['loop']


@lru_cache(maxsize=128)
def is_coroutine_func(func):
    return iscoroutinefunction(func)


class Signal(blinker.Signal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send(self, sender=None, **kwargs):
        """
        Emit this signal on behalf of *sender*, passing on **kwargs.
        :param sender: any object or None
        :param kwargs: data to be sent to receivers
        """
        if not self.receivers:
            return

        if GLOBAL_DATA['loop_thread'] is not threading.current_thread():
            receiver_call = self.thread_safe_receiver_call
        else:
            receiver_call = self.receiver_call

        ret = []
        ret_append = ret.append

        for receiver in self.receivers_for(sender):
            receiver_call(receiver, sender, ret_append, kwargs)

        return ret

    @staticmethod
    def thread_safe_receiver_call(receiver, sender, ret_append, kwargs):
        """
        Performs threadsafe сall receiver.
        :param receiver: receiver
        :param sender: sender
        :param ret_append: The method of the list. This method appends results
        of calling receiver to this list.
        :param kwargs: data to be sent to receivers
        """
        if is_coroutine_func(receiver):
            future = asyncio.run_coroutine_threadsafe(
                receiver(sender, **kwargs),
                GLOBAL_DATA['loop']
            )
            ret_append((receiver, future))
        else:
            callback_wrapper = GLOBAL_DATA['loop'].call_soon_threadsafe(
                lambda receiver_=receiver: receiver_(sender, **kwargs)
            )
            ret_append((receiver, callback_wrapper))

    @staticmethod
    def receiver_call(receiver, sender, ret_append, kwargs):
        """
        Делает вызов receiver потоко не безопасным способом. Используется,
        когда receiver вызывается из потока в котором создавался loop.
        :param receiver: receiver
        :param sender: sender
        :param ret_append: The method of the list. This method appends results
        of calling receiver to this list.
        :param kwargs: data to be sent to receivers
        """
        if is_coroutine_func(receiver):
            future = asyncio.ensure_future(
                receiver(sender, **kwargs),
                loop=GLOBAL_DATA['loop']
            )
            ret_append((receiver, future))
        else:
            ret_append((receiver, receiver(sender, **kwargs)))


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
