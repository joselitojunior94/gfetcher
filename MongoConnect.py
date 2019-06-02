from pymongo import MongoClient

def connect():
    cliente = MongoClient('localhost', 27017)
    banco = cliente['collectedIssues_database']

    return banco

def save(data, collec_name):
   p = banco[collec_name]
   reg = p.insert(data)

def mountEventJSON(atb0, atb1, atb2, atb3, atb4):
    J1 = {  'Issue': atb0,
            'Ator': atb1,
            'Criado em': atb2,
            'Evento': atb3,
            'Label': atb4
    }

    return J1

def mountIssueCommentJSON(atb1, atb2, atb3, atb4):
    J = { 
          'Autor': atb1,
          'Data': atb2,
          'Comentário': atb3,
          'Reações': atb4
        } 

    return J

def mountIssueJSON(atb0, atb1, atb2, atb3, atb4, atb5, atb6, atb7, atb8, atb9, atb10):
    J = { 'Nome do Repositório' : atb0, 
          'id':  atb1,
          'Autor': atb2,
          'Criado em': atb3,
          'Situação': atb4,
          'Título': atb5,
          'Descrição': atb6,
          'Labels': atb10,
          'Reações': atb7,
          'Eventos': atb8,
          'Comentários':atb9 
        } 

    return J

def mountLabelsJSON(atb0):
    J = {
        'name': atb0
    }

    return J

def mountReactionsJSON(thumbsup, heart, hooray, confused, deslike, laugh, rocket, eyes):
    J = {
        'Like' : thumbsup,
        'Deslike' : deslike,
        'hooray' : hooray,
        'heart' : heart,
        'confused' : confused,
        'laugh' : laugh,
        'rocket': rocket,
        'eyes' : eyes
    }

    return J

def find(db, J):
    p = db.issue_collection
    return p.find_one(J)

def findIssue(number, collec_name):
    p = banco[collec_name]
    J = {'id': number}

    return p.find_one(J)


def delete(number, collec_name):
    p = banco[collec_name]
    J = {'id': number}
    p.delete_one(J)


banco = connect()

