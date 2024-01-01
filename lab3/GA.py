import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

# TSP 类：代表旅行商问题
class TSP:
    # City 子类：表示具有坐标 (x, y) 的城市
    class City:
        def __init__(self, x, y):
            self.x = x  # 城市的 x 坐标
            self.y = y  # 城市的 y 坐标

        # 计算到另一个城市的欧几里得距离
        def distance(self, city):
            x_dis = abs(self.x - city.x)
            y_dis = abs(self.y - city.y)
            return np.sqrt((x_dis ** 2) + (y_dis ** 2))

        # 城市的字符串表示（坐标）
        def __repr__(self):
            return f"({self.x},{self.y})"

    # 静态方法：绘制路线图
    @staticmethod
    def plot_route(route):
        x, y = zip(*[(city.x, city.y) for city in route])  # 提取所有城市的坐标
        plt.plot(x, y, 'ro-')  # 绘制路线图
        plt.title("Route")  # 图表标题
        plt.xlabel("X Coordinate")  # x轴标签
        plt.ylabel("Y Coordinate")  # y轴标签
        plt.show()  # 显示图表

# GA 类：实现遗传算法
class GA:
    # Fitness 子类：用于评估路径适应度
    class Fitness:
        def __init__(self, route):
            self.route = route  # 路径
            self.distance = 0  # 路径长度
            self.fitness = 0.0  # 路径的适应度值

        # 计算路径的总距离
        def route_distance(self):
            if self.distance == 0:
                path_distance = 0
                for i in range(len(self.route)):
                    from_city = self.route[i]
                    to_city = self.route[i + 1] if i + 1 < len(self.route) else self.route[0]
                    path_distance += from_city.distance(to_city)
                self.distance = path_distance
            return self.distance

        # 计算路径的适应度
        def route_fitness(self):
            if self.fitness == 0:
                self.fitness = 1 / float(self.route_distance())  # 适应度是路径长度的倒数
            return self.fitness

    # 初始化遗传算法类
    def __init__(self, population, pop_size, elite_size, mutation_rate, generations):
        self.population = population  # 初始种群
        self.pop_size = pop_size  # 种群大小
        self.elite_size = elite_size  # 精英大小
        self.mutation_rate = mutation_rate  # 变异率
        self.generations = generations  # 迭代代数

    # 创建随机路径
    @staticmethod
    def create_route(city_list):
        return random.sample(city_list, len(city_list))

    # 创建初始种群
    def initial_population(self):
        return [self.create_route(self.population) for _ in range(self.pop_size)]

    # 对路径进行排名
    @staticmethod
    def rank_routes(population):
        fitness_results = {i: GA.Fitness(population[i]).route_fitness() for i in range(len(population))}
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)

    # 选择函数
    def selection(self, pop_ranked):
        selection_results = []
        df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(self.elite_size):
            selection_results.append(pop_ranked[i][0])
        for _ in range(len(pop_ranked) - self.elite_size):
            pick = 100 * random.random()
            for i in range(len(pop_ranked)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(pop_ranked[i][0])
                    break
        return selection_results

    # 生成配对池
    def mating_pool(self, population, selection_results):
        return [population[i] for i in selection_results]

    # 交叉（繁殖）函数
    @staticmethod
    def breed(parent1, parent2):
        geneA, geneB = random.sample(range(len(parent1)), 2)
        start_gene, end_gene = sorted([geneA, geneB])
        childP1 = parent1[start_gene:end_gene]
        childP2 = [item for item in parent2 if item not in childP1]
        return childP1 + childP2

    # 繁殖种群
    def breed_population(self, matingpool):
        children = matingpool[:self.elite_size]
        length = len(matingpool) - self.elite_size
        pool = random.sample(matingpool, len(matingpool))

        for i in range(length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    # 变异函数
    @staticmethod
    def mutate(individual, mutation_rate):
        for swapped in range(len(individual)):
            if random.random() < mutation_rate:
                swap_with = int(random.random() * len(individual))
                individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
        return individual

    # 变异种群
    def mutate_population(self, population):
        return [self.mutate(individual, self.mutation_rate) for individual in population]

    # 生成下一代种群
    def next_generation(self, current_gen):
        pop_ranked = self.rank_routes(current_gen)
        selection_results = self.selection(pop_ranked)
        matingpool = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(matingpool)
        return self.mutate_population(children)

    # 运行遗传算法
    def run(self):
        pop = self.initial_population()  # 初始化种群
        print("Initial distance: " + str(1 / self.rank_routes(pop)[0][1]))

        best_distance = 1 / self.rank_routes(pop)[0][1]  # 初始化最佳距离
        best_generation = 0  # 记录达到最佳距离的代数
        best_route = None  # 初始化最佳路线

        for i in range(self.generations):  # 对每一代进行迭代
            pop = self.next_generation(pop)  # 生成下一代种群
            current_best_distance = 1 / self.rank_routes(pop)[0][1]  # 获取当前代的最佳距离

            if current_best_distance < best_distance:  # 如果找到更短的路径
                best_distance = current_best_distance  # 更新最佳距离
                best_generation = i + 1  # 更新最佳代数
                best_route_index = self.rank_routes(pop)[0][0]  # 获取最佳路径的索引
                best_route = pop[best_route_index]  # 更新最佳路径

            print(f"Generation {i + 1}: Distance = {current_best_distance}")

        print(f"Generation {best_generation} : Final distance: {best_distance} ")
        if best_route:
            # 将 best_route 中的城市坐标转换为在 coordinates 列表中的索引
            best_route_indices = [coordinates.index((city.x, city.y)) for city in best_route]
            best_route_indices.append(best_route_indices[0])


        print("Best route:", best_route_indices)
        return best_route if best_route else pop[self.rank_routes(pop)[0][0]]

#10个城市
coordinates = [(87, 7), (91, 38), (83, 46), (71, 44), (64, 60), (68, 58), (83, 69), (87, 76), (74, 78), (71, 71)]


# coordinates = [
#     (87, 7), (91, 38), (83, 46), (71, 44), (64, 60),
#     (68, 58), (83, 69), (87, 76), (74, 78), (71, 71),
#     (58, 69), (54, 62), (51, 67), (37, 84), (41, 94),
#     (2, 99), (7, 64), (22, 60), (25, 62), (18, 54),
#     (4, 50), (13, 40), (18, 40), (24, 42), (25, 38),
#     (41, 26), (45, 21), (44, 35), (58, 35), (62, 32)
# ]
citys = [TSP.City(x, y) for x, y in coordinates]
ga = GA(population=citys, pop_size=100, elite_size=20, mutation_rate=0.01, generations=500)
best_route = ga.run()
TSP.plot_route(best_route)
