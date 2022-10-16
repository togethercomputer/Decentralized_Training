from .dist_dp_allreduce import AllReduceDP
from .dist_dp_central_ps import CentralPSDP
from .dist_dp_sharded_ps import ShardedPSDP
from .dist_dp_sharded_ps_compressed import ShardedPSDPCompressed
from .dist_dp_local import LocalDP
from .dist_dp_admm import ADMMDP
from .dist_dp_proxskip import ProxSkipDP
from .dist_dp_proxskip_adam import ProxSkipAdamDP


def get_dp_module(args, device, module, optimizer):
    print("Data parallel implementation: ", args.dp_mode)
    if args.dp_mode == 'allreduce':
        return AllReduceDP(args, device, module, optimizer, flatten=False)
    elif args.dp_mode == 'central_ps':
        return CentralPSDP(args, device, module, optimizer)
    elif args.dp_mode == 'sharded_ps':
        return ShardedPSDP(args, device, module, optimizer)
    elif args.dp_mode == 'sharded_ps_compressed':
        return ShardedPSDPCompressed(args, device, module, optimizer)
    elif args.dp_mode == 'local':
        return LocalDP(args, device, module, optimizer)
    elif args.dp_mode == 'admm':
        return ADMMDP(args, device, module, optimizer)
    elif args.dp_mode == 'proxskip':
        return ProxSkipDP(args, device, module, optimizer)
    elif args.dp_mode == 'proxskip_adam':
        return ProxSkipAdamDP(args, device, module, optimizer)
    else:
        print("Not recognize this data parallel mode.")
        assert False
