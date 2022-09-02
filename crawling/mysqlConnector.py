import mysql.connector


def insert(book):
    mysql_con = mysql.connector.connect(host='localhost', port='3306', database='mydatabase', user='root',
                                        password='1234')
    mysql_cursor = mysql_con.cursor()

    sql = ("INSERT INTO book_list ('barcode', 'name', 'author', 'publisher', 'pDate', 'review', 'rCnt', 'price' " \
           "VALUES (%(barcode)s,%(name)s,%(author)s,%(publisher)s,%(pDate)s,%(review)s,%(rCnt)s,%(price)s)")

    param = {
        'barcode': book.barcode,
        'name': book.name,
        'author': book.author,
        'publisher': book.publisher,
        'pDate': book.pDate,
        'review': book.review,
        'rCnt': book.rCnt,
        'price': book.price,
    }

    mysql_cursor.execute(sql, param)

    mysql_con.commit()
    mysql_cursor.close()
