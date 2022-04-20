import numpy as np
import random
import itertools
import config


# GPT-3 XL
batch_size = 0.5e6
layer_size = 24
para_size = 1.3e9

# physical topology
num_devices = config.nodes
peer_delay = None
peer_bandwidth = None

# assigned task
batch_size_per_task = 0.25e6
layer_size_per_task = 6
send_activation_size = 4  # gigabytes
send_gradient_size = 1  # gigabytes


def normalization(parent1=None, parent2=None, partition_size=None):
    parent1_str = [0] * num_devices
    parent2_str = [0] * num_devices
    for i in range(num_devices):
        parent1_str[parent1[i]] = i // partition_size
        parent2_str[parent2[i]] = i // partition_size

    way = int(num_devices / partition_size)
    count = np.zeros(shape=(way, way))
    for i in range(num_devices):
        count[parent1_str[i], parent2_str[i]] += 1

    map = [0] * way
    for i in range(way):
        max_idx = np.argmax(count)
        p = max_idx // way
        q = max_idx - p * way
        for j in range(way):
            count[p][j] = float('-inf')
            count[j][q] = float('-inf')
        map[q] = p

    for i in range(num_devices):
        parent2_str[i] = map[parent2_str[i]]

    return parent1_str, parent2_str


def five_point_crossover(parent1_str=None, parent2_str=None, partition_size=None):
    points = list(range(num_devices))
    random.shuffle(points)
    points = points[:5]

    for point in points:
        parent2_str[point] = parent1_str[point]

    way = int(num_devices / partition_size)
    unbalanced_offspring = [[] for _ in range(way)]
    for i in range(num_devices):
        unbalanced_offspring[parent2_str[i]].append(i)

    offspring = list(itertools.chain.from_iterable(unbalanced_offspring))
    return offspring


def GCMA(nodes=None, partition_size=None, population_size=None, trails=None):
    # https://dl.acm.org/doi/10.5555/2933718.2933740
    candidate_partitions = []
    for i in range(population_size):
        cur_nodes = nodes.copy()
        random.seed = i
        random.shuffle(cur_nodes)
        candidate_partitions.append(cur_nodes)
    for i in range(trails):
        np.random.seed = i
        parent1_idx, parent2_idx = np.random.randint(population_size, size=2)
        parent1_str, parent2_str = normalization(
            candidate_partitions[parent1_idx], candidate_partitions[parent2_idx], partition_size)
        offspring = five_point_crossover(
            parent1_str, parent2_str, partition_size)
    return candidate_partitions


def all_candidate_partitions(nodes=None, partition_size=None):
    candidate_partitions = []
    if len(nodes) == partition_size:
        candidate_partitions.append([tuple(nodes)])
    else:
        for cur_partition in itertools.combinations(nodes, partition_size):
            rest_nodes = nodes.copy()
            for node in cur_partition:
                rest_nodes.remove(node)

            rest_partitions = all_candidate_partitions(
                rest_nodes, partition_size)
            for rest_partition in rest_partitions:
                candidate_partitions.append([cur_partition])
                candidate_partitions[-1].extend(rest_partition)
    return candidate_partitions


def compute_data_parallel_cost(candidate_partition=None):
    data_parallel_cost = 0
    for partition in candidate_partition:
        within_partition_cost = float('inf')
        for primary in partition:
            cur_cost = 0
            for secondary in partition:
                if primary != secondary:
                    cur_cost += peer_delay[primary, secondary] / 1e3 + \
                        send_activation_size * 8 / \
                        peer_bandwidth[primary, secondary]
            if cur_cost < within_partition_cost:
                within_partition_cost = cur_cost
        data_parallel_cost += within_partition_cost
    return data_parallel_cost


class open_loop_tsp:
    # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5388488
    def __init__(self, cost_matrix, start_node):
        self.cost_matrix = cost_matrix
        self.num_nodes = self.cost_matrix.shape[0]
        self.start_node = start_node
        self.dp_table = np.full(
            shape=(self.num_nodes, pow(2, self.num_nodes)), fill_value=np.inf)
        self.trace_table = np.zeros(
            shape=(self.num_nodes, pow(2, self.num_nodes)))

    def convert(self, future_nodes):
        binary_future_nodes = 0
        for future_node in future_nodes:
            binary_future_nodes += pow(2, future_node)
        return binary_future_nodes

    def solve(self, node, future_nodes):
        if len(future_nodes) == 0:
            # closed loop tsp problem: return self.cost_matrix[node][self.start_node]
            # open loop tsp problem: return 0
            return 0

        all_distance = []
        for next_node in future_nodes:
            next_future_nodes = future_nodes.copy()
            next_future_nodes.remove(next_node)
            binary_next_future_nodes = self.convert(next_future_nodes)
            if self.dp_table[next_node][binary_next_future_nodes] == np.inf:
                all_distance.append(
                    self.cost_matrix[node][next_node] + self.solve(next_node, next_future_nodes))
            else:
                all_distance.append(
                    self.cost_matrix[node][next_node] + self.dp_table[next_node][binary_next_future_nodes])

        min_distance = min(all_distance)
        next_node = future_nodes[all_distance.index(min_distance)]

        binary_future_nodes = self.convert(future_nodes)
        self.dp_table[node][binary_future_nodes] = min_distance
        self.trace_table[node][binary_future_nodes] = next_node
        return min_distance

    def get_least_cost_route(self):
        future_nodes = list(range(self.num_nodes))
        future_nodes.remove(self.start_node)
        cost = self.solve(self.start_node, future_nodes)

        path = [self.start_node]
        cur_node = self.start_node
        while len(future_nodes) > 0:
            binary_future_nodes = self.convert(future_nodes)
            cur_node = int(self.trace_table[cur_node][binary_future_nodes])
            future_nodes.remove(cur_node)
            path.append(cur_node)
        return cost, path


