from SavingData import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from datetime import *
from functools import partial
import tkinter as tk
import tkinter.messagebox
from functools import partial

def adicionaNaLista():
    #listbox.insert(END, nomeRepositorioEntry.get())
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
    vLogin = loginEntry.get()
    vPass =  passEntry.get()
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
    flag = False
    while (flag == False):
        flag = extractDataFromGithub(vLogin, 
                        vPass, 
                        vList, 
                        vOp, 
                        vCls, 
                        vComm, 
                        vEvt, 
                        vRct, 
                        vLbs)

    #app.deiconify()
    """
    folder = filedialog.askdirectory()
    
    if(folder != ""):
        if(v.get() == 0):
             extraction_data_per_repository(folder, listbox.get(0, END),
                    varOpen.get(),
                    varClose.get(),
                    varComment.get(),
                    varSummary.get(),
                    varLabels.get())
        elif(v.get() == 1):
            extracting_and_save_separately(folder, listbox.get(0, END),
                    varOpen.get(),
                    varClose.get(),
                    varComment.get(),
                    varSummary.get(),
                    varLabels.get())
        """
        #extractDataFromGithub(repoList, opFlag, clFlag, comFlag, evtFlag, rctFlag, labelsFlag)

        

def removerRepo():
    listbox.delete(listbox.curselection())


def goBugZilla():
    root.destroy()
    bugzillaGo()
    
def goJira():
    root.destroy()
    jiraGo()

color = '#f2f2f2'

root = Tk()
root.geometry("600x380+400+200")
root.resizable(10, 0)
root.title("Github Fetcher")

listbox = Listbox(root, height=20)
listbox.place(x=452, y=30)

#nomeRepositorioAdicionadoLabel = Label(
 #   root, text="Lista de Repositórios Adicionados", background=color)
#nomeRepositorioAdicionadoLabel["font"] = ("Arial", "12", "bold")
#nomeRepositorioAdicionadoLabel.place(x=395, y=5)

nomeRepositorioLabel = Label(
    root, text="Insira o repositorio: Ex.: nomeUsuario/nomeRepositorio", background=color)
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
removerButton["text"] = "< Remover repo "
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
"""
summaryCheck = Checkbutton(
    root, text="Extrair descrição", variable=varSummary, background=color)
summaryCheck.place(x=102, y=150)
"""

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

#modoSalvamentoLabel = Label(
   # root, text="Modo de salvamento das informações", background=color)
#modoSalvamentoLabel["font"] = ("Arial", "12", "bold")
#modoSalvamentoLabel.place(x=12, y=220)



#v = IntVar()

#modoUmRadio = Radiobutton(root, text="Issues em conjunto", variable=v, value=0, background=color)
#modoUmRadio.place(x=12, y=250)
#modoDoisRadio = Radiobutton(root, text="Issues separadas", variable=v, value=1, background=color)
#modoDoisRadio.place(x=170, y=250)

extrairButton = Button(root)
extrairButton["text"] = "Extrair dados "
extrairButton["font"] = ("Calibri", "10")
extrairButton["width"] = 12
extrairButton["command"] = extrairDados
extrairButton.place(x=296, y=350)


loginLabel = Label(
    root, text="Login: ", background=color)
loginLabel["font"] = ("Arial", "12", "bold")
loginLabel.place(x=10, y=332)

loginEntry = Entry(root)
loginEntry["width"] = 10
loginEntry.place(x=10, y=350)

loginLabel = Label(
    root, text="Password: ", background=color)
loginLabel["font"] = ("Arial", "12", "bold")
loginLabel.place(x=150, y=332)

passEntry = Entry(root)
passEntry["width"] = 10
passEntry.place(x=150, y=350)



"""
bugzillaButton = Button(root)
bugzillaButton["text"] = "BugZilla "
bugzillaButton["font"] = ("Calibri", "10")
bugzillaButton["width"] = 12
bugzillaButton["command"] = goBugZilla
bugzillaButton.place(x=10, y=350)
"""

"""
jiraButton = Button(root)
jiraButton["text"] = "Jira"
jiraButton["font"] = ("Calibri", "10")
jiraButton["width"] = 12
jiraButton["command"] = goJira
jiraButton.place(x=120, y=350)
"""

#app = Tk()
#app.title("Progresso")
#app.resizable(False, False)
#app.geometry("600x80+405+300")
#app.configure(background=color)
#app.withdraw()

#updateLabel = Label(app, text = "Progresso da extração", background=color)
#updateLabel.pack()
#progressBar = ttk.Progressbar(app, orient=HORIZONTAL, mode='indeterminate')
#progressBar.pack(expand=True, fill=BOTH, side=TOP)

root.resizable(False, False)

root.configure(background=color)

root.mainloop() 

#app.mainloop()

