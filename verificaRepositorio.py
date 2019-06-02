from github import GithubException
from github import Github
import io

repositorios = open('repositorios.txt','r')
auth = Github('', '')
f = open('repositoriosValidos.txt','w')
print(auth.get_rate_limit().core.remaining)
r = repositorios.read().split(' ')

for i in r:
    print(i)
    try:
        repo = auth.get_repo(str(i))
        print('Existe')
        i += '\n'
        f.write(i)
    except GithubException as e:
         if(e.status == 403):
             print('Limite excedido')
             exit()
         if(e.data['message'] == 'Not Found'):
             print('Repositório não existe')

repositorios.close()
f.close()