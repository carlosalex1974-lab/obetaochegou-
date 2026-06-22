Faturamento = 1000
Custo = 350
Lucro = Faturamento - Custo
novas_vendas = 101
Faturamento = Faturamento + novas_vendas

taxa_imposto = 0.2  #20% de imposto float
mensagem = "O faturamento foi de " # string com informações do faturamento = texto
teve_lucro = True # booleano indicando se teve lucro ou não

imposto = taxa_imposto * Faturamento  # cálculo do imposto


print("Faturamento", Faturamento)
print("Custo", Custo)
print("Lucro", Faturamento - Custo - imposto)
print(mensagem, Faturamento)