import mysql.connector as sql
import datetime
import csv
import os
import sys


def get_stud_id():
    try:
        stud_id = int(input("Enter the student id: "))
        stud_name = input("Enter the student name: ")
        ret_id = [x.lower().capitalize() for x in stud_name.split(" ")]
        ret_id.insert(0, str(stud_id))
        return "_".join(ret_id)
    except ValueError:
        sys.exit("Student ID should be a number")


def stud_check(cur, stud_id):
    cur.execute("show tables;")
    x= [y[0] for y in cur]
    if stud_id in x:
        return True
    if stud_id not in x:
        return False


def date_check(date):
    date = date.split("/")
    if date != [""]:
        month = int(date[1])
        year = int(date[2])
        day = int(date[0])
        cur_date = [
            datetime.datetime.now().year,
            datetime.datetime.now().month,
            datetime.datetime.now().day,
        ]
        day_dict = {
            1: 31,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            day_dict[2] = 29
        else:
            day_dict[2] = 28

        # checks if year is greater than 1900 and less than or equal to the current year
        if 1900 <= year <= cur_date[0]:
            # checks is month input is a valid month lies in 1 , 12
            if month in day_dict:
                # checks if date is valid according to input month
                if day in range(1, day_dict[month] + 1):
                    # if year is current year then checks if user is not inputting future marks
                    if year == cur_date[0]:
                        if month <= cur_date[1]:
                            if day <= cur_date[2]:
                                return True
                            else:
                                return False
                        else:
                            return False
                    elif year < cur_date[0]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


def add_stud(cur):
    stud_name = input("Enter stud name: ").split(" ")
    stud_name=[x.lower().capitalize() for x in stud_name]
    cur.execute("show tables;")
    students = cur.fetchall()
    stud_id = len(students) + 1
    stud_name.insert(0, str(stud_id))
    stud_id = "_".join(stud_name)
    cur.execute(
        "create table {} (Date varchar(10), Marks integer,Subject char(20), Pattern char(3));".format(
            stud_id
        )
    )
    db.commit()
    print("Student Table created, would you like to add records to the table")
    cmd = input("(Y/N)==>")
    if cmd.lower() == "y":
        update_stud(cur, stud_id)
    elif cmd.lower() == "n":
        print("Returning you to the main menu")
    else:
        print("Invalid Option Selected, please select one of Y or N")


def update_stud(cur, stud_id):
    sub_list = ["Physics", "Chemistry", "Maths", "English", "Computer"]
    pat_list = ["Sub", "Obj"]
    if stud_check(cur, stud_id):
        n = int(input("Enter the number of tests: "))
        for i in range(n):
            date = input("Enter the date of test (DD/MM/YYYY): ")
            if date_check(date):
                subj = sub_list[
                    int(
                        input(
                            "Please select the subject:\n1. Physics\n2. Chemistry\n3. Maths\n4. English\n5. Computer\n==>"
                        )
                    )
                    - 1
                ]
                marks = int(input("Enter the marks(%): "))
                if marks in range(0, 101):
                    pat = pat_list[
                        int(
                            input(
                                "Please select the pattern of the test:\n1. Subjective\n2. Objective\n==>"
                            )
                        )
                        - 1
                    ]
                    cur.execute(
                        'insert into {} values ("{}","{}","{}","{}");'.format(
                            stud_id, date, str(marks), subj, pat
                        ),
                    )
                    print("Record Added Successfully")
                    db.commit()
                else:
                    print(
                        "Please check the marks you have entered, make sure the marks are in percentage form"
                    )
            elif not date_check(date):
                print(
                    "Please check your date, make sure the date is entered in the format DD/MM/YYYY\nEnsure you use '/'(Forward slash) not ''(Back slash) or '-'(Dash)"
                )
    elif not stud_check(cur, stud_id):
        print(
            "Student does not exist please create a new entry or check the data entered"
        )


def retrive_stud(cur, stud_id):
    stud_name = stud_id.split("_")
    stud_name.pop(0)
    stud_name = " ".join(stud_name)
    cur.execute("select * from {};".format(stud_id))
    dat = [i for i in cur]
    dates = [i[0] for i in dat]
    marks = [i[1] for i in dat]
    subj = [i[2] for i in dat]
    pat = [i[3] for i in dat]
    print("+" + ("-" * 10 + "+") * 5)
    print("|{:^54}|".format(stud_name.capitalize()))
    print("+" + ("-" * 10 + "+") * 5)
    print(
        "|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format(
            "Sr No.", "Date", "Marks", "Subject", "Pattern"
        )
    )
    print("+" + ("-" * 10 + "+") * 5)
    for i in range(len(dat)):
        print(
            "|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format(
                i + 1,
                dates[i],
                marks[i],
                subj[i],
                pat[i],
            )
        )
        print("+" + ("-" * 10 + "+") * 5)
    return dat


