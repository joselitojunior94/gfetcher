from github import Github
import csv
import io
import os
from MongoConnect import *

def teste(window):
    window.deiconify()

def get_IssueBody(repo, issueID):
    issue = repo.get_issue(issueID)
    return issue.body

def get_IssueComments(self, repo, id):
    issue = repo.get_issue(id)
    comments = issue.get_comments()
    vCommentsBody = []

    for comm in comments:
        vCommentsBody.append(comm)
        
    return vCommentsBody

def extracting_data(repoList, opFlag, clFlag, comFlag, sumFlag):
    with io.open('githubIssues.csv', 'w', newline='', encoding="utf-8") as file:
        columns = ['Nome do Repositório', 'id', 'Situação' , 'Título','Descrição da Issue', 'Comentário da Issue']
        WriterCSV = csv.writer(file, delimiter=';')
        WriterCSV.writerow(columns)
        for repoID in repoList:
            repository = auth.get_repo(repoID)
            print(repository.name)
            if(opFlag == 1):
                issuesList = repository.get_issues()
                for issue in issuesList:
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = ['-', repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
            if(clFlag == 1):
                issuesList = repository.get_issues(state='closed')
                for issue in issuesList:
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = ['-', repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
    file.close()

#
#       Extraí todos as issues juntas em um .csv e cria uma pasta para os arquivos
#


def extraction_data_per_repository(f, repoList, opFlag, clFlag, comFlag, sumFlag, labelsFlag):
    for repoID in repoList:
        repository = auth.get_repo(repoID)
        dirS = os.path.join(f, "Files")
        os.makedirs(dirS)
        name = repository.name + '.csv'
        if(labelsFlag == 1):
            extracting_labels(repository, dirS)
        caminho_arquivo = os.path.join(dirS, name)
        print(caminho_arquivo)
        with io.open(caminho_arquivo, 'w', newline='', encoding="utf-8") as file:
            columns = ['Nome do Repositório', 'id', 'Situação' , 'Título','Descrição da Issue', 'Comentário da Issue']
            WriterCSV = csv.writer(file, delimiter=';')
            WriterCSV.writerow(columns)
            if(opFlag == 1):
                issuesList = repository.get_issues()
                for issue in issuesList:
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = [repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
            if(clFlag == 1):
                issuesList = repository.get_issues(state='closed')
                for issue in issuesList:
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = [repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
        file.close()

#
#       Extrai todas as labels do repositório
#

def extracting_labels(repo, filePath):
    nA = repo.name + '_labels.csv'
    caminho_arquivo = os.path.join(filePath, nA)
    labels = repo.get_labels()
    with io.open(caminho_arquivo, 'w', encoding="utf-8") as file:
        WriterCSV = csv.writer(file, delimiter=' ')
        for label in labels:
            #print(label.name)
            WriterCSV.writerow([label.name])
    file.close()
    print('Finished')


#
#       Método salva a Issue uma por uma em diferentes .csv  
#

def extracting_and_save_separately(f, repoList, opFlag, clFlag, comFlag, sumFlag, labelsFlag):
    for repoID in repoList:
        repository = auth.get_repo(repoID)
        dirS = os.path.join(f, repository.name)
        os.makedirs(dirS)
        if(labelsFlag == 1):
            extracting_labels(repository, dirS)

        columns = ['Nome do Repositório', 'id', 'Situação' , 'Título','Descrição da Issue', 'Comentário da Issue']   

        if(opFlag == 1):
            issuesList = repository.get_issues()
            for issue in issuesList:
                name = str(issue.number) + '.csv'
                caminho_arquivo = os.path.join(dirS, name)
                with io.open(caminho_arquivo, 'w', newline='', encoding="utf-8") as file:
                    WriterCSV = csv.writer(file, delimiter=';')
                    WriterCSV.writerow(columns)
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = [repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
                file.close()
                print('Finished Open')
            
        if(clFlag == 1):
            issuesList = repository.get_issues(state='closed')
            for issue in issuesList:
                name = str(issue.number) + '.csv'
                caminho_arquivo = os.path.join(dirS, name)
                with io.open(caminho_arquivo, 'w', newline='', encoding="utf-8") as file:
                    WriterCSV = csv.writer(file, delimiter=';')
                    WriterCSV.writerow(columns)
                    if(sumFlag == 1):
                        data = [repository.name, issue.number, issue.state, issue.title, issue.body, '-']
                        WriterCSV.writerow(data)
                    if(comFlag == 1):
                        for comment in issue.get_comments():
                            data = [repository.name, issue.number, issue.state, issue.title, '-', comment.body]
                            WriterCSV.writerow(data)
                file.close()
                print('Finished Closed')