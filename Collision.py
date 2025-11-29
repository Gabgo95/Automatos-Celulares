"""# Colisão"""

# Tamanho da grade
N = 200

# Estados: 0 = vazio, 1 = norte, 2 = sul, 3 = leste, 4 = oeste
# Cada célula pode conter múltiplas partículas (usamos listas)
grid = [[[] for _ in range(N)] for _ in range(N)]

# Inicializa partículas aleatórias
for _ in range(300):
    i, j = np.random.randint(0, N, size=2)
    direction = np.random.choice([1, 2, 3, 4])
    grid[i][j].append(direction)

# Função para atualizar a grade
def update(frameNum, img, grid, N):
    new_grid = [[[] for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for d in grid[i][j]:
                if d == 1:  # norte
                    new_i = (i - 1) % N
                    new_j = j
                elif d == 2:  # sul
                    new_i = (i + 1) % N
                    new_j = j
                elif d == 3:  # leste
                    new_i = i
                    new_j = (j + 1) % N
                elif d == 4:  # oeste
                    new_i = i
                    new_j = (j - 1) % N
                new_grid[new_i][new_j].append(d)

    # Colisões: se norte e sul na mesma célula → viram leste e oeste
    # se leste e oeste → viram norte e sul
    for i in range(N):
        for j in range(N):
            d = new_grid[i][j]
            if 1 in d and 2 in d:
                new_grid[i][j] = [3, 4]
            elif 3 in d and 4 in d:
                new_grid[i][j] = [1, 2]

    # Visualização: número de partículas por célula
    img.set_data([[len(cell) for cell in row] for row in new_grid])
    for i in range(N):
        for j in range(N):
            grid[i][j] = new_grid[i][j]
    return img,

# Visualização
fig, ax = plt.subplots()
img = ax.imshow([[len(cell) for cell in row] for row in grid], cmap='viridis', interpolation='nearest')
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N), frames=100, interval=100)

HTML(ani.to_jshtml())
