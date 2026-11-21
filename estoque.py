import json
import math

nomes = []
precos = []
quantidades = []
estoque_minimo = []

opcao = 0

try:
    with open('estoque.json', 'r') as arquivo:
        dados = json.load(arquivo)

        nomes = dados['nomes']
        precos = dados['precos']
        quantidades = dados['quantidades']
        estoque_minimo = dados['estoque_minimo']

    if not all(isinstance(lista, list) for lista in (nomes, precos, quantidades, estoque_minimo)):
        raise ValueError('Os dados do estoque devem estar organizados em listas.')

    if not (len(nomes) == len(precos) == len(quantidades) == len(estoque_minimo)):
        raise ValueError('As listas do estoque possuem tamanhos diferentes.')

    if not all(isinstance(nome, str) for nome in nomes):
        raise ValueError('Existem nomes de produtos inválidos.')

    if not all(isinstance(preco, (int, float)) and math.isfinite(preco) and preco > 0 for preco in precos):
        raise ValueError('Existem preços inválidos.')

    if not all(isinstance(qntd, int) and qntd >= 0 for qntd in quantidades):
        raise ValueError('Existem quantidades inválidas.')

    if not all(isinstance(minimo, int) and minimo >= 0 for minimo in estoque_minimo):
        raise ValueError('Existem valores de estoque mínimo inválidos.')

except FileNotFoundError:
    print('Arquivo de estoque ainda não existe.' )

except json.JSONDecodeError:
    print('Erro: o arquivo de estoque está vazio ou contém dados inválidos.')

except KeyError as erro:
    print(f'Erro: está faltando uma informação no arquivo JSON: {erro}')

except ValueError as erro:
    print(f'Erro nos dados do estoque: {erro}')   

