"""
    IMPORTANT: This program works only with two archives
    Collect the name of two files from the user (.java archives)
    Verify the existance of this files
    Verify number of lines of each file
    Verify if a word is in the file, count how many times it appears and identify where
    Identify the program with Syntax Error (more send/recv)
    ***Create a dictionary to save the lines and the commands
    ***Create an archive (.txt) with a code to GraphViz
    ***Define the conections between the two programs
    ---tentar abrir o GraphViz--- (Não feito)
"""
import os #impotação do módulo OS para abrir arquivos
"""
Para abrir com o progrma padrão do WINDOWS:
    os.startfile("teste.txt")
"""
subGraph=0
nSend=0
nRecv=0
nLinhas=0
contRECV=0
contSEND=0
contOUT=0
contIN=0

toCode = ""

listProg1=[]
dici={}

#verifica a existência de cada palavra recebida em um arquivo determinado
def find_word(palavra, file):
    cont = 0
    #print("\nPalavra: " + palavra)
    for linha in file:
        #verifica se determinada string está contida nas linhas do arquivo
        if palavra in linha:
            dici[file.index(linha)+1]=palavra
            #salva o comando e a linha no dicionário
            #print("Encontrado na linha: " + str(file.index(linha)+1))
            cont += 1
    #print ("Total de ocorrências: " + str(cont))
    return cont

#define as interações via rede
def ligacoesDeRede(list1,list2):
    ligacoes=""
    
    aux=0
    aux2=0
    
    try:
        for num in range(len(list1)):
            if list1[num].startswith("writeUTF_"):
                while aux < len(list2):
                    if list2[aux].startswith("readUTF_"):
                        ligacoes += "    " + list1[num] + " -> " + list2[aux] + "\n"
                        aux+=1
                        break
                    else:
                        aux+=1
            if list2[num].startswith("writeUTF_"):
                while aux2< len(list1):
                    if list1[aux2].startswith("readUTF_"):
                        ligacoes += "    " +  list2[num] + " -> " + list1[aux2] + "\n"
                        aux2+=1
                        break
                    else:
                        aux2+=1
        return ligacoes
    except:
        print("Erro inesperado com sends/recv")


#determina o fluxo do programa
def fluxo(auxString, numLinha):
    global dici
    global toCode
    
    if numLinha == max(dici.keys()):
        toCode += auxString + " -> end"
    elif numLinha == min(dici.keys()):
        toCode += "start -> " + auxString + " -> "
    else:
        toCode += auxString + " -> "
        
#escreve um arquivo para ser executado no GraphViz
def writingCode():
    global nLinhas
    global subGraph
    global dici
    global contRECV
    global contSEND
    global contOUT
    global contIN
    global toCode
    global listProg1
    
    list=[]
    auxMenor=0
    
    if subGraph==0:
        code ="""digraph G {

    start [shape=Mdiamond];
    end [shape=Msquare];
    
    subgraph cluster_""" + str(subGraph) + """{
        style=filled;
	color=lightgrey;
	node [style=filled,color=white];"""
    else:
        code ="""
    \nsubgraph cluster_""" + str(subGraph) + """{
        style=filled;
	color=lightgrey;
	node [style=filled,color=white];"""
    #Verifica todos os itens no dicionário    
    for item in range(nLinhas-2):
        try:
            #Verificar qual o comando da primeira linha e escrever no arquivo texto
            if dici[auxMenor]=='readUTF':
                sAux ="""\n        readUTF_""" + str(contRECV) + """[shape=invhouse, fillcolor=white,color =cyan, label="recv\nreadUTF: line """ + str(auxMenor) + '"]' #imprimir \n
                auxString = "readUTF_" + str(contRECV)
                fluxo(auxString, auxMenor)
                list.append(auxString)
                code += sAux
                auxMenor += 1
                contRECV+=1
            if dici[auxMenor]=='writeUTF':
                sAux ="""\n        writeUTF_""" + str(contSEND) + """[shape = house, fillcolor=white, color=salmon, label="send\nwriteUTF: line """ + str(auxMenor) + '"]'
                auxString = "writeUTF_" + str(contSEND)
                fluxo(auxString, auxMenor)
                list.append(auxString)
                code += sAux
                auxMenor += 1
                contSEND+=1
            if dici[auxMenor]=='System.in':
                sAux= """\n        System_in_""" + str(contIN) + """[ shape=octagon, label="In\nSystem.in: line """ + str(auxMenor) + '"]'
                auxString = "System_in_" + str(contIN)
                fluxo(auxString, auxMenor)
                code += sAux
                auxMenor += 1
                contIN+=1
            if dici[auxMenor] =='System.out':
                sAux = """\n        System_out_""" + str(contOUT) + """[shape=oval, fillcolor=white, color=gold2, label="Out\nSystem.out: line """ + str(auxMenor) + '"]'
                auxString = "System_out_" + str(contOUT)
                fluxo(auxString, auxMenor)
                code += sAux
                auxMenor += 1
                contOUT+=1
        except KeyError:
            auxMenor += 1
    
    #inclui label do grafo e finaliza o cógido
    if subGraph==0:
        listProg1=list
        list=[]
        code +="\n        label=" +' "' + entrada +'" ' + """
    }
    """ + toCode
        writeFile = open('teste.txt','w')
    elif subGraph==1:
        ligaRede = ligacoesDeRede(listProg1, list) 
        code +="\n        label=" +' "' + entrada2 +'" ' + """
    }\n    """+ toCode + "\n" + ligaRede + "}"
        writeFile = open('teste.txt','a')
    
    #cria um arquivo para salvar o código do GraphViz
    writeFile.write(code)
    writeFile.close()
    toCode=""
    subGraph+=1
    dici={}

#recebe uma string; verifica a existencia de um .java nomeado dessa forma; retorna o n de linhas; verifica a existência de "palavras-chave"
def verify_file(file_in):
    global nLinhas
    try:
        print("---------------------------------------------------")
        newfile=open(file_in + ".java","r") 
        #operações com o arquivo
        file=newfile.readlines() #salva as linhas do arquivo em uma lista
        #print("\nARQUIVO: " + file_in + "\n")
        #print("Total de linhas: " + str(len(file))) #número de linhas do arquivo
        nLinhas += len(file)
        nRecv = find_word("readUTF",file) #"procura" por recvs
        nSend = find_word("writeUTF",file) #"procura" por sends
        find_word("System.in",file) #"procura" por entradas
        find_word("System.out",file) #"procura" por saídas
        newfile.close()
        return nRecv, nSend
    except FileNotFoundError:
        print("\n----The file doesn't exist----")

#recebe do usuário os arquivos para se verificar
entrada = input ("NOME DE UM ARQUIVO: ") 
info = verify_file(entrada)
writingCode()

entrada2 = input ("NOME DE OUTRO ARQUIVO: ")
info2 = verify_file(entrada2)


#partindo do pressuposto que há sempre mais comandos que o necessário
try:
    if info[0] > info2[1]:
        print("\n\nSYNTAX ERROR: " + entrada + " tem recv em excesso")
    elif info[1] > info2[0]:
        print("\n\nSYNTAX ERROR: " + entrada + " tem send em excesso ")
    elif info2[0] > info[1]:
        print("\n\nSYNTAX ERROR: " + entrada2 + " tem recv em excesso ")
    elif info2[1] > info[0]:
        print("\n\nSYNTAX ERROR: " + entrada2 + " tem send em excesso ")
    writingCode()
except:
    print("Error.\nPlease try again")
os.startfile("teste.txt")