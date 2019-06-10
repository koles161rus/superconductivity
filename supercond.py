# Численное решение уравнения Лапласа с помощью метода конечных разностей
import numpy as np
import matplotlib.pyplot as plt
import random

# Максимальное число итераций
maxIter = 500

# Размерность и шаг
lenR = lenZ = 101
delta = 1

# Граничные условия
Utop = 0.75
Ubottom = 0
Uleft = 0.25
Uright = 0.25

# Стиль для отображения решения
colorinterpolation = 50
colourMap = plt.cm.jet

# Создание сетки
R, Z = np.meshgrid(np.arange(0, lenR), np.arange(0, lenZ))

# Создание массива и заполнение начальным условием
U = np.empty((lenR, lenZ))
U.fill(0)

# Заполнение массива граничными условиями
U[(lenZ-1):, :] = Utop
U[:1, :] = Ubottom
U[:, (lenR-1):] = Uright
U[:, :1] = Uleft

# Относительно случайное расположение островков сверхпроводимости
x01 = np.array([round(random.randint(5, 25)) for i in range(lenZ//20)])
x02 = np.array([round(random.randint(40, 60)) for i in range(lenZ//20)])
x03 = np.array([round(random.randint(75, 95)) for i in range(lenZ//20)])

print(x01, x02, x03)

# Численное решение
print("Подождите")
for iteration in range(0, maxIter):
    for i in range(0, lenR-1, delta):
        for j in range(0, lenZ-1, delta):
            U[i, j] = (U[i+1][j] + U[i-1][j] + U[i][j+1] + U[i][j-1]) / 4
            # Внедрение островков сверхпроводимости
            if i == j and i // 10 == i / 10:
                for k in range(5):
                    for l in range(15):
                        U[5+k*20+l, x01[k]] = 1
                        U[5+k*20+l, x02[k]] = 1
                        U[5+k*20+l, x03[k]] = 1

print("Выполнено")

# Получение напряжённости для тока и инициализация сумм тока и напряжения
gx, gy = np.gradient(U)

voltsum = 0
currsum = 0
condcoef = 1 #удельная электропроводность

# Вычисление эффективной проводимости
for i in range(0, lenZ-1, delta):
    if i < x02[2]-2 or i > x02[2]+2:
        voltsum += abs(gx[44, i])
        voltsum += abs(gy[44, i])
        currsum += U[44, i]
        currsum += abs(gy[44, i])
    elif i == x02[2]-1 or i == x02[2]+2:
        for j in range(44, 61, delta):
            voltsum += abs(gx[j, x02[2]-2])
            voltsum += abs(gy[j, x02[2]-2])
            voltsum += abs(gx[j, x02[2]+2])
            voltsum += abs(gy[j, x02[2]+2])
            currsum += U[j, x02[2]-2]
            currsum += U[j, x02[2]+2]
            currsum += abs(gx[j, x02[2]-2])
            currsum += abs(gx[j, x02[2]+2])
    else:
        voltsum += abs(gx[60, i])
        voltsum += abs(gy[60, i])
        currsum += U[60, i]
        currsum += abs(gy[60, i])

# Изображение решения
plt.title("Эффективная проводимость = " + str(condcoef * currsum / voltsum))
plt.contourf(R, Z, U, colorinterpolation, cmap=colourMap)
plt.plot([0, x02[2]-2], [44, 44], color="white")
plt.plot([x02[2]-2, x02[2]-2], [44, 60], color="white")
plt.plot([x02[2]-2, x02[2]+2], [60, 60], color="white")
plt.plot([x02[2]+2, x02[2]+2], [60, 44], color="white")
plt.plot([x02[2]+2, lenZ-1], [44, 44], color="white")

# Построение
plt.colorbar()

# Вывод на экран
plt.show()

print("")
