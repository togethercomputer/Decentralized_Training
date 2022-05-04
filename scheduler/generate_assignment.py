import numpy as np


def random_assignment_0_datacenter(nodes=64):
    print("Generate random_assignment_0_datacenter")
    np.random.seed(2022)
    gpu_per_instances = min(nodes // 2, 8)
    instances = nodes // gpu_per_instances
    arr = np.arange(1, nodes)
    np.random.shuffle(arr)
    result = arr.tolist()
    result.insert(0, 0)
    print('nodes_per_node=(', end='')
    for i in range(instances):
        print(gpu_per_instances, end='' if i==instances-1 else ' ')
    print(')')
    print('rank_map=(', end='')
    for i in range(len(result)):
        val = result[i]
        print(val, end='' if i==nodes-1 else ' ')
    print(')')


def random_assignment_1_datacenter_spot(gpu_per_instances=4, multi_gpu_instances=8, single_gpu_instances=32):
    print("Generate random_assignment_1_datacenter_spot")
    np.random.seed(2022)
    gpus = []
    for i in range(multi_gpu_instances):
        for j in range(single_gpu_instances // multi_gpu_instances):
            gpus.append(1)
        gpus.append(gpu_per_instances)
    print('nodes_per_node=(', end='')
    instances = multi_gpu_instances + single_gpu_instances
    for i in range(instances):
        print(gpus[i], end='' if i == instances - 1 else ' ')
    print(')')
    world_size = gpu_per_instances*multi_gpu_instances+single_gpu_instances
    arr = np.arange(1, world_size)
    np.random.shuffle(arr)
    result = arr.tolist()
    result.insert(0, 0)
    print('rank_map=(', end='')
    for i in range(len(result)):
        val = result[i]
        print(val, end='' if i==world_size-1 else ' ')
    print(')')


def optimal_assignment_1_datacenter_spot(gpu_per_instances=4, multi_gpu_instances=8, single_gpu_instances=32):
    print("Generate optimal_assignment_1_datacenter_spot")

    gpus = []
    for i in range(multi_gpu_instances):
        for j in range(single_gpu_instances//multi_gpu_instances):
            gpus.append(1)
        gpus.append(gpu_per_instances)
    print('nodes_per_node=(', end='')
    instances = multi_gpu_instances+single_gpu_instances
    for i in range(instances):
        print(gpus[i], end='' if i==instances-1 else ' ')
    print(')')
    world_size = gpu_per_instances*multi_gpu_instances+single_gpu_instances
    arr = np.arange(world_size)
    result = arr.tolist()
    print('rank_map=(', end='')
    for i in range(len(result)):
        val = result[i]
        print(val, end='' if i==world_size-1 else ' ')
    print(')')

def main():
    print("------------------------------------")
    random_assignment_0_datacenter()
    print("------------------------------------")
    random_assignment_1_datacenter_spot()
    print("------------------------------------")
    optimal_assignment_1_datacenter_spot()


if __name__ == '__main__':
    main()
