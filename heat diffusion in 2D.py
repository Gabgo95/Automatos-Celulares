"""#Difusão de calor em 2D"""

# --- Parâmetros ---
# Tamanho da grade
N = 50
# Posição da fonte de calor
heat_source_pos = (N // 2, N // 2)
# Intensidade da fonte de calor
HEAT_SOURCE_VALUE = 100

# --- Inicialização ---
# Cria a grade com todos os pontos a zero
grid = np.zeros((N, N))
# Define a fonte de calor no centro
grid[heat_source_pos] = HEAT_SOURCE_VALUE

# --- Função de Atualização (Regra de Difusão) ---
def update(frameNum, img, grid, N, heat_source_pos, heat_source_value):
    """
    Atualiza a grade do modelo de difusão de calor.
    Cada ponto da grade recebe a média da temperatura de seus vizinhos.
    A fonte de calor é mantida constante em sua posição.
    """
    # Cria uma cópia da grade para evitar modificar os valores usados no cálculo
    new_grid = grid.copy()

    # Percorre cada célula da grade
    for i in range(N):
        for j in range(N):
            # A fonte de calor não é alterada.
            # Se for, o calor vai se dissipar em vez de se propagar.
            if (i, j) == heat_source_pos:
                continue

            # Média dos vizinhos (usando condição de contorno periódica/toroidal)
            neighbors_sum = (
                grid[(i - 1 + N) % N, j] +
                grid[(i + 1) % N, j] +
                grid[i, (j - 1 + N) % N] +
                grid[i, (j + 1) % N]
            )

            # A nova temperatura é a média da temperatura dos vizinhos
            new_grid[i, j] = 0.25 * neighbors_sum

    # Atualiza a imagem com os novos dados
    img.set_data(new_grid)
    # Copia a nova grade para a grade original para a próxima iteração
    grid[:] = new_grid[:]
    return img,

# --- Visualização e Animação ---
# Configura a figura e a visualização
fig, ax = plt.subplots(figsize=(6, 6))
# A cor 'hot' é ideal para a visualização de calor
img = ax.imshow(grid, cmap='hot', interpolation='nearest', vmin=0, vmax=HEAT_SOURCE_VALUE)
ax.set_xticks([])
ax.set_yticks([])

# Cria a animação
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, heat_source_pos, HEAT_SOURCE_VALUE),
                              frames=200, interval=50, blit=True)

# Exibe a animação no notebook
HTML(ani.to_jshtml())
