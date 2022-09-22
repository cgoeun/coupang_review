class Review:
    def __init__(self, star=0, date="", review="", help=0):
        self.star = star
        self.date = date
        self.review = review
        self.help = help

    # def __str__(self):
    #     print(
    #         f"star = {self.star}, date = {self.date}, store = {self.store}, review = {self.review}, help = {self.help}")
    #     return ""
    
    # def __iter__(self):
    #     return iter([self.star, self.date, self.store, self.review, self.help])
