#%%
from Bio import Entrez
from Bio import SeqIO
from collections import Counter
from urllib.error import HTTPError
import random
import matplotlib.pyplot as plt

# Configurar o email para o NCBI Entrez
Entrez.email = "profissionalrobertgabriel@gmail.com"
#%%
# Função para buscar sequências do NCBI
def buscar_sequencias(codigo_ncbi):
    try:
        handle = Entrez.efetch(db="nucleotide", id=codigo_ncbi, rettype="fasta", retmode="text")
        seq_records = list(SeqIO.parse(handle, "fasta"))
        handle.close()
        return seq_records
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return []

# Buscar sequências usando o código NCBI
codigo_ncbi = "18281244"  # Use a valid NCBI identifier
sequences = buscar_sequencias(codigo_ncbi)

# Iterar sobre as sequências e imprimir algumas informações
for seq_record in sequences:
    print(f"ID: {seq_record.id}")
    print(f"Description: {seq_record.description}")
    print(f"Sequence length: {len(seq_record.seq)}")
    print(f"Sequence: {seq_record.seq[:50]}...")  # Imprimir os primeiros 50 nucleotídeos

# Função para contar nucleotídeos
def contar_nucleotideos(seq):
    return Counter(seq)

# Função para plotar gráfico de barras dos nucleotídeos
def plotar_nucleotideos(contagem, seq_id):
    nucleotideos = list(contagem.keys())
    contagens = list(contagem.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(nucleotideos, contagens, color='blue')
    plt.xlabel('Nucleotídeos')
    plt.ylabel('Contagem')
    plt.title(f'Contagem de Nucleotídeos para {seq_id}')
    plt.show()
#%%
# Análise adicional: contagem de nucleotídeos e plotagem
for seq_record in sequences:
    contagem = contar_nucleotideos(seq_record.seq)
    print(f"Contagem de nucleotídeos para {seq_record.id}: {contagem}")
    plotar_nucleotideos(contagem, seq_record.id)
# %%
# Função para calcular a porcentagem de nucleotídeos
def calcular_porcentagem_nucleotideos(seq):
    contagem = contar_nucleotideos(seq)
    total = len(seq)
    porcentagem = {nuc: (count / total) * 100 for nuc, count in contagem.items()}
    return porcentagem

# Função para encontrar regiões de alta GC
def encontrar_regioes_gc(seq, window_size=100, gc_threshold=50):
    gc_rich_regions = []
    for i in range(0, len(seq) - window_size + 1, window_size):
        window = seq[i:i + window_size]
        gc_content = (window.count('G') + window.count('C')) / window_size * 100
        if gc_content >= gc_threshold:
            gc_rich_regions.append((i, i + window_size, gc_content))
    return gc_rich_regions

# Função para plotar a porcentagem de nucleotídeos
def plotar_porcentagem_nucleotideos(porcentagem, seq_id):
    nucleotideos = list(porcentagem.keys())
    porcentagens = list(porcentagem.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(nucleotideos, porcentagens, color='green')
    plt.xlabel('Nucleotídeos')
    plt.ylabel('Porcentagem')
    plt.title(f'Porcentagem de Nucleotídeos para {seq_id}')
    plt.show()

# Análise adicional: porcentagem de nucleotídeos e regiões de alta GC
for seq_record in sequences:
    porcentagem = calcular_porcentagem_nucleotideos(seq_record.seq)
    print(f"Porcentagem de nucleotídeos para {seq_record.id}: {porcentagem}")
    plotar_porcentagem_nucleotideos(porcentagem, seq_record.id)
    
    regioes_gc = encontrar_regioes_gc(seq_record.seq)
    print(f"Regiões de alta GC para {seq_record.id}: {regioes_gc}")
# %%
# Função para plotar a distribuição do comprimento das sequências
def plotar_distribuicao_comprimento(sequences):
    comprimentos = [len(seq_record.seq) for seq_record in sequences]
    
    plt.figure(figsize=(10, 6))
    plt.hist(comprimentos, bins=20, color='purple', edgecolor='black')
    plt.xlabel('Comprimento da Sequência')
    plt.ylabel('Frequência')
    plt.title('Distribuição do Comprimento das Sequências')
    plt.show()

# Função para plotar a distribuição de regiões de alta GC
def plotar_distribuicao_gc(regioes_gc, seq_id):
    gc_contents = [gc_content for _, _, gc_content in regioes_gc]
    
    plt.figure(figsize=(10, 6))
    plt.hist(gc_contents, bins=20, color='orange', edgecolor='black')
    plt.xlabel('Conteúdo GC (%)')
    plt.ylabel('Frequência')
    plt.title(f'Distribuição de Regiões de Alta GC para {seq_id}')
    plt.show()

# Plotar a distribuição do comprimento das sequências
plotar_distribuicao_comprimento(sequences)

# Plotar a distribuição de regiões de alta GC para cada sequência
for seq_record in sequences:
    regioes_gc = encontrar_regioes_gc(seq_record.seq)
    plotar_distribuicao_gc(regioes_gc, seq_record.id)
# %%



#%%
# Função para gerar uma sequência aleatória
def gerar_sequencia_aleatoria(tamanho):
    nucleotideos = ['A', 'T', 'C', 'G']
    return ''.join(random.choices(nucleotideos, k=tamanho))

# Função para calcular a similaridade entre duas sequências
def calcular_similaridade(seq1, seq2):
    if len(seq1) != len(seq2):
        raise ValueError("As sequências devem ter o mesmo comprimento para calcular a similaridade.")
    
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return matches / len(seq1) * 100

# Gerar uma sequência aleatória de mesmo comprimento
sequencia_aleatoria = gerar_sequencia_aleatoria(534)

# Calcular a similaridade entre a sequência original e a sequência aleatória
for seq_record in sequences:
    similaridade = calcular_similaridade(seq_record.seq, sequencia_aleatoria)
    print(f"Similaridade entre {seq_record.id} e a sequência aleatória: {similaridade:.2f}%")

# Função para plotar a similaridade entre duas sequências
def plotar_similaridade(seq1, seq2, seq_id):
    if len(seq1) != len(seq2):
        raise ValueError("As sequências devem ter o mesmo comprimento para plotar a similaridade.")
    
    matches = [1 if a == b else 0 for a, b in zip(seq1, seq2)]
    
    plt.figure(figsize=(15, 4))
    plt.plot(matches, color='blue', marker='o', linestyle='None', markersize=4, label='Match')
    plt.axhline(y=0.5, color='red', linestyle='--', label='Threshold')
    plt.xlabel('Posição')
    plt.ylabel('Similaridade')
    plt.title(f'Similaridade entre {seq_id} e a sequência aleatória')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotar a similaridade entre a sequência original e a sequência aleatória
for seq_record in sequences:
    plotar_similaridade(seq_record.seq, sequencia_aleatoria, seq_record.id)
# %%
