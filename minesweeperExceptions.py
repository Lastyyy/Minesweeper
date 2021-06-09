class BoardTooSmallException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class BoardTooBigException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class BombsAmountNotCorrectException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EmptyFieldException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class Game:
    def __init__(self, n, m, bombs):
        self.__n = n
        self.__m = m
        self.__bombs = bombs

    def CreateGame(self):
        if self.__n < 2 or self.__m <2:
            raise BoardTooSmallException("Jedna z wspolrzednych jest mniejsza od 2!")
        elif self.__n > 15 or self.__m > 15:
            raise BoardTooBigException("Jedna z wspolrzednych jest wiekszka od 15!")
        elif self.__bombs > (self.__n * self.__m) or self.__bombs < 0:
            raise BombsAmountNotCorrectException("Liczba bomb musi byc z zakresu <0, " + str(int(self.__n) * int(self.__m)) + ">!")
        elif str(self.__bombs) == '' or str(self.__n) == '' or str(self.__m) == "":
            raise EmptyFieldException("Zadne pole nie moze byc puste!")