def salvar_dados():
    dados = {
        'nomes': nomes,
        'precos': precos,
        'quantidades': quantidades,
        'estoque_minimo': estoque_minimo
    }

    with open('estoque.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)   

def cadastrar_produtos():
    while True:         
        print('\n========== CADASTRO DE PRODUTO ==========')
        nome = input('Nome do produto: ').strip()
    
        if nome == '':
            print('O nome do produto não pode ficar vazio!')
    
        elif nome.lower() in [n.strip().lower() for n in nomes]:
            print('Esse produto já existe!')
    
        else:
            break
    
    while True:
        try:
            preco = float(input('Digite o valor: ').replace(',', '.'))
            if not math.isfinite(preco) or preco <= 0:
                print('Erro: o preço deve ser um valor maior que R$ 0,00.')
                continue
    
            else:
                break
        except ValueError:
            print('Erro: digite valores numéricos válidos!')
            continue
    
    while True:
        try:      
            qntd = int(input('Digite a quantidade: '))
            if qntd < 0 :
                print('A quantidade não pode ser negativa!')
                continue
            else:
                break
    
        except ValueError:
            print('Erro: digite um número inteiro válido!')
    
    while True:
        try:
            estoqMin = int(input('Qual a quantidade mínima que deve permanecer no estoque? '))
            if estoqMin < 0:
                print('O estoque mínimo não pode ser negativo!')
            else:
                break
    
        except ValueError:
            print('Erro: digite um número inteiro válido!')
    
    nomes.append(nome)
    precos.append(preco)
    quantidades.append(qntd)
    estoque_minimo.append(estoqMin)
    
    salvar_dados()
    
    print(f'Produto "{nome}" cadastrado com sucesso!')

def consultar_produtos():
    if len(nomes) == 0:
        print('Nenhum produto cadastrado.')
    else:
        print('\n========== PRODUTOS CADASTRADOS ==========')
        print(f'{"PRODUTO":<20} {"PREÇO":<12} {"ESTOQUE":<10} {"MÍNIMO":<10} SITUAÇÃO')

        produtos_baixos = 0

        for i in range(len(nomes)):
            if quantidades[i] <= estoque_minimo[i]:
                situacao = 'REPOR'
                produtos_baixos += 1
            else:
                situacao = 'NORMAL'
            print(f'{nomes[i]:<20} R$ {precos[i]:<9.2f} {quantidades[i]:<10} {estoque_minimo[i]:<10} {situacao}')

        print(f'Total de produtos cadastrados: {len(nomes)}')


        total_unidades = sum(quantidades)
        print(f'Total de unidades em estoque: {total_unidades}')

        valor_total = 0

        for i in range(len(nomes)):
            valor_total += precos[i] * quantidades[i]

        print(f'Valor total do estoque: R$ {valor_total:.2f}')

        print(f'Produtos precisando de reposição: {produtos_baixos}')

        percentual = (produtos_baixos / len(nomes)) * 100
        print(f'Percentual de produtos precisando de reposição: {percentual:.1f}%')
        print('==========================================')

def registrar_entrada():
    atualizar = input('Qual o produto que deseja atualizar? ').strip().lower()
    encontrou = False

    for i in range(len(nomes)):
        if nomes[i].lower() == atualizar:
            encontrou = True
            print(f'Produto "{nomes[i]}" encontrado!')
            while True:
                try:
                    entrada = int(input('Quantas unidades chegaram? '))

                    if entrada > 0:
                        break
                    else:
                        print('A entrada deve ser maior que zero!')
                        
                except ValueError:
                    print('Erro: digite uma quantidade inteira válida.')
                    continue

            quantidades[i] += entrada

            print(f'Entrada de {entrada} unidades registrada com sucesso!')
            print(f'Estoque atualizado de {nomes[i]}: {quantidades[i]} unidades.')

            salvar_dados()

    if not encontrou:
        print('Produto não encontrado.')

def registrar_saida():
    retirar = input('Qual produto deseja retirar? ').strip().lower()
    encontrou = False

    for i in range(len(nomes)):
        if nomes[i].lower() == retirar:
            encontrou = True
            print(f'Produto "{nomes[i]}" encontrado!')

            while True:
                try:
                    saida = int(input('Quantas unidades deseja retirar? '))

                    if saida <= 0:
                        print('A saída deve ser maior que zero!')

                    elif saida > quantidades[i]:
                        print('Quantidade solicitada superior ao estoque disponível!')

                    else:
                        break

                except ValueError:
                    print('Erro: digite valores numéricos válidos!')

            quantidades[i] -= saida
            print(f'Saída de {saida} unidades registrada com sucesso!')
            print(f'Estoque atualizado de {nomes[i]}: {quantidades[i]} unidades.')

            salvar_dados()

    if not encontrou:
        print('Produto não encontrado')

def verificar_estoque_baixo():
    encontrouAbaixo = False

    if len(nomes) == 0:
        print('Nenhum produto cadastrado.')

    else:
        for i in range(len(nomes)):
            if quantidades[i] <= estoque_minimo[i]:
                if not encontrouAbaixo:
                    print('\n========== ALERTA DE ESTOQUE BAIXO ==========')
                    encontrouAbaixo = True

                print(f'{nomes[i]} | Disponível: {quantidades[i]} UN | Mínimo: {estoque_minimo[i]} UN')

        if not encontrouAbaixo:
            print('Nenhum produto está com o estoque baixo.')

def sair_programa():
    print('\nPrograma encerrado. Até mais!')

while True:
    print('=== SISTEMA DE ESTOQUE ===')
    print('1 - Cadastrar produto')
    print('2 - Consultar produtos')
    print('3 - Registrar entrada')
    print('4 - Registrar saída')
    print('5 - Produtos com estoque baixo')
    print('6 - Sair')

    try:
        opcao = int(input('Escolha uma opção: '))

    except ValueError:
        print('\nDigite apenas números!')
        continue

    if opcao == 1:
        cadastrar_produtos()

    elif opcao == 2: 
        consultar_produtos()

    elif opcao == 3: 
        registrar_entrada()
        
    elif opcao == 4:
        registrar_saida()

    elif opcao == 5: 
        verificar_estoque_baixo()

    elif opcao == 6:
        sair_programa()
        break
    else:
        print('Opção inválida, tente novamente')   