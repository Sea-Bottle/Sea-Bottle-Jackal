Sea-Bottle-Jackal
=================

Искажение изображений (алгоритм Seam carving)
---------------------------------------------

*Задача:* получение из изображения искаженного изображения (видео).

Возможности искажателя
~~~~~~~~~~~~~~~~~~~~~~

* Загрузка изображения через web и получение искаженного изображения/видео на выходе с возможностью скачивания;
* Искажение изображения и его сохранение с помощью командной строки.
* Пример работы алгоритма:

До:

.. figure:: https://raw.githubusercontent.com/Sea-Bottle/Sea-Bottle-Jackal/master/examples/wolf.png
       :scale: 70 %
       :align: center


После:

.. image:: https://github.com/Sea-Bottle/Sea-Bottle-Jackal/raw/master/examples/wolf.gif
       :scale: 70 %
       :align: center

Зависимости
-----------

* ``fastapi``
* ``numpy``
* ``cv2``

Пользовательские интерфейсы
---------------------------

* web-интерфейс на HTML, CSS, JS;
* интерфейс командной строки.

Макет web-интерфейса
~~~~~~~~~~~~~~~~~~~~

Страница загрузки файла:

.. figure:: https://raw.githubusercontent.com/Sea-Bottle/Sea-Bottle-Jackal/master/examples/main.png
       :scale: 70 %
       :align: center


Страница с отслеживанием прогресса создания результата:

.. figure:: https://raw.githubusercontent.com/Sea-Bottle/Sea-Bottle-Jackal/master/examples/progress.png
       :scale: 70 %
       :align: center


Страница с результатом и возможностью скачивания:

.. figure:: https://raw.githubusercontent.com/Sea-Bottle/Sea-Bottle-Jackal/master/examples/result.png
       :scale: 70 %
       :align: center


Интерфейс командной строки
~~~~~~~~~~~~~~~~~~~~~~~~~~

``python -m jackalify [-h] [-w] [-g] [-o OUTPUT_PATH] [INPUT_PATH]``

Если не указан флаг ``-g``, то создастся статичная картинка. Также если не указано имя выходного файла, то искажённое изображение (или gif) будет создано рядом с исходной картинкой. Если не указан флаг ``-w``, то обязательно наличие входного файла, однако если флаг ``-w`` указан, никакие другие аргументы не должны присутствовать.

Опции:
""""""

* ``-h`` - помощь;
* ``-w`` - запуск серверного интерфейса (fastapi), опционально;
* ``-o`` - имя выходного файла, опционально;
* ``-g`` - создание gif вместо статичной картинки, опционально;
* ``INPUT_PATH`` - путь к файлу с оригинальным изображением, опционально.

Примеры:
""""""""

* ``python -m jackalify wolf.png -o wolf-jackal.png`` - получение искаженного изображения ``wolf-jackal.png``
* ``python -m jackalify wolf.png`` - получение искаженного изображения ``wolf_jackalified.png``
* ``python -m jackalify wolf.png -o wolf-jackal.gif -g`` - получение искаженного видео ``wolf-jackal.gif``
* ``python -m jackalify -w`` - запуск серверного интерфейса

При установке пакета через ``pip`` вместо ``python -m jackalify`` нужно вызывать ``jackalify``.
