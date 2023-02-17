import tkinter
from tkinter import *
import pandas as pd
from tkinter import font as tkFont

aird_data = pd.read_csv(r"C:\Users\josha\AirCharacteristics\airData.csv")

##SIMULATION
def runmodel():
    if shape.get() == "Toroidal":
        paracd = 2.2
        avt = 2  ##area vs time relationship
        cfc = 8  ## canopy fill constant for inflation time calculations
    elif shape.get() == "Parabolic":
        paracd = .97
        avt = 1
        cfc = 11.7
    cds = ((((float(e1.get())) / 2) ** 2) * 3.1415926) * paracd
    vls = float(e3.get())
    tf = ((float(e1.get())) * cfc) / vls
    tflabel.set(("%.2f" % tf)+" s")
    weight = float(e2.get())
    depAlt = float(e4.get())
    landAlt = float(e5.get())
    landAird = float(aird_data[aird_data["Altitude"] > landAlt].iloc[0]["Density"])

    fdr = ((2 * weight) / (landAird * cds)) ** .5
    fdrlabel.set(("%.1f" % fdr)+" ft/s")

    ti = .005
    rows = int((tf/ti) + 1)
    model = [
            [0, (-1 * vls), 0, weight, depAlt]
        ]
    for i in range(1, rows):
        t, velocity, acceleration, drag, altitude = model[i - 1]
        deltamodel = []
        deltamodel.append(t + ti)
        deltamodel.append((acceleration * ti) + velocity)
        deltamodel.append((drag - weight) / (weight / 32.172))
        if (((.5 * (float(aird_data[aird_data["Altitude"] > altitude].iloc[0]["Density"])) * (velocity ** 2) * cds) * (t / tf) ** avt) < weight):
            deltamodel.append(weight)
        elif (((.5 * (float(aird_data[aird_data["Altitude"] > altitude].iloc[0]["Density"])) * (velocity ** 2) * cds) * (t / tf) ** avt) >= weight):
            deltamodel.append(((.5 * (float(aird_data[aird_data["Altitude"] > altitude].iloc[0]["Density"])) * (velocity ** 2) * cds) * (t / tf) ** avt))
        deltamodel.append((ti*velocity)+altitude)

        model.append(deltamodel)

        fx = 0
        for line in model:
            fx = max(fx, line[3])
            fxlabel.set(("%.0f" % fx) + " lbs")
   ##_____________________________________________________
master = Tk()
master.attributes('-fullscreen', False)
master.geometry("800x400")

canvas = Canvas(master, width=1000, height=400)
canvas.pack()
canvas.create_rectangle(15, 70, 420, 375, fill='gray76')
canvas.create_rectangle(435, 70, 785, 250, fill='gray76')
canvas.create_line(240,140,240,365)


mainfont = ("Bahnschrift")
shapefont = tkFont.Font(family = 'Helvetica', size = 15)

title = Label(master, text = "FxCALC", font = (mainfont, 30, "bold", "underline")).place(x=330, y=5)

##STRING VARIABLES
fdrlabel = StringVar()
fxlabel = StringVar()
shape = StringVar()
tflabel = StringVar()

shape.set("Parabolic")
parashapes = [
    "Parabolic",
    "Toroidal"
]

#####INPUT LABELS
Label(master, text = "Inputs", font = (mainfont, 20, "bold"), bg = "gray76").place(x = 170, y = 75)
Label(master, text = "Shape", font = (mainfont, 15), bg = "gray76").place(x = 100, y = 135)
Label(master, text="Diameter (ft)", font = (mainfont, 15), bg = "gray76").place(x=68, y=175)
Label(master, text="Dry Weight (lbs)", font = (mainfont, 15), bg = "gray76").place(x=52, y=215)
Label(master, text="Deployment Vel. (ft/s)", font = (mainfont, 15), bg = "gray76").place(x=30, y=255)
Label(master, text = "Deployment Alt. (ft)", font = (mainfont, 15), bg = "gray76").place(x=40, y=295)
Label(master, text = "Landing Alt. (ft)", font = (mainfont, 15), bg = "gray76").place(x=55, y=335)

OptionMenu(master, shape, *parashapes).place(x=285, y=135)

#####ENTRIES
e1 = Entry(master, font = (mainfont, 16), width = 11)  ##diameter
e2 = Entry(master, font = (mainfont, 16), width = 11)  ##weight
e3 = Entry(master, font = (mainfont, 16), width = 11)  ##vls
e4 = Entry(master, font = (mainfont, 16), width = 11)  ##deployment altitude
e5 = Entry(master, font = (mainfont, 16), width = 11)  ##landing altitude

e1.place(x=260, y=175)
e2.place(x=260, y=215)
e3.place(x=260, y=255)
e4.place(x=260,y=295)
e5.place(x=260,y=335)

#####OUTPUT LABELS
fxresult = Label(master, textvariable=fxlabel, font = (mainfont, 16), bg = "gray76")
fxresult.place(x = 675, y = 135)
fdrresult = Label(master, textvariable=fdrlabel, font = (mainfont, 16), bg = "gray76")
fdrresult.place(x = 675, y = 175)
tfresult = Label(master, textvariable=tflabel, font = (mainfont, 16), bg = "gray76")
tfresult.place(x = 675, y = 215)

Label(master, text = "Outputs", font = (mainfont, 20, "bold"), bg = "gray76").place(x = 565, y = 75)
Label(master, text="Opening Force:", font = (mainfont, 15), bg = "gray76").place(x=480, y=135)
Label(master, text = "Final Descent Rate:",  font = (mainfont, 15), bg = "gray76").place(x=460, y=175)
Label(master, text = "Inflation Time:",  font = (mainfont, 15), bg = "gray76").place(x=485, y=215)

b = Button(master, text="Run Simulations", command=runmodel, font = (mainfont, 20, "bold"), height = 1, width = 20, bg = "SkyBlue1", relief = "ridge")
b.place(x = 455, y = 290)

master.mainloop()