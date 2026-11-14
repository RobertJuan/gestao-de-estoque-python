import json

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

except FileNotFoundError:
    print('Arquivo de estoque ainda não existe.' )

def salvar_dados():
    dados = {
        'nomes': nomes,
        'precos': precos,
        'quantidades': quantidades,
        'estoque_minimo': estoque_minimo
    }

    with open('estoque.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)    

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

#1 - Cadastrar produto

    if opcao == 1:
        while True:         
            print('Cadastre um poduto')
            nome = input('Nome do produto: ').strip()

            if nome == '':
                print('O nome do produto não pode ficar vazio!')

            elif nome in nomes:
                print('Esse produto já existe!')

            else:
                break

        while True:
            try:
                preco = float(input('Digite o valor: ').replace(',', '.'))
                if preco <= 0:
                    print('O preço deve ser maior que zero!')
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

        print('Cadastro realizado.')

#2 - Consultar produtos

    elif opcao == 2: 
        if len(nomes) == 0:
            print('Nenhum produto cadastrado')
        else:
            print('produto|Preço|Estoque')
            for i in range(len(nomes)):
                print(f'{nomes[i]} - {precos[i]:.2f} - {quantidades[i]}')

#3 - Registrar entrada

    elif opcao == 3: 
        atualizar = input('Qual o produto que deseja atualizar? ')
        encontrou = False

        for i in range(len(nomes)):
            if nomes[i] == atualizar:
                encontrou = True
                print('produto encontrado!')
                while True:
                    try:
                        entrada = int(input('Quantas unidades chegaram? '))

                        if entrada > 0:
                            break
                        else:
                            print('A entrada deve ser maior que zero!')
                        
                    except ValueError:
                        print('Erro: digite valores numéricos válidos!')
                        continue

                quantidades[i] += entrada

                print(f'Novo estoque: {quantidades[i]}')

                salvar_dados()

        if not encontrou:
            print('Produto não encontrado')
        
    elif opcao == 4:
        retirar = input('Qual produto deseja retirar? ')
        encontrou = False

        for i in range(len(nomes)):
            if nomes[i] == retirar:
                encontrou = True
                print('Produto encontrado!')

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
                print('Saída registrada.')
                print(f'Novo estoque: {quantidades[i]}')

                salvar_dados()

        if not encontrou:
            print('Produto não encontrado')

    elif opcao == 5: 
        encontrouAbaixo = False

        if len(nomes) == 0:
            print('Nenhum produto cadastrado.')

        else:
            for i in range(len(nomes)):
                if quantidades [i] <= estoque_minimo[i]:
                    encontrouAbaixo = True
                    print(f'Produtos com estoque baixo')
                    print(f'o produto {nomes[i]} esta com o estoque baixo | estoque atual: {quantidades[i]} UN - estoque minimo: {estoque_minimo[i]} UN')

            if not encontrouAbaixo:
                print('Nenhum produto está com o estoque baixo.')

    elif opcao == 6:
        print('Programa encerrado')
        break
    else:
        print('Opção invalida, tente novamente')    