def compute_pipeline_parallel_cost(candidate_partition=None):
    way = len(candidate_partition)

    # bipartite matching
    crose_partition_cost = np.zeros(shape=(way, way))
    for i in range(way):
        for j in range(i+1, way):
            bipartite_matches = []
            for x in itertools.permutations(candidate_partition[i]):
                bipartite_matches.append(list(zip(x, candidate_partition[j])))
            all_transfer_times = []
            for bipartite_match in bipartite_matches:
                cur_transfer_times = []
                for pair in bipartite_match:
                    cur_transfer_times.append(
                        peer_delay[pair[0], pair[1]]/1e3 + send_gradient_size * 8 / peer_bandwidth[pair[0], pair[1]])
                all_transfer_times.append(max(cur_transfer_times))
            crose_partition_cost[i, j] = min(all_transfer_times)
    crose_partition_cost = crose_partition_cost + crose_partition_cost.T

    pipeline_parallel_cost = []
    pipeline_parallel_path = []
    for start_node in range(way):
        tsp = open_loop_tsp(crose_partition_cost, start_node)
        cost, path = tsp.get_least_cost_route()
        pipeline_parallel_cost.append(cost)
        pipeline_parallel_path.append(path)
    dp_pipeline_parallel_cost = min(pipeline_parallel_cost)
    dp_pipeline_parallel_path = pipeline_parallel_path[pipeline_parallel_cost.index(
        dp_pipeline_parallel_cost)]

    # pipeline_parallel_cost = float('inf')
    # pipeline_parallel_path = None
    # for path in itertools.permutations(range(way)):
    #    cur_cost = 0
    #    for i in range(way - 1):
    #        cur_cost += crose_partition_cost[path[i], path[i+1]]
    #    if cur_cost < pipeline_parallel_cost:
    #        pipeline_parallel_cost = cur_cost
    #        pipeline_parallel_path = path
    # assert(dp_pipeline_parallel_cost == pipeline_parallel_cost)

    return dp_pipeline_parallel_cost, dp_pipeline_parallel_path


if __name__ == "__main__":
    assert(batch_size % batch_size_per_task == 0)
    assert(layer_size % layer_size_per_task == 0)
    assert(num_devices == batch_size * layer_size /
           (batch_size_per_task * layer_size_per_task))
    GCMA(nodes=list(range(num_devices)),
         partition_size=2, population_size=50, trails=100)
    exit()

    simulate_cases = [config.simulate_0_datacenter, config.simulate_1_datacenter_spot_gpu, config.simulate_2_multi_universities,
                      config.simulate_3_regional_geo_distributed, config.simulate_4_worldwide_geo_distributed]
    import time
    for simulate_case in simulate_cases:
        peer_delay, peer_bandwidth = simulate_case()
        start = time.perf_counter()
        min_total_cost = float('inf')
        candidate_partition = None
        data_parallel_cost = None
        pipeline_parallel_cost = None
        pipeline_parallel_path = None
        all_cost_records = []
        for cur_candidate_partition in all_candidate_partitions(list(range(num_devices)),
                                                                int(batch_size / batch_size_per_task)):
            cur_data_parallel_cost = compute_data_parallel_cost(
                candidate_partition=cur_candidate_partition)
            cur_pipeline_parallel_cost, cur_pipeline_parallel_path = compute_pipeline_parallel_cost(
                cur_candidate_partition)
            cur_total_cost = cur_data_parallel_cost + cur_pipeline_parallel_cost
            all_cost_records.append(cur_total_cost)
            if min_total_cost >= cur_total_cost:
                min_total_cost = cur_total_cost
                candidate_partition = cur_candidate_partition
                pipeline_parallel_path = cur_pipeline_parallel_path
                data_parallel_cost = cur_data_parallel_cost
                pipeline_parallel_cost = cur_pipeline_parallel_cost
        end = time.perf_counter()
        print("run time(" + str(len(all_cost_records)) +
              " candidates): " + str(end - start) + " seconds")
        print("candidate partition: " + str(candidate_partition))
        print("pipeline parallel path: " + str(pipeline_parallel_path))
        print("total cost: " + str(data_parallel_cost + pipeline_parallel_cost))
        print("data parallel cost: " + str(data_parallel_cost))
        print("pipeline parallel cost: " + str(pipeline_parallel_cost))
