faturamento = 1000  # valor inicial do faturamento
custo = 700  # custo fixo
novas_vendas = 300  # novas vendas realizadas
faturamento = faturamento + novas_vendas  # atualiza o faturamento com as novas vendas
taxa_imposto = faturamento * 0.1  # 10% de imposto
lucro = faturamento - custo - taxa_imposto  # cálculo do lucro

print(faturamento)
print(lucro)
margem_lucro = lucro / faturamento  # margem de lucro
print( margem_lucro)  # exibe a margem de lucro em porcentagem
resttuição = taxa_imposto * 0.1  # restituição de 10% do imposto
print(resttuição)  # exibe o valor da restituição





tempo_em_meses = 160
tempo_em_anos = int(tempo_em_meses / 12)  # converte meses para anos
print(tempo_em_anos, "anos")  # exibe o tempo em anos
print(tempo_em_meses % 12, "meses")  # exibe o restante em meses