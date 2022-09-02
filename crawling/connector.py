import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='1234',
                             database='mydatabase',
                             cursorclass=pymysql.cursors.DictCursor)


with connection:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    #
    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "INSERT INTO book_list (barcode, name, author, publisher, pDate, review, rCnt, price " \
          "VALUES (%(barcode)s,%(name)s,%(author)s,%(publisher)s,%(pDate)s,%(review)s,%(rCnt)s,%(price)s))"

        cursor.execute(sql, (barcode, name, author, publisher, pDate, review, rCnt, price))
        cursor.commit()