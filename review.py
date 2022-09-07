class Review:
    def __init__(self, rating=0, date="", seller="", content="", help=0):
        self.rating = rating
        self.date = date
        self.seller = seller
        self.content = content
        self.help = help

    def __str__(self):
        print(
            f"rating = {self.rating}, date = {self.date}, seller = {self.seller}, content = {self.content}, help = {self.help}")
        return ""
    
    def __iter__(self):
        return iter([self.rating, self.date, self.seller, self.content, self.help])
