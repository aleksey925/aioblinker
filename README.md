aioblinker
==========

**[ENG]**

aioblinker is an extension for the blinker library (https://github.com/jek/blinker),
which expands the possibilities of the original implementation.

Features:
- allows to use the coroutines as signal receivers;
- when a signal is called from a child thread, the signal recipient will 
be executed in the event loop thread;
- in the Signal.send method, the sender argument is optional and is set to 
None by default.

## Performance

aioblinker works a little slower then blinker because of overhead from event loop. 
aioblinker analyzes necessity of using event loop and use it only if it's needed.

## Comparison of performance blinker and aioblinker

aioblinker works slower than blinker:

- ~9% (when sending signals within a single thread);
- ~353% (when sending signals from a child thread to the main thread).

P.S. measurements were made with the help of `timeit`.

## Examples

Examples can be found in the example folder, which is located at the root of 
the repository.


**[RU]**

aioblinker - расширение для библиотеки blinker (https://github.com/jek/blinker),
которое дополняет возможности оригинальной реализации.

Особенности:

- позволяет использовать сопрограммы в качестве приемников сигналов;
- при вызове сигнала из дочернего потока, получатель сигнала будет выполняться
в потоке event loop, а не в дочернем, откуда производилась отправка сигнала;
- в методе Signal.send аргумент sender сделан необязательным и по умолчанию 
имеет значение None.

## Производительность

aioblinker работает немного медленнее blinker, эта цена которую приходится 
 платить, за возможность потокобезопасно пробрасывать из дочернего потока в 
 главный вызовы получателей и поддержку сопрограмм.

Для увеличения производительности, aioblinker анализует, из какого потока 
происходит вызов сигнала, и использует потокобезопасную реализацию только при 
необходимости.

## Сранение производительности blinker и aioblinker

aioblinker работает медленние чем blinker примерно:

- на 9% (при отправке сигналов в рамках одного потока);
- на 353% (при отправке сигналов из дочернего потока в главный).

P.S. замеры производились при помощи `timeit`.

## Примеры

Примеры можно посмотреть в папке examples, которая находится в корне 
репозитория.


