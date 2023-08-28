## 11.4

1. Перепишите первый пример с двумя функциями, где мы вычитали или прибавляли число, так чтобы примитивом синхронизации был семафор. Что будет, если передать 2 как изначальное число для счётчика?
2. В стандартной библиотеке есть [ещё один тип семафора](https://docs.python.org/3/library/threading.html#threading.BoundedSemaphore), который может привнести чуть больше безопасности в нашу программу. Его суть в том, что если значение счётчика превысит его изначальное значение, то будет поднято исключение — очевидное указание на ошибку. Прочитайте документацию о нём и добавьте его в код.