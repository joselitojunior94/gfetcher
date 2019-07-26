#
# python python DatabaseAnalysisScript.py listaDeRepositorios.txt nomeDoArquivo.csv
#

import io
import os
import sys
import csv
from MongoConnect import *

quantIssuesOpen = 0
quantIssuesClosed = 0

quantReacoesOpen = 0
quantReacoesClosed = 0

quantComentariosOpen = 0
quantComentariosClosed = 0

quantReacoesDescricaoOpen = 0
quantReacoesDescricaoClosed = 0

def ler_arquivo(caminho):

    arq = open(caminho, 'r')
    texto = arq.readlines()
    arq.close()

    return texto

collection_name = ler_arquivo(sys.argv[1])
nome_arquivo = sys.argv[2]

with io.open(nome_arquivo, 'w', newline='') as file:
    columns = ['Nome do Repositório', 'Quantidade de Issues Open', 'Quantidade de Issues Closed', 
               'Quantidade de Comentários Open', 'Quantidade de Comentários Closed', 'Quantidade de Reações Issue Open'
               , 'Quantidade de Reações Issue Closed']
    WriterCSV = csv.writer(file, delimiter=';')
    WriterCSV.writerow(columns)
    
    collection_name = ['terminal']
    for repo in collection_name:
        p = banco[repo]
        cursor = p.find({})
        print("Dados do repositório: "+ str(repo))
        for document in cursor:
            if(document['Situação'] == 'open'):
                quantIssuesOpen += 1
                rD = document['Reações']
                quantReacoesOpen += (    rD['Like'] + 
                                     rD['Deslike'] +
                                     rD['hooray'] + 
                                     rD['heart'] + 
                                     rD['confused'] + 
                                     rD['laugh'] + 
                                     rD['rocket'] + 
                                     rD['eyes'])
                quantComentariosOpen += len(document['Comentários'])
                for l in document['Comentários']:
                    r = l['Reações']
                    quantReacoesOpen += (r['Like'] + 
                                     r['Deslike'] +
                                     r['hooray'] + 
                                     r['heart'] + 
                                     r['confused'] + 
                                     r['laugh'] + 
                                     r['rocket'] + 
                                     r['eyes'])
        
            elif(document['Situação'] == 'closed'):
                quantIssuesClosed += 1
                rD = document['Reações']
               
                quantReacoesClosed +=  (rD['Like'] + 
                                       rD['Deslike'] +
                                       rD['hooray'] + 
                                       rD['heart'] + 
                                       rD['confused'] + 
                                       rD['laugh'] + 
                                       rD['rocket'] + 
                                       rD['eyes']) 

                quantComentariosClosed += len(document['Comentários'])
                for l in document['Comentários']:
                    r = l['Reações']
                    quantReacoesClosed +=  (r['Like'] + 
                                       r['Deslike'] +
                                       r['hooray'] + 
                                       r['heart'] + 
                                       r['confused'] + 
                                       r['laugh'] + 
                                       r['rocket'] + 
                                       r['eyes'])         

        data = [repo, quantIssuesOpen, quantIssuesClosed, quantComentariosOpen, 
                    quantComentariosClosed, quantReacoesOpen, quantReacoesClosed]
        
        WriterCSV.writerow(data)
        
        quantIssuesOpen = 0
        quantIssuesOpenClosed = 0   
        quantReacoesOpen = 0
        quantReacoesClosed = 0  
        quantComentariosOpen = 0
        quantComentariosClosed = 0

        print("\n")

file.close()
