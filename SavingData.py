from github import GithubException
from requests import exceptions 
from github import Github
from MongoConnect import *
from tkinter import *
from datetime import *
from functools import partial
import csv
import io
import os
import time
import requests

lastIssue = -1

def extraiEventos(issue, a):
    verificaQuantRequisicoes(a)
    print("---> Extraindo EVENTOS...")
    events = []

    try:
        e = ''
        for event in issue.get_events():
            verificaQuantRequisicoes(a) 
           
            if(event.actor is None):
                if(event.label is None):
                    e = mountEventJSON(issue.number, 
                                       '-', 
                                       event.created_at, 
                                       event.event, 
                                       '-')
                else:
                    e = mountEventJSON(issue.number, 
                                       '-', 
                                       event.created_at, 
                                       event.event, 
                                       event.label.name)
            else:
                if(event.label is None):
                    e = mountEventJSON(issue.number, 
                                       event.actor.login, 
                                       event.created_at, 
                                       event.event, 
                                       '-')
                else:
                    e = mountEventJSON(issue.number, 
                                       event.actor.login, 
                                       event.created_at, 
                                       event.event, 
                                       event.label.name)
            events.append(e)
    except requests.exceptions.ConnectionError as aes:
        print('Error de conexão')
        #continue
    except GithubException as d:
        if(d.status == 403):
            print("Limite de requisições atingido ao requisitar evento. Por favor, espere uma hora.")
            return False

    return events

def extraiComentarios(issue, a):
    verificaQuantRequisicoes(a)
    comments = []
    try:   
        c = ''
        for comment in issue.get_comments():
            print('----> Extraindo COMENTÁRIOS...')       
            verificaQuantRequisicoes(a)
            reactions = extraiReacoes(comment, a)
            if(comment.user is None):
                c = mountIssueCommentJSON('-', 
                                          comment.created_at, 
                                          comment.body, 
                                          reactions) 
            else: 
                c = mountIssueCommentJSON(comment.user.login, 
                                          comment.created_at, 
                                          comment.body, 
                                          reactions)                       
            comments.append(c)
            
    except GithubException as e:
        if(e.status == 403):
            print("Limite de requisições atingido ao requisitar comentrários. Por favor, espere uma hora.")
            return False
    except requests.exceptions.ConnectionError as aes:
        print('Erro crítico ao resgatar issue.')
        #continue


    return comments

def extraiReacoes(r, a):
    verificaQuantRequisicoes(a)
    print('----> ----> Extraindo REAÇÕES...') 
    count = [0, 0, 0, 0, 0, 0, 0, 0]
    """ thumbsup [1]
        deslike  [2]
        hooray   [3]
        heart    [4]
        confused [5]
        laugh    [6]
        rocket   [7]
        eyes     [8]
    """
    try:
        for reaction in r.get_reactions():
            verificaQuantRequisicoes(a) #### Verifica
            #print('------ Reaçoes')

            if(reaction.content == '+1'):
                count[0] += 1
            elif(reaction.content == 'heart'):
                count[1] += 1
            elif(reaction.content == 'hooray'):
                count[2] += 1
            elif(reaction.content == 'confused'):
                count[3] += 1
            elif(reaction.content == '-1'):
                count[4] += 1
            elif(reaction.content == 'laugh'):
                count[5] += 1
            elif(reaction.content == 'rocket'):
                count[6] += 1
            elif(reaction.content == 'eyes'):
                count[7] += 1
            
    except GithubException as e:
        if(e.status == 403):
            print("Limite de requisições atingido ao requisitar reações. Por favor, espere uma hora.")
            return False
    except requests.exceptions.ConnectionError as aes:
        print('Erro crítico ao resgatar issue.')
        #continue

    return mountReactionsJSON(count[0], 
                              count[1], 
                              count[2], 
                              count[3], 
                              count[4], 
                              count[5], 
                              count[6], 
                              count[7])

def extraiLabel(repo, a):
    print("-> Extraindo LABELS... ")
    verificaQuantRequisicoes(a) #### Verifica 
    labelList = []
    try:
        for label in repo.get_labels():        
            labelList.append(label.name)
        l = mountLabelsJSON(labelList)

    except GithubException as e:
        if(e.status == 403):
            print("Limite de requisições atingido ao requisitar labels. Por favor, espere uma hora.")
            return False
    except requests.exceptions.ConnectionError as aes:
        print('Erro crítico ao resgatar issue.')
        #continue

    return l

def getIssueAfterBreak(iss):
    try:
        issue = repo.get_issue(iss)
    except GithubException as e:
        if(e.data['message'] == 'Not Found'):
                print('Issue não encontrada')
        #continue
    except requests.exceptions.ConnectionError as e:
        print('Erro crítico ao resgatar issue.')
        return False
    return iss
    

