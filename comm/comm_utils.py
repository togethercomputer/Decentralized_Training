from .torch_backend import *
from .nccl_backend import *

_DATA_PARALLEL_COMM = None
_DATA_PARALLEL_RANK = None
_DATA_PARALLEL_WORLD_SIZE = None

_PIPELINE_PARALLEL_COMM = None
_PIPELINE_PARALLEL_RANK = None
_PIPELINE_PARALLEL_WORLD_SIZE = None

_TENSOR_PARALLEL_COMM = None
_TENSOR_PARALLEL_RANK = None
_TENSOR_PARALLEL_WORLD_SIZE = None


def get_data_parallel_comm() -> NCCLCommunicator:
    assert _DATA_PARALLEL_COMM is not None
    return _DATA_PARALLEL_COMM


def get_data_parallel_rank() -> int:
    assert _DATA_PARALLEL_RANK is not None
    return _DATA_PARALLEL_RANK


def get_data_parallel_world_size() -> int:
    assert _DATA_PARALLEL_WORLD_SIZE is not None
    return _DATA_PARALLEL_WORLD_SIZE


def get_pipeline_parallel_comm() -> NCCLCommunicator:
    assert _PIPELINE_PARALLEL_COMM is not None
    return _PIPELINE_PARALLEL_COMM


def get_pipeline_parallel_rank() -> int:
    assert _PIPELINE_PARALLEL_RANK is not None
    return _PIPELINE_PARALLEL_RANK


def get_pipeline_parallel_world_size() -> int:
    assert _PIPELINE_PARALLEL_WORLD_SIZE is not None
    return _PIPELINE_PARALLEL_WORLD_SIZE


def get_megatron_tensor_parallel_comm() -> NCCLCommunicator:
    assert _TENSOR_PARALLEL_COMM is not None
    return _TENSOR_PARALLEL_COMM


def get_megatron_tensor_parallel_rank() -> int:
    assert _TENSOR_PARALLEL_RANK is not None
    return _TENSOR_PARALLEL_RANK


def get_megatron_tensor_parallel_world_size() -> int:
    assert _TENSOR_PARALLEL_WORLD_SIZE is not None
    return _TENSOR_PARALLEL_WORLD_SIZE


def init_communicators(args):
    default_init(args)
    assert args.world_size == args.data_group_size * args.pipeline_group_size
    if args.world_size == args.data_group_size * args.pipeline_group_size:
        #    We do the following hard code alignment of communication groups:
        #    Suppose there are 8 instances (world_size), and 4 data parallel groups (data_group_size is 2),
        #    Then there would be 2 pipeline parallel groups (pipeline_group_size is 4), then the groups will look like:
        #    pipeline parallel: <group 0: [0,1,2,3]>, <group 1: [4,5,6,7]>
        #    data parallel: <group 0: [0,4]>, <group 1: [1,5]>, <group 2: [2,6]>, <group 3: [3,7]>
        # assert args.world_size == args.data_group_size * args.pipeline_group_size
        global _DATA_PARALLEL_COMM
        global _PIPELINE_PARALLEL_COMM
        global _DATA_PARALLEL_RANK
        global _PIPELINE_PARALLEL_RANK
        global _DATA_PARALLEL_WORLD_SIZE
        global _PIPELINE_PARALLEL_WORLD_SIZE
        # We use pipeline parallel by default.
        _PIPELINE_PARALLEL_WORLD_SIZE = args.pipeline_group_size
        _PIPELINE_PARALLEL_RANK = args.rank % args.pipeline_group_size
        _PIPELINE_PARALLEL_COMM = NCCLCommunicator(_PIPELINE_PARALLEL_RANK, args.cuda_id, args.pipeline_group_size,
                                                   "pipeline_group_"+str(args.rank // args.pipeline_group_size))
        if args.data_group_size != 1:
            _DATA_PARALLEL_WORLD_SIZE = args.data_group_size
            _DATA_PARALLEL_RANK = args.rank // args.pipeline_group_size
            _DATA_PARALLEL_COMM = NCCLCommunicator(_DATA_PARALLEL_RANK, args.cuda_id, args.data_group_size,
                                                   "data_group_"+str(args.rank % args.pipeline_group_size))
            
            # for i in range(args.pipeline_group_size):
            #     ranks = [rank for rank in range(i, args.world_size, args.pipeline_group_size)]
            #     print(args.rank, ranks)
            #     data_group = torch.distributed.new_group(ranks, backend='gloo')
            #     if args.rank in ranks:
            #         def to_global_rank(dp_rank):
            #             rank = _PIPELINE_PARALLEL_RANK + dp_rank * args.pipeline_group_size
            #             # print(f"{dp_rank} --> {rank}")
            #             return rank
            #         _DATA_PARALLEL_COMM = TorchCommunicator(data_group, to_global_rank=to_global_rank)
            
        print('comm init done!!')
            
    # elif args.world_size == args.data_group_size * args.tensor_group_size:
    #    global _DATA_PARALLEL_COMM
    #    global _TENSOR_PARALLEL_COMM
    #    global _DATA_PARALLEL_RANK
    #    global _TENSOR_PARALLEL_RANK
    #    global _DATA_PARALLEL_WORLD_SIZE
    #    global _TENSOR_PARALLEL_WORLD_SIZE
        # We use megatron tensor parallel by default.
    #    _TENSOR_PARALLEL_WORLD_SIZE = args.tensor_group_size
    #    _TENSOR_PARALLEL_RANK = args.rank % args.tensor_group_size
    #    _TENSOR_PARALLEL_COMM = NCCLCommunicator(_TENSOR_PARALLEL_RANK, args.cuda_id, args.tensor_group_size,
    #                                             "tensor_group_" + str(args.rank // args.tensor_group_size))
    #    if args.data_group_size != 1:
    #        _DATA_PARALLEL_WORLD_SIZE = args.data_group_size
    #        _DATA_PARALLEL_RANK = args.rank // args.tensor_group_size
    #        _DATA_PARALLEL_COMM = NCCLCommunicator(_DATA_PARALLEL_RANK, args.cuda_id, args.data_group_size,
    #                                              "data_group_" + str(args.rank % args.tensor_group_size))
    else:
        print("Not supported yet")
        assert False