def delete_stud(cur, stud_id):
    if stud_check(cur, stud_id):
        print("Would you like to\n1. Delete all records\n2. Delete certain records")
        cmd = int(input("==>"))
        if cmd == 1:
            cur.execute("drop table {}".format(stud_id))
        elif cmd == 2:
            data = retrive_stud(cur, stud_id)
            del_rec = int(input("Which record would you like to delete?\n==>"))
            if del_rec in range(1, len(data) + 1):
                date = [i[0] for i in data][del_rec - 1]
                marks = [i[1] for i in data][del_rec - 1]
                subj = [i[2] for i in data][del_rec - 1]
                pat = [i[3] for i in data][del_rec - 1]
                cur.execute(
                    'delete from {} where date="{}" and marks="{}" and subject ="{}" and pattern="{}"'.format(
                        stud_id, date, str(marks), subj, pat
                    )
                )
                db.commit()
                print(
                    "Record Deleted\n"
                    + "+"
                    + ("-" * 10 + "+") * 4
                    + "\n"
                    + "|{:^10}|{:^10}|{:^10}|{:^10}|".format(date, marks, subj, pat)
                    + "\n+"
                    + ("-" * 10 + "+") * 4
                    + "\nRecord deleted successfully!",
                )

    else:
        print("Student does not exist, nothing to delete")


def add_csv(cur, stud_id):
    if stud_check(cur, stud_id):
        path = input("Enter the path of the csv file: ")
        with open(path, "r") as f:
            csv_read_file = csv.reader(f)
            rows = list(csv_read_file)
            rows.pop(0)
            for j in rows:
                if date_check(j[0]):
                    cur.execute(
                        'insert into {} values ("{}","{}","{}","{}");'.format(
                            stud_id, j[0], j[1], j[2], j[3]
                        )
                    )
                    db.commit()
                else:
                    print(
                        "Please check the date you have entered for row no.",
                        rows.index(j) + 1,
                        "and retry",
                    )
                    break
    else:
        print(
            "Student",
            stud_id.capitalize(),
            "does not exist, would you like to add a new student with the same name: ",
        )
        cmd = input("(Y/N)==>")
        if cmd.lower() == "y":
            cur.execute(
                "create table {} (Date varchar(10), Marks integer,Subject char(20), Pattern char(3));".format(
                    stud_id
                )
            )
            add_csv(cur, stud_id)
        elif cmd.lower() == "n":
            print("Returning you to the main menu")
        else:
            print("Invalid Option Selected, please select one of Y or N")


def export_csv(cur, stud_id):
    cur.execute("select * from {};".format(stud_id))
    path = os.getcwd() + "/{}_marks.csv".format(stud_id)
    with open(path, "w") as f:
        f.writelines(["Date, Marks, Subject, Pattern\n"])
        for i in cur:
            i = [str(x) for x in i]
            f.writelines(",".join(i) + "\n")


def menu(cur):
    print(
        """
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |  ________    | || |   ______     | || | ____    ____ | || |    _______   | |
| |   /  ___  |  | || | |_   ___ `.  | || |  |_   _ \    | || ||_   \  /   _|| || |   /  ___  |  | |
| |  |  (__ \_|  | || |   | |   `. \ | || |    | |_) |   | || |  |   \/   |  | || |  |  (__ \_|  | |
| |   '.___`-.   | || |   | |    | | | || |    |  __'.   | || |  | |\  /| |  | || |   '.___`-.   | |
| |  |`\____) |  | || |  _| |___.' / | || |   _| |__) |  | || | _| |_\/_| |_ | || |  |`\____) |  | |
| |  |_______.'  | || | |________.'  | || |  |_______/   | || ||_____||_____|| || |  |_______.'  | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
"""
    )
    stat = True
    menu_str = "Options:\n1. Add a new Student\n2. Insert Student Records\n3. Retrive Student Record\n4. Delete Student Records\n5. Add Student Records via CSV\n6. Export Student Records to CSV\n7. Exit"
    while stat:
        print(menu_str)
        cmd = int(input("==>"))
        if cmd in range(1, 8):
            if cmd == 1:
                add_stud(cur)
            elif cmd == 2:
                update_stud(cur, get_stud_id())
            elif cmd == 3:
                retrive_stud(cur, get_stud_id())
            elif cmd == 4:
                delete_stud(cur, get_stud_id())
            elif cmd == 5:
                add_csv(cur, get_stud_id())
            elif cmd == 6:
                export_csv(cur, get_stud_id())
            elif cmd == 7:
                print("Exiting! Have a nice day!")
                stat = False
        else:
            print("Invalid Option")


db = sql.connect(
    host="localhost", user="root", passwd="sql@racl5261436c", database="cs_final_project"
)
sql_cur = db.cursor()
menu(sql_cur)
