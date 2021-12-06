from random import randint, uniform, sample


class GeneticAlgorithm:
    def __init__(self, evaluation_function, amount_of_genes, max_steps, population_limit, survive_ratio,
                 productivity_ratio, stop_fitness):
        self.evaluation_function = evaluation_function
        self.amount_of_genes = amount_of_genes
        self.max_steps = max_steps
        self.population_limit = population_limit
        self.survive_ratio = survive_ratio
        self.productivity_ratio = productivity_ratio
        self.stop_fitness = stop_fitness

        self.bounds = (-100, 100)
        self.best_gene = None

    def solve(self):
        # empty population
        gene_population = []

        for i in range(self.max_steps):
            print(f"Step #{i}")
            population = self.generate_population(gene_population)
            if not self.best_gene:
                self.best_gene = population[0]

            best = self.survive(population)
            gene_population = self.crossover(best)

            self.best_gene = max(self.best_gene, best[0], key=lambda i: i[1])

            print(f"Best iteration gene {self.best_gene[0]}. Result: {self.best_gene[1]}")
            print("\n")

            if self.stop_fitness is not None and self.best_gene[1] >= self.stop_fitness:
                print(f"Complete: {self.best_gene[1]} <= {self.stop_fitness}")
                break

        return self.best_gene

    def mutate(self, gene):
        # mutate one random gene
        gene_id = randint(0, len(gene) - 1)
        gene[gene_id] = round(uniform(self.bounds[0], self.bounds[1]))
        return gene

    def mutate_old_population(self, old_population):
        new_population = []
        for item in old_population:
            item = self.mutate(item)
            fitness = self.evaluation_function(item)
            new_population.append((item, fitness))
        return new_population

    def create_new_random_population(self, new_population_limit):
        new_population = []
        for i in range(new_population_limit):
            new_gene = []
            for gene_id in range(self.amount_of_genes):
                gene = round(uniform(self.bounds[0], self.bounds[1]))
                new_gene.append(gene)
            fitness = self.evaluation_function(new_gene)
            new_population.append((new_gene, fitness))
        return new_population

    def generate_population(self, old_population):
        # mutate old population
        new_population = self.mutate_old_population(old_population)

        # create new population
        new_population_limit = self.population_limit - len(new_population)

        new_random_population = self.create_new_random_population(new_population_limit)

        new_population += new_random_population
        return new_population

    def crossover(self, population):
        newborns = []
        for _ in range(len(population) * self.productivity_ratio):
            dad, mom = sample(population, 2)
            child = []
            for gene_m, gene_f, idx in zip(dad[0], mom[0], range(len(dad[0]))):
                if idx % 2 == 0:
                    gene = gene_m
                else:
                    gene = gene_f
                child.append(gene)
            newborns.append(child)
        return newborns

    def survive(self, population):
        num_survivors = int(self.population_limit * self.survive_ratio)
        best_genes = sorted(population, key=lambda i: -i[1])[:num_survivors]
        return best_genes


def create_evaluation_function(a: int, b: int, c: int, d: int, e: int, f: int):
    def base_evaluation_function(x: list):
        z = a * x[0] + b * x[1] + c * x[2] + d * x[3] + e * x[4] + f * x[5]
        ans = 1000
        solved = "- Solved!" if z == ans else ""
        print(f"{a}*{x[0]} + {b}*{x[1]} + {c}*{x[2]} + {d}*{x[3]} + {e}*{x[4]} + {f}*{x[5]} = {z} {solved}")
        return -abs(ans - z)

    return base_evaluation_function


evaluation_function = create_evaluation_function(1, 2, 3, 4, 5, 6)

genetic_algorithm = GeneticAlgorithm(evaluation_function=evaluation_function, amount_of_genes=6, max_steps=100,
                                     population_limit=10, survive_ratio=0.25, productivity_ratio=5, stop_fitness=0)

result = genetic_algorithm.solve()
print(result)
