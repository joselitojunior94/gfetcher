from SavingData import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from datetime import *
from functools import partial
import tkinter as tk
import tkinter.messagebox
import SavingData
from SavingData import startMiningFunction

def adicionaNaLista():
    entrada = nomeRepositorioEntry.get()
    if(entrada != ''):
        listbox.insert(END, entrada)
    elif(entrada == ''):
        try:
            folder = filedialog.askopenfilename()
            repositorios = open(folder,'r')
            lista0 = repositorios.read().split('\n')
            for l in lista0:
                if( l != ' '):
                    listbox.insert(END, l)
        except FileNotFoundError as e:
            print('Não houve seleção de arquivo.')
            
def extrairDados():
    vkey = keyEntry.get()
    vList =  listbox.get(0, END)
    vOp = varOpen.get()
    vCls = varClose.get()
    vComm = varComment.get()
    vEvt = evtsIssue.get()
    vRct = varReactions.get()
    vLbs = varLabels.get()
    messagebox.showinfo("Atenção!", 
                                "Esta janela será fechada e o processo poderá ser acompanhado pelo terminal. Para finalizar o processo digite Ctrl + C")
    root.destroy()
    startMiningFunction(vkey, 
                        vList, 
                        'en', 
                        vOp , 
                        vCls, 
                        vComm, 
                        vEvt, 
                        vRct, 
                        vLbs)
    #flag = False
    #while (flag == False):
    #    pass


def removerRepo():
    listbox.delete(listbox.curselection())

color = '#f2f2f2'

root = Tk()
root.geometry("620x400+400+200")
root.resizable(10, 0)
root.title("gFetcher")

listbox = Listbox(root, height=20)
listbox.place(x=452, y=30)

nomeRepositorioLabel = Label(
    root, text="nomeUsuario/nomeRepositorio", background=color)
nomeRepositorioLabel["font"] = ("Arial", "12", "bold")
nomeRepositorioLabel.place(x=9, y=5)

nomeRepositorioEntry = Entry(root)
nomeRepositorioEntry["width"] = 40
nomeRepositorioEntry.place(x=10, y=26)

inserirButton = Button(root)
inserirButton["text"] = "Adicionar > "
inserirButton["font"] = ("Calibri", "10")
inserirButton["width"] = 12
inserirButton["command"] = adicionaNaLista
inserirButton.place(x=296, y=60)

removerButton = Button(root)
removerButton["text"] = "< Remover "
removerButton["font"] = ("Calibri", "10")
removerButton["width"] = 12
removerButton["command"] = removerRepo
removerButton.place(x=296, y=100)

nomeRepositorioLabel = Label(root, text="Issues", background=color)
nomeRepositorioLabel["font"] = ("Arial", "12", "bold")
nomeRepositorioLabel.place(x=8, y=125)

varOpen = IntVar()
varClose = IntVar()
varComment = IntVar()
varSummary = IntVar()
varLabels = IntVar()
varReactions = IntVar()
evtsIssue = IntVar()

openCheck = Checkbutton(root, text="Open", variable=varOpen, background=color)
openCheck.place(x=12, y=150)

closeCheck = Checkbutton(
    root, text="Closed", variable=varClose, background=color)
closeCheck.place(x=12, y=170)

labelsCheck = Checkbutton(
    root, text="Extrair labels do repositório", variable=varLabels, background=color)
labelsCheck.place(x=102, y=150)

evtsCheck = Checkbutton(
    root, text="Extrair eventos da issue", variable=evtsIssue, background=color)
evtsCheck.place(x=102, y=170)

reactionsCheck = Checkbutton(
    root, text="Extrair reações de comentários", variable=varReactions, background=color)
reactionsCheck.place(x=102, y=190)

commentCheck = Checkbutton(
    root, text="Extrair comentários", variable=varComment, background=color)
commentCheck.place(x=102, y=210)

extrairButton = Button(root)
extrairButton["text"] = "Extrair dados "
extrairButton["font"] = ("Calibri", "10")
extrairButton["width"] = 12
extrairButton["command"] = extrairDados
extrairButton.place(x=296, y=350)

keyLabel = Label(
    root, text="Key: ", background=color)
keyLabel["font"] = ("Arial", "12", "bold")
keyLabel.place(x=10, y=328)

keyEntry = Entry(root, show='*')
keyEntry["width"] = 33
keyEntry.place(x=10, y=350)

root.resizable(False, False)
root.configure(background=color)
root.mainloop() 
