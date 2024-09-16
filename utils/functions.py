import datetime





if __name__ == "__main__":

    d = datetime.date.today()
    print(type(d))

    str_date = date2str(d)
    print(str_date)

    d2 = str2date(str_date)
    print(d2)

    str_date = date2str(d)
    print(str_date)