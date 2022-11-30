import tkinter as TK
from tkinter import ttk
from tkinter import messagebox, filedialog
import os
import csv
import datetime


# this function forms lists from the string, each element of the list will be a word of the string(separated by a space)
def formList(lstStr):
    lsttemp = lstStr.strip().split(" ")
    return lsttemp


def showScores():
    def selectSubj(subj):
        scoreLvl = TK.Toplevel(showScore)
        scoreLvl.title(subj+" Marks")
        path = os.getcwd()+"/Storage/ScoreTracker/"+subj+".txt"
        with open(path, "r") as subjFile:
            dat = subjFile.readlines()
            l1=TK.Label(scoreLvl,text="Date",borderwidth=1, relief="groove", width=15)
            l2=TK.Label(scoreLvl,text="Pattern",borderwidth=1, relief="groove", width=15)
            l3=TK.Label(scoreLvl,text="Marks",borderwidth=1, relief="groove", width=15)
            for i in range(len(dat)):
                for j in range(1,len(dat[0].strip().split(" "))):
                    l = TK.Label(scoreLvl, text = dat[i].strip().split(" ")[j], borderwidth=1, relief="groove", width=15,)
                    l.grid(row=i+1,column=j, padx=5)
            l1.grid(row = 1, column=0,padx=5)
            l2.grid(row = 2,column=0,padx=5)
            l3.grid(row = 3,column=0,padx=5)
    showScore  = TK.Toplevel(root)
    showScore.title("View Past Scores")
    subjDropDown = ttk.Combobox(
        showScore,
        values=["Maths", "Physics", "Chemistry", "English", "Computer"],
        state="readonly",
        width=15,)
    subjSelectBtn = TK.Button(showScore, command=lambda: selectSubj(subjDropDown.get()), text="Select", width=15)
    subjDropDown.grid(row=0, column=0)
    subjSelectBtn.grid(row=0, column=1)
    subjDropDown.set("--Pick An Option--")


# Score Tracker Functions
def scoreTracker():
    def date_check(date):
        date = date.split("/")
        month = int(date[1])
        year = int(date[2])
        date = int(date[0])
        day_dict = {30:[4,6,9,11], 31:[1,3,5,7,8,10,12], 28:[2], 29:[2]}
        if year%4 == 0 and year%100 != 0 or year%400==0:
           day_dict.pop(28)
        else:
            day_dict.pop(29)
        if year>=1900 and year<=datetime.datetime.now().year: 
            if month in range(1,13):
                for i in day_dict:
                    if month in day_dict[i]:
                        if date in range(1,i+1):
                            return True
                        else: return False
            else: return False
        else: return False
    # this will rebuild the whole text file with the new scores that are added
    def rewrite(alpha):
        path = os.getcwd() + "/Storage/ScoreTracker/" + alpha[3] + ".txt"
        alpha.pop(3)
        with open(path, "w") as markObj:
            writeList = []
            for i in range(len(alpha)):
                tempstr = ""
                for j in alpha[i]:
                    tempstr = tempstr + str(j) + " "
                tempstr += "\n"
                writeList.append(tempstr)
            markObj.writelines(writeList)

    # this will add the new score to the list formed from the formList() function
    def add_CSV():
        file_loc = filedialog.askopenfilename()
        with open(file_loc, "r") as CSVFile:
            csvFile = list(csv.reader(CSVFile))
            csvFile.pop(0)
            for i in range(len(csvFile)):
                if not add(csvFile[i]):
                    messagebox.showerror("Error", "Data has been entered up to entry no. "+str(i)+".\nPlease check the format of date for rest of entries")
                    break
    def add(dat_lst):
        if date_check(dat_lst[0]):
            # this will get the current working directory and then will find the storage text files for the past scores
            path = os.getcwd() + "/Storage/ScoreTracker/" + dat_lst[1] + ".txt"
            with open(path, "r") as subFile:
                dat = subFile.readlines()
                datelst = formList(dat[0])
                patlst = formList(dat[1])
                marklst = formList(dat[2])
            datelst.append(dat_lst[0])
            marklst.append(dat_lst[3])
            patlst.append(dat_lst[2])
            a = [datelst, patlst, marklst, dat_lst[1]]
            rewrite(a)
            subList.set("--Pick An Option--")
            patternList.set("--Pick An Option--")
            dateInpt.delete(0, TK.END)
            marksInpt.delete(0, TK.END)
            return True
        else:
            messagebox.showerror("Error","Please check the date you have entered")
            return False


    scoreTracker = TK.Toplevel(root)
    scoreTracker.title("ScoreTracker")
    scoreTracker.configure(bg="gray")
    scoreTracker.state("normal")
    subList = ttk.Combobox(
        scoreTracker,
        values=["Maths", "Physics", "Chemistry", "English", "Computer"],
        state="readonly",
        width=25,
    )
    patternList = ttk.Combobox(
        scoreTracker, values=["Subj", "Obj"], state="readonly", width=25
    )
    dateInpt = TK.Entry(scoreTracker, width=28)
    marksInpt = TK.Entry(scoreTracker, width=28)
    dateLbl = TK.Label(scoreTracker, text="Date(DD/MM/YY): ", bg="gray")
    subLbl = TK.Label(scoreTracker, text="Subject: ", bg="gray")
    PatternLbl = TK.Label(scoreTracker, text="Pattern: ", bg="gray")
    MarksLbl = TK.Label(scoreTracker, text="Marks(Percentage out of 100:)", bg="gray")
    addBtn = TK.Button(
        scoreTracker,
        text="Add",
        command=lambda : add([dateInpt.get(),subList.get(),patternList.get(),marksInpt.get()]),
        width=50,
        background="gray",
        highlightcolor="gray",
        activebackground="gray",
        border=0.5,
    )
    backBtn = TK.Button(
        scoreTracker,
        text="Done",
        command=scoreTracker.destroy,
        width=50,
        background="gray",
        highlightcolor="gray",
        activebackground="gray",
        border=0.5,
    )
    addViaCSV = TK.Button(
        scoreTracker,
        text ="Add via CSV File",
        command = add_CSV,
        width=50,
        background="gray",
        highlightcolor="gray",
        activebackground="gray",
        border=0.5,)
    dateLbl.grid(row=0, column=0, padx=10, pady=5)
    dateInpt.grid(row=0, column=1, padx=10, pady=5)
    subLbl.grid(row=1, column=0, padx=10, pady=5)
    subList.grid(row=1, column=1, padx=10, pady=5)
    PatternLbl.grid(row=2, column=0, padx=10, pady=5)
    patternList.grid(row=2, column=1, padx=10, pady=5)
    MarksLbl.grid(row=3, column=0, padx=10, pady=5)
    marksInpt.grid(row=3, column=1, padx=10, pady=5)
    addBtn.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    backBtn.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
    addViaCSV.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
    subList.set("--Pick An Option--")
    patternList.set("--Pick An Option--")


root = TK.Tk()
root.title("Main Page")
root.geometry("700x700")
ScoreTrackerBtn = TK.Button(root, text="Add Test Scores", command=scoreTracker)
ScoreTrackerBtn.grid(row=0, column=0, padx="100", pady="100")
showScoresBtn = TK.Button(root, text="Show Past Scores", command=showScores)
showScoresBtn.grid(row=1, column=0, pady=100, padx=100)
root.mainloop()
