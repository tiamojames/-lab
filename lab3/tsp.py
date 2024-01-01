import numpy as np
import matplotlib.pyplot as plt

# 参数
citys = 30  # 染色体DNA长度
pc = 0.1  # 交叉概率
pm = 0.02  # 变异概率
popsize = 500  # 种群规模
iternum = 100  # 迭代次数

# 定义遗传算法类
class GA(object):
    def __init__(self, citys, pc, pm, popsize):
        self.citys = citys
        self.pc = pc
        self.pm = pm
        self.popsize = popsize

        # 生成随机初始种群
        self.pop = np.vstack([np.random.permutation(citys) for _ in range(popsize)])

    # 将DNA序列转换成坐标
    def translateDNA(self, DNA, city_position):
        lineX = np.empty_like(DNA, dtype=np.float64)
        lineY = np.empty_like(DNA, dtype=np.float64)
        for i, d in enumerate(DNA):
            city_coord = city_position[d]
            lineX[i, :] = city_coord[:, 0]
            lineY[i, :] = city_coord[:, 1]
        return lineX, lineY

    # 计算适应度和总距离
    def getFitness(self, lineX, lineY):
        totalDis = np.empty((lineX.shape[0],), dtype=np.float64)
        for i, (xval, yval) in enumerate(zip(lineX, lineY)):
            totalDis[i] = np.sum(np.sqrt(np.square(np.diff(xval)) + np.square(np.diff(yval))))
        fitness = np.exp(self.citys * 2 / totalDis)
        return fitness, totalDis

    # 选择
    def selection(self, fitness):
        idx = np.random.choice(np.arange(self.popsize), size=self.popsize, replace=True, p=fitness / fitness.sum())
        return self.pop[idx]

    # 交叉
    def crossover(self, parent, pop):
        if np.random.rand() < self.pc:
            i = np.random.randint(0, self.popsize, size=1)
            cross_points = np.random.randint(0, 2, self.citys).astype(bool)
            keep_city = parent[~cross_points]
            swap_city = pop[i, np.isin(pop[i].ravel(), keep_city, invert=True)]
            parent[:] = np.concatenate((keep_city, swap_city))
        return parent

    # 变异
    def mutation(self, child):
        for point in range(self.citys):
            if np.random.rand() < self.pm:
                swap_point = np.random.randint(0, self.citys)
                swapa, swapb = child[point], child[swap_point]
                child[point], child[swap_point] = swapb, swapa
        return child

    # 进化
    def evolve(self, fitness):
        pop = self.selection(fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = self.crossover(parent, pop_copy)
            child = self.mutation(child)
            parent[:] = child
        self.pop = pop

# 定义TSP问题类
class TSP(object):
    def __init__(self, citys):
        # self.city_position = np.random.rand(citys, 2)
        self.city_position = np.array([
            (87, 7), (91, 38), (83, 46), (71, 44), (64, 60),
            (68, 58), (83, 69), (87, 76), (74, 78), (71, 71),
            (58, 69), (54, 62), (51, 67), (37, 84), (41, 94),
            (2, 99), (7, 64), (22, 60), (25, 62), (18, 54),
            (4, 50), (13, 40), (18, 40), (24, 42), (25, 38),
            (41, 26), (45, 21), (44, 35), (58, 35), (62, 32)
        ], dtype=np.float64)  # 将坐标数据归一化到[0, 1]范围内
        plt.ion()

    # 绘制图形
    def plotting(self, lx, ly, total_d):
        plt.cla()
        plt.scatter(self.city_position[:, 0].T, self.city_position[:, 1].T, s=100, c='k')
        plt.plot(lx.T, ly.T, 'r-')
        plt.text(-0.05, -0.05, "Total distance=%.2f" % total_d, fontdict={'size': 20, 'color': 'red'})
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
        plt.pause(0.01)

if __name__ == '__main__':
    ga = GA(citys=citys, pc=pc, pm=pm, popsize=popsize)
    env = TSP(citys=citys)

    for gen in range(iternum):
        lx, ly = ga.translateDNA(ga.pop, env.city_position)
        fitness, total_distance = ga.getFitness(lx, ly)
        ga.evolve(fitness)
        best_idx = np.argmax(fitness)
        print("Gen:", gen, " | best fit: %.2f" % fitness[best_idx], )

    env.plotting(lx[best_idx], ly[best_idx], total_distance[best_idx])

    plt.ioff()
    plt.show()