requisicoesRestantes = 0

def extractDataFromGithub(us, ps, repoList, opFlag, clFlag, comFlag, evtFlag, rctFlag, labelsFlag):    
    repoCount = 0
    global requisicoesRestantes
    global lastIssue

    try:
        auth = Github(us, ps)
        requisicoesRestantes = int(auth.rate_limiting[0])
        verificaQuantRequisicoes(auth)
        for repoID in repoList:
            repository = auth.get_repo(repoID)
            print('Extração do repositorio '+repository.name+ ' começou.')
            verificaQuantRequisicoes(auth) #### Verifica
            l = '-'
            if(labelsFlag == 1):
                l = extraiLabel(repository, auth)
            if(opFlag == 1):
                issuesList = repository.get_issues()            
                for issue in issuesList:
                    if(findIssue(issue.number, repository.name) is None): 
                        lastIssue = issue
                        verificaQuantRequisicoes(auth) #### Verifica  
                        print('--> Extraindo Issue Open: '+str(issue.number))
                        e = '-'
                        c = '-'
                        r = '-'
                        if(evtFlag == 1):
                            e = extraiEventos(issue, auth)
                        if(comFlag == 1):
                            c = extraiComentarios(issue, auth)
                        if(rctFlag == 1):
                            r = extraiReacoes(issue, auth) 
                        
                        p = mountIssueJSON(repository.name, 
                                        issue.number, 
                                        issue.user.login, 
                                        issue.created_at, 
                                        issue.state, 
                                        issue.title, 
                                        issue.body, 
                                        r, e, c, l)
                        save(p, repository.name)
                    
            if(clFlag == 1):
                issuesList = repository.get_issues(state='closed')
                verificaQuantRequisicoes(auth) #### Verifica
                for issue in issuesList:
                    if(findIssue(issue.number, repository.name) is None): 
                        lastIssue = issue
                        verificaQuantRequisicoes(auth) #### Verifica
                        print('--> Extraindo Issue Closed: '+str(issue.number))
                        e = '-'
                        c = '-'
                        r = '-'
                        if(evtFlag == 1):
                            e = extraiEventos(issue, auth)
                        if(comFlag == 1):
                            c = extraiComentarios(issue, auth)
                        if(rctFlag == 1):
                            r = extraiReacoes(issue, auth)
                            
                        p = mountIssueJSON(repository.name, 
                                            issue.number, 
                                            issue.user.login, 
                                            issue.created_at, 
                                            issue.state, issue.title, 
                                            issue.body, 
                                            r, e, c, l)
                        save(p, repository.name)      
            repoCount += 1
        if(repoCount == len(repoList)):
            print("Concluído!", "Trabalho concluído.")
            return True
            #exit()
        return True
    except requests.exceptions.ConnectionError as req:
        print("Erro de conexão")
        return False
        
    except GithubException as f:
        if(f.status == 403):
            print("Limite de requisições atingido ao requisitar issues. Após uma hora, reinicie a aplicação.")
            return False
        else:
            print("Erro na função principal")
            return False 

def verificaQuantRequisicoes(auth):
    global requisicoesRestantes
    r = 0
    #time.sleep(2) # Espera0
    requisicoesRestantes -= 1
    #print('->->->-> Verificando requisições')
    
    #requisicoesRestantes = 
    #print("Aux "+str(requisicoesRestantes))
    
    if(requisicoesRestantes < 30):
        try:
            r = int(auth.get_rate_limit().core.remaining)
            if(r > 30):
                print("~~~~~~~ AJUSTANDO NÚMERO DE REQUISIÇÕES ~~~~~~~")
                requisicoesRestantes = r
            #print("Entrou r = "+str(r)+' e reqRestantes = '+str(requisicoesRestantes))
        except requests.exceptions.ConnectionError as req:
            print("Erro de conexão")
            return False
            #print('Timeout')
            #time.sleep(60)
            #verificaQuantRequisicoes(auth)

        while(requisicoesRestantes < 30):
            print("~~~~~~~ Processo DORMIU ~~~~~~~")    
            time.sleep(1800)
            print("~~~~~~~ Processo ACORDOU ~~~~~~~")
            try:
                requisicoesRestantes = int(auth.get_rate_limit().core.remaining)
            except requests.exceptions.ConnectionError as req:
                print("Erro de conexão")
                return False
            print("~~~~~~~ VERIFICANDO  REQUISIÇÕES ~~~~~~~")
            print(str(requisicoesRestantes)+" dispoíveis.")
    
        