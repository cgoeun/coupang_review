class Book:
    def __init__(self, barcode=0, name="", author="", pub="", pDate="", review=0, rCnt=0, price=0):
        self.barcode = barcode
        self.name = name
        self.author = author
        self.publisher = pub
        self.pDate = pDate
        self.review = review
        self.rCnt = rCnt
        self.price = price

    def __str__(self):
        print(
            f"barcode = {self.barcode}, name = {self.name}, author = {self.author}, publisher = {self.publisher}, pDate = {self.pDate}, review = {self.review}, rCnt = {self.rCnt}, price = {self.price}")
        return ""