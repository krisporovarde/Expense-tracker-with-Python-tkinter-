from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import calendar
import time
from tinydb import TinyDB, Query

db = TinyDB("db.json")
User = Query()
def lisa_db():
    kuud = ["Jaanuar", "Veebruar", "Märts", "Aprill", "Mai", "Juuni", "Juuli", "August", "September", "Oktoober", "November", "Detsember"]
    for kuu in kuud:
        db.insert({"kuu": kuu, "kulud kokku": 0, "söögid kokku": 0, "alkohol kokku": 0, "arved kokku": 0, "muu kokku": 0})
#lisa_db()
#print(db.all())


#akna loomine
aken = Tk()
aken.geometry("700x500")
aken.eval('tk::PlaceWindow . center')
aken.title("Kulude jälgija")
aken.configure(bg="WhiteSmoke")
#mooduli tegemine ja #ekraanile kuvamine
pealkiri1 = Label(aken, text="Vali kulu:", bg="WhiteSmoke", font=("Times New Roman", 20)).grid(column=0, row=0, padx=10, pady=5)


#Sisestus box
sisestus = Entry(aken, width=20, borderwidth=2, font=("Times New Roman", 14), justify='center')
sisestus.grid(row=5, column=2)
sisestus.insert(0, "Sisesta kulu")

#Märksõna valimine
märksõna = StringVar()
r1 = Radiobutton(aken, text="Söök", bg="WhiteSmoke", variable=märksõna, value="söök", font=("Times New Roman", 14)).grid(column=0, row=1, padx=10, pady=5, sticky="w")
r2 = Radiobutton(aken, text="Alkohol", bg="WhiteSmoke", variable=märksõna, value="alkohol", font=("Times New Roman", 14)).grid(column=0, row=2, padx=10, pady=5, sticky="w")
r3 = Radiobutton(aken, text="Arved", bg="WhiteSmoke", variable=märksõna, value="arved", font=("Times New Roman", 14)).grid(column=0, row=3, padx=10, pady=5, sticky="w")
r4 = Radiobutton(aken, text="Muu", bg="WhiteSmoke", variable=märksõna, value="muu", font=("Times New Roman", 14)).grid(column=0, row=4, padx=10, pady=5, sticky="w")

#programm, mis väljastab nupu(Sisesta) vajutusega jooksva kuu kulud
def arvutus():
    kuud = ["Jaanuar", "Veebruar", "Märts", "Aprill", "Mai", "Juuni", "Juuli", "August", "September", "Oktoober", "November", "Detsember"]

    dt = datetime.today()
    kuu_indeks = dt.month - 1
    kuu_nimi = kuud[kuu_indeks]
    hetke_kuu = db.search(User.kuu == kuu_nimi)
    
    hetke_kuu_kulud = hetke_kuu[0]["kulud kokku"] + float(sisestus.get())
    db.update({"kulud kokku": hetke_kuu_kulud}, User.kuu == kuu_nimi)

    hetke_kuu_söögid_kokku = hetke_kuu[0]["söögid kokku"]
    hetke_kuu_alkohol_kokku = hetke_kuu[0]["alkohol kokku"]
    hetke_kuu_arved_kokku = hetke_kuu[0]["arved kokku"]
    hetke_kuu_muu_kokku = hetke_kuu[0]["muu kokku"]

    if märksõna.get() == "söök":
        hetke_kuu_söögid_kokku += float(sisestus.get())
        db.update({"söögid kokku": hetke_kuu_söögid_kokku}, User.kuu == kuu_nimi)
    elif märksõna.get() == "alkohol":
        hetke_kuu_alkohol_kokku += float(sisestus.get())
        db.update({"alkohol kokku": hetke_kuu_alkohol_kokku}, User.kuu == kuu_nimi)
    elif märksõna.get() == "arved":
        hetke_kuu_arved_kokku += float(sisestus.get())
        db.update({"arved kokku": hetke_kuu_arved_kokku}, User.kuu == kuu_nimi)
    elif märksõna.get() == "muu":
        hetke_kuu_muu_kokku += float(sisestus.get())
        db.update({"muu kokku": hetke_kuu_muu_kokku}, User.kuu == kuu_nimi)
    väljastus = Label(aken, bg="WhiteSmoke", text="Jooksev kuu: " + str(round(hetke_kuu_kulud, 2)) + " €", font=("Times New Roman", 14)).grid(row=7, column=2)
    väljastus = Label(aken, bg="WhiteSmoke", text="Söögid kokku: " + str(round(hetke_kuu_söögid_kokku, 2)) + " €", font=("Times New Roman", 14)).grid(row=8, column=2)
    väljastus = Label(aken, bg="WhiteSmoke", text="Alkohol kokku: " + str(round(hetke_kuu_alkohol_kokku, 2)) + " €", font=("Times New Roman", 14)).grid(row=9, column=2)
    väljastus = Label(aken, bg="WhiteSmoke", text="Arved kokku: " + str(round(hetke_kuu_arved_kokku, 2)) + " €", font=("Times New Roman", 14)).grid(row=10, column=2)
    väljastus = Label(aken, bg="WhiteSmoke", text="Muu kokku: " + str(round(hetke_kuu_muu_kokku, 2)) + " €", font=("Times New Roman", 14)).grid(row=11, column=2)
    sisestus.delete(0,9)
    sektordiagramm()
    
def sektordiagramm():
    dt = datetime.today()
    kuu_indeks = dt.month - 1
    kuu_nimi = kuud[kuu_indeks]
    hetke_kuu = db.search(User.kuu == kuu_nimi)
    
    hetke_kuu_söögid_kokku = hetke_kuu[0]["söögid kokku"]
    hetke_kuu_alkohol_kokku = hetke_kuu[0]["alkohol kokku"]
    hetke_kuu_arved_kokku = hetke_kuu[0]["arved kokku"]
    hetke_kuu_muu_kokku = hetke_kuu[0]["muu kokku"]
    
    # Sektordiagrammi kujundamine
    fig = plt.figure(figsize=(6, 6), dpi=100)
    fig.set_size_inches(4, 2)
    fig.set_facecolor('WhiteSmoke')

    # Andmed
    labels = "Söögid kokku", "Alkohol kokku", "Arved kokku", "Muu kokku"
    kulud = [int(hetke_kuu_söögid_kokku), int(hetke_kuu_alkohol_kokku), int(hetke_kuu_arved_kokku), int(hetke_kuu_muu_kokku)]
    värvid = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'Orange', 'red']

    # Sektodiagrammi loomine
    plt.pie(kulud, labels=labels, colors=värvid, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    # Diagrammi aknal kuvamine
    canvasbar = FigureCanvasTkAgg(fig, master=aken)
    canvasbar.draw()
    canvasbar.get_tk_widget().place(relx = 1, x =-2, y = 2, anchor= "ne") 

# Comboboxi vajutus.
def kuu_valik_vajutus(e):
    hetke_kuu = db.search(User.kuu == kuu_valik.get())
    väljastus1 = Label(aken,  bg="WhiteSmoke", text=str(kuu_valik.get()) + " kokku: " + str(round(hetke_kuu[0]["kulud kokku"], 2)), font=("Times New Roman", 14))
    väljastus2 = Label(aken, bg="WhiteSmoke", text=str(kuu_valik.get()) + " söök kokku: " + str(round(hetke_kuu[0]["söögid kokku"], 2)), font=("Times New Roman", 14))
    väljastus3 = Label(aken, bg="WhiteSmoke", text=str(kuu_valik.get()) + " alkohol kokku: " + str(round(hetke_kuu[0]["alkohol kokku"], 2)), font=("Times New Roman", 14))
    väljastus4 = Label(aken, bg="WhiteSmoke", text=str(kuu_valik.get()) + " arved kokku: " + str(round(hetke_kuu[0]["arved kokku"], 2)), font=("Times New Roman", 14))
    väljastus5 = Label(aken, bg="WhiteSmoke", text=str(kuu_valik.get()) + " muu kokku: " + str(round(hetke_kuu[0]["muu kokku"], 2)), font=("Times New Roman", 14))
    väljastus1.grid(row=7, column=3)
    väljastus2.grid(row=8, column=3)
    väljastus3.grid(row=9, column=3)
    väljastus4.grid(row=10, column=3)
    väljastus5.grid(row=11, column=3)
    väljastus1.after(3000, väljastus1.destroy)
    väljastus2.after(3000, väljastus2.destroy)
    väljastus3.after(3000, väljastus3.destroy)
    väljastus4.after(3000, väljastus4.destroy)
    väljastus5.after(3000, väljastus5.destroy)

# Combobox
kuud = ["Jaanuar", "Veebruar", "Märts", "Aprill", "Mai", "Juuni", "Juuli", "August", "September", "Oktoober", "November", "Detsember"]
kuu_valik = ttk.Combobox(aken, value=kuud,state="readonly")
kuu_valik.current(0)
kuu_valik.bind("<<ComboboxSelected>>", kuu_valik_vajutus)
kuu_valik.grid(column=3, row=6, padx=130, pady=5)


sektordiagramm()

#Sisesta nupp
nupp = Button(aken, text="Sisesta", width=17, command=arvutus, bg="black", fg="white", font=("Times New Roman", 14)).grid(row=6, column=2, sticky="nsew")

aken.mainloop()