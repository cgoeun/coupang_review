class Product:
    def __init__(self, name="", price=0, rating=0.0, review=0):
        self.name = name
        self.price = price
        self.rating = rating
        self.review = review

    def __str__(self):
        print(f"name = {self.name}, price = {self.price}, rating = {self.rating}, review = {self.review}")
        return ""
