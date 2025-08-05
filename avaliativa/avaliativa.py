produtos = []
clientes = []
vendas = []

def cadastrar_produto():
    try:
        nome = input("Nome do produto: ").strip()
        tipo = input("Tipo (unidade/quilo): ").lower()
        if tipo not in ["unidade", "quilo"]:
            print("Tipo inválido.")
            return
        preco = float(input("Preço: R$ "))
        quantidade = float(input("Quantidade inicial: "))
        desconto = float(input("Desconto (%): "))
        produto = {
            "nome": nome,
            "tipo": tipo,
            "preco": preco,
            "quantidade": quantidade,
            "desconto": desconto,
            "vendido": 0
        }
        produtos.append(produto)
        print("✅ Produto cadastrado com sucesso!")
    except ValueError:
        print("❌ Entrada inválida. Use números onde for necessário.")

def cadastrar_cliente():
    nome = input("Nome do cliente: ").strip()
    antigo = input("Cliente antigo? (s/n): ").lower()
    cliente = {
        "nome": nome,
        "antigo": antigo == 's'
    }
    clientes.append(cliente)
    print("✅ Cliente cadastrado!")

def realizar_venda():
    if not produtos:
        print("❌ Nenhum produto cadastrado!")
        return
    if not clientes:
        print("❌ Nenhum cliente cadastrado!")
        return

    print("\n--- CLIENTES ---")
    for c in clientes:
        print(f"- {c['nome']} ({'Antigo' if c['antigo'] else 'Novo'})")
    
    nome_cliente = input("Digite o nome do cliente: ").strip()
    cliente = next((c for c in clientes if c["nome"].lower() == nome_cliente.lower()), None)
    if not cliente:
        print("❌ Cliente não encontrado.")
        return

    forma = input("Forma de pagamento (dinheiro/pix/cartao): ").lower()
    if forma not in ["dinheiro", "pix", "cartao"]:
        print("❌ Forma inválida.")
        return

    total = 0
    itens = []

    while True:
        print("\n--- PRODUTOS DISPONÍVEIS ---")
        for p in produtos:
            print(f"- {p['nome']} | R$ {p['preco']:.2f} | Qtd: {p['quantidade']} | Desc: {p['desconto']}%")

        nome_prod = input("Produto (ou 'fim' para encerrar): ").strip().lower()
        if nome_prod == "fim":
            break

        produto = next((p for p in produtos if p["nome"].lower() == nome_prod), None)
        if not produto:
            print("❌ Produto não encontrado.")
            continue

        try:
            qtd = float(input("Quantidade: "))
        except ValueError:
            print("❌ Quantidade inválida.")
            continue

        if qtd <= 0 or produto["quantidade"] < qtd:
            print("❌ Estoque insuficiente ou valor inválido.")
            continue

        preco_final = produto["preco"] * (1 - produto["desconto"] / 100)
        subtotal = preco_final * qtd
        produto["quantidade"] -= qtd
        produto["vendido"] += qtd
        total += subtotal
        itens.append((produto["nome"], qtd, preco_final))

    if total == 0:
        print("❌ Nenhum produto vendido.")
        return

    comissao = total * 0.05 if forma in ["pix", "dinheiro"] else total * 0.03

    vendas.append({
        "cliente": cliente["nome"],
        "forma": forma,
        "total": total,
        "comissao": comissao,
        "itens": itens
    })

    print(f"✅ Venda finalizada! Total: R$ {total:.2f}")
    print(f"Comissão: R$ {comissao:.2f}")

def relatorio_mais_vendido():
    if not produtos:
        print("❌ Nenhum produto cadastrado.")
        return
    mais_vendido = max(produtos, key=lambda p: p["vendido"])
    print(f"📊 Produto mais vendido: {mais_vendido['nome']} ({mais_vendido['vendido']})")

def alerta_estoque_baixo():
    for p in produtos:
        if p["quantidade"] <= 2:
            print(f"⚠️ Estoque baixo: {p['nome']} - {p['quantidade']} restantes")

def realizar_devolucao():
    nome_prod = input("Produto a devolver: ").strip().lower()
    produto = next((p for p in produtos if p["nome"].lower() == nome_prod), None)
    if not produto:
        print("❌ Produto não encontrado.")
        return
    try:
        qtd = float(input("Quantidade devolvida: "))
        if qtd <= 0:
            print("❌ Quantidade inválida.")
            return
        produto["quantidade"] += qtd
        produto["vendido"] = max(0, produto["vendido"] - qtd)
        print("✅ Devolução registrada.")
    except ValueError:
        print("❌ Use um número válido.")

def menu():
    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar produto")
        print("2 - Cadastrar cliente")
        print("3 - Realizar venda")
        print("4 - Relatório mais vendido")
        print("5 - Alerta de estoque baixo")
        print("6 - Devolução")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            cadastrar_cliente()
        elif opcao == "3":
            realizar_venda()
        elif opcao == "4":
            relatorio_mais_vendido()
        elif opcao == "5":
            alerta_estoque_baixo()
        elif opcao == "6":
            realizar_devolucao()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("❌ Opção inválida.")

menu()
