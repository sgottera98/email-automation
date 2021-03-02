#Projeto de envio de emails com anexo a partir de um array onde estarão salvos
#os clientes e de arquivos salvos em pastas criadas por esse executável

import os
from shutil import make_archive
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

clientes=['Teste de Envio 1', 'Teste de Envio 2']

email=['teste@hotmail.com', ' ']

###############################################################################################################################################################################################################################

def criar_pastas(): #funcao onde serão criados as pastas especificas dos clientes
    try:
        for i in range(len(clientes)): #laço de repetição
            os.makedirs('/Coletas Mensais/'+clientes[i]) #criando diretórios de clientes
            for j in range(2020,2021+1): #laço de repetição
                os.makedirs('/Coletas Mensais/'+clientes[i]+'/'+str(j)) #criando diretórios de anos
                os.makedirs('/Coletas Mensais/'+clientes[i]+'/'+str(j)+'/Arquivos Compactados Para Envio')
                for k in range(1,12+1): #laço de repetição
                    os.makedirs('/Coletas Mensais/'+clientes[i]+'/'+str(j)+'/'+str(k)) #criando diretórios de meses
        os.makedirs('/Coletas Mensais/Configuração') #config de email
    except FileExistsError: #tratando erro de diretório existente
        print('Conjunto de pastas já existe, verifique.')

def compactar(cliente):
    try:
        make_archive('/Coletas Mensais/'+cliente+'/'+str(ano_atual)+'/Arquivos Compactados Para Envio/Arquivos do Mes '+str(mes_atual),'zip','/Coletas Mensais/'+cliente+'/'+str(ano_atual)+'/'+str(mes_atual))
    except FileNotFoundError: #tratando erro de diretório não encontrado
        print('Arquivo a ser compactado não foi encontrado, verifique')

def email_envio(nome,remete,senha,destina,smtp,assunto,corpo,arquivo,mes): #funcao envio de email com anexo
    try:
        msg = MIMEMultipart()
        msg['Subject'] = assunto 
        msg['From'] = nome
        msg['To'] = destina

        body = corpo

        msg.attach(MIMEText(body, 'plain'))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(arquivo, "rb").read())
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment; filename=Arquivos do Mes '+mes+'.zip')

        msg.attach(part)

        server = smtplib.SMTP(smtp, 587)
        server.starttls()
        server.login(remete, senha)
        server.sendmail(remete, destina, msg.as_string())
    except:
        print('Não foi possível enviar o email')

###############################################################################################################################################################################################################################    

#trazendo data atual
data_hora_atuais =(datetime.now())

mes_atual = data_hora_atuais.month
ano_atual = data_hora_atuais.year
hora_atual = data_hora_atuais.hour
                 
if mes_atual == 1:
    mes_atual = 12
    ano_atual -= 1             
else:
    mes_atual -= 1
    ano_atual

###############################################################################################################################################################################################################################
    
assunto = 'Arquivos Referentes à Empresa '

if hora_atual < 12:
    saudacao = 'Bom dia'
else:
    saudacao = 'Boa tarde'

corpo = '''Segue em anexo os arquivos da empresa '''
assinatura = '''\n\nAtenciosamente\n'''

resp = 'S'
while resp == 'S' or resp == 's':
    menu = str(input("Escolha uma opção:\n1-Enviar email.\n2-Enviar todos os emails. \n3-Configurar email remetente.\n4-Alterar email do cliente.\n5-Criar pastas automáticas.\n\n"))

    if menu == '1':
        opcao = 'S'
        while opcao == 'S' or opcao == 's':
            if os.path.isfile('/Coletas Mensais/Configuração/email.txt') and os.path.isfile('/Coletas Mensais/Configuração/senha.txt') and os.path.isfile('/Coletas Mensais/Configuração/smtp.txt') and os.path.isfile('/Coletas Mensais/Configuração/nome.txt'):
                with open('/Coletas Mensais/Configuração/email.txt', 'r') as e:
                    emailremete = e.readline().strip()
                with open('/Coletas Mensais/Configuração/senha.txt', 'r') as s:
                    senha = s.readline().strip()
                with open('/Coletas Mensais/Configuração/smtp.txt', 'r') as smtp:
                    smtp = smtp.readline().strip()
                with open('/Coletas Mensais/Configuração/nome.txt', 'r') as n:
                    nome = n.readline().lstrip()
                for i in range(len(clientes)):
                    print(str(i+1)+' '+clientes[i])
                n = int(input("\nSelecione o cliente:\n"))
                compactar(clientes[n-1])
                arquivo = '/Coletas Mensais/'+clientes[n-1]+'/'+str(ano_atual)+'/Arquivos Compactados Para Envio/Arquivos do Mes '+str(mes_atual)+'.zip'
                email_envio(nome,emailremete,senha,email[n-1],smtp,assunto+clientes[n-1],saudacao+'\n\n'+corpo+clientes[n-1]+' referentes ao mês '+str(mes_atual)+assinatura+nome,arquivo,str(mes_atual))
            else:
                print('Email do remetente não foi configurado, verifique.')
            opcao = str(input("\nDeseja continuar? S/N\n"))
            
    elif menu == '2':
        opcao = str(input('Tem certeza que deseja enviar arquivos a todos os destinatários? S/N\n'))
        if opcao == 'S' or opcao == 's':        
            if os.path.isfile('/Coletas Mensais/Configuração/email.txt') and os.path.isfile('/Coletas Mensais/Configuração/senha.txt') and os.path.isfile('/Coletas Mensais/Configuração/smtp.txt') and os.path.isfile('/Coletas Mensais/Configuração/nome.txt'):
                with open('/Coletas Mensais/Configuração/email.txt', 'r') as e:
                    emailremete = e.readline().strip()
                with open('/Coletas Mensais/Configuração/senha.txt', 'r') as s:
                    senha = s.readline().strip()
                with open('/Coletas Mensais/Configuração/smtp.txt', 'r') as smtp:
                    smtp = smtp.readline().strip()
                with open('/Coletas Mensais/Configuração/nome.txt', 'r') as n:
                    nome = n.readline().lstrip()
                for i in range(len(clientes)):
                    print(str(i+1)+' '+clientes[i])
                for i in range(len(clientes)):
                    compactar(clientes[i])
                    arquivo = '/Coletas Mensais/'+clientes[i]+'/'+str(ano_atual)+'/Arquivos Compactados Para Envio/Arquivos do Mes '+str(mes_atual)+'.zip'
                    email_envio(nome,emailremete,senha,email[i],smtp,assunto+clientes[i],saudacao+'\n\n'+corpo+clientes[i]+' referentes ao mês '+str(mes_atual)+assinatura+nome,arquivo,str(mes_atual))
            else:
                print('Email do remetente não foi configurado, verifique.')

    elif menu == '3':
        with open('/Coletas Mensais/Configuração/email.txt', 'w') as e:
            e.write(str(input('Email: ')))
        with open('/Coletas Mensais/Configuração/senha.txt', 'w') as s:   
            s.write(str(input('Senha: ')))
        with open('/Coletas Mensais/Configuração/smtp.txt', 'w') as smtp:
            smtp.write(str(input('SMTP: ')))
        with open('/Coletas Mensais/Configuração/nome.txt', 'w') as n:
            n.write(str(input('Nome Remetente: ')))
        
    elif menu == '4':
        for i in range(len(clientes)):
            print(str(i+1)+' '+clientes[i]+' - '+email[i])
        opcao = int(input("\nQual cliente deseja alterar?\n"))
        email[opcao - 1] = str(input("Email: "))

    elif menu == '5':
        criar_pastas()

    else:
        print("Opção inválida")

    resp = str(input("\nDeseja realizar outra operação? S/N\n"))



