import argparse
import time

import torch.autograd.profiler as profiler
from pipeline_parallel.dist_pp_utils import get_pp_inference_module
from utils.dist_args_utils import *
from utils.dist_inference_utils import *
from comm.comm_utils import *
from coordinator.lsf.lsf_coordinate_client import CoordinatorInferenceClient
from coordinator.global_coordinator.global_coordinator_client import GlobalCoordinatorClient


def sync_setting(args, pipeline, device, return_msg=None):
    num_return_sequences_tensor = torch.zeros(1, dtype=torch.int64, device=device)
    generate_token_length_tensor = torch.zeros(1, dtype=torch.int64, device=device)
    temperature_tensor = torch.zeros(1, dtype=torch.float32, device=device)
    top_p_tensor = torch.zeros(1, dtype=torch.float32, device=device)
    do_sample_tensor = torch.zeros(1, dtype=torch.uint8, device=device)

    if get_pipeline_parallel_rank() == 0:
        generate_token_length = return_msg['hf_api_para']['parameters']['max_new_tokens']
        do_sample = return_msg['hf_api_para']['parameters']['do_sample']
        temperature = return_msg['hf_api_para']['parameters']['temperature']
        top_p = return_msg['hf_api_para']['parameters']['top_p']
        num_return_sequences = return_msg['hf_api_para']['parameters']['num_return_sequences']
        num_return_sequences_tensor[:] = num_return_sequences
        generate_token_length_tensor[:] = generate_token_length
        temperature_tensor[:] = temperature
        top_p_tensor[:] = top_p
        do_sample_tensor[:] = do_sample

    pipeline.comm.broadcast(num_return_sequences_tensor, src=0)
    pipeline.num_completions = num_return_sequences_tensor.item()

    pipeline.comm.broadcast(generate_token_length_tensor, src=0)
    pipeline.generate_seq_length = generate_token_length_tensor.item()

    pipeline.comm.broadcast(temperature_tensor, src=0)
    args.temperature = temperature_tensor.item()

    pipeline.comm.broadcast(top_p_tensor, src=0)
    args.top_p = top_p_tensor.item()

    pipeline.comm.broadcast(do_sample_tensor, src=0)
    if do_sample_tensor.item() == 0:
        args.temperature = 0


def main():
    parser = argparse.ArgumentParser(description='Inference Runner with coordinator.')
    add_device_arguments(parser)
    add_torch_distributed_inference_w_euler_coordinator_arguments(parser)
    add_inference_arguments(parser)
    add_inference_details_arguments(parser)
    add_global_coordinator_arguments(parser)
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--profiling', type=str, default='tidy_profiling', metavar='S',
                        help='enable which profiling? default: tidy mode')
    parser.add_argument('--trace-postfix', type=str, default='default', metavar='S',
                        help='postfix of the tracing file name.')
    args = parser.parse_args()
    print_arguments(args)
    torch.manual_seed(args.seed)
    if args.use_cuda:
        assert (torch.cuda.is_available())
        device = torch.device('cuda', args.cuda_id)
    else:
        device = torch.device('cpu')

    coord_client = CoordinatorInferenceClient(args)
    prime_ip, rank, port = coord_client.notify_inference_join()
    print("<====Coordinator assigned prime-IP:", prime_ip, " and my assigned rank", rank, "====>")

    init_inference_communicators_with_coordinator(args, prime_ip, rank, port=port)

    pipeline = get_pp_inference_module(args, device, rank=rank)

    tokenizer = get_tokenizer(args)
    tokenizer.model_max_length = args.input_seq_length

    input_ids = torch.ones([args.batch_size, args.input_seq_length]).long().cuda()
    attention_mask = torch.ones([args.batch_size, args.input_seq_length]).long().cuda()

    while True:
        if get_pipeline_parallel_rank() == 0:
            global_coord_client = GlobalCoordinatorClient(args)
            return_msg = global_coord_client.get_request_cluster_coordinator()
            print("<<<<<<<<<<<<<<Return_msg Dict>>>>>>>>>>>>")
            print(return_msg)

            if return_msg is None:
                time.sleep(10)
            else:
                sync_setting(args, pipeline, device, return_msg)
                pipeline.update_processors(args)
                #####
                inputs = tokenizer(return_msg['hf_api_para']['inputs'], return_tensors='pt',
                                   padding='max_length', truncation=True, )

                input_ids = inputs['input_ids'].long().to(device)
                attention_mask = inputs['attention_mask'].long().to(device)

                pipeline.comm.broadcast(input_ids, src=0)
                pipeline.comm.broadcast(attention_mask, src=0)

                output_ids_list = []
                pipeline.inference_batch(input_ids, output_ids_list, attention_mask=attention_mask)
                return_full_text = return_msg['hf_api_para']['parameters']['return_full_text']

                results = []
                for i in range(pipeline.num_completions):
                    token_len = torch.zeros([1], dtype=torch.int64).cuda()
                    pipeline.comm.recv(token_len, src=pipeline.pipeline_group_size - 1)
                    result = torch.empty((1, token_len.item()), dtype=torch.long).cuda()
                    pipeline.comm.recv(result, src=pipeline.pipeline_group_size - 1)
                    if return_full_text:
                        results.append(return_msg['hf_api_para']['parameters']['inputs'] + tokenizer.decode(result[0]))
                    else:
                        results.append(tokenizer.decode(result[0]))
                global_coord_client.put_request_cluster_coordinator(return_msg, results)

        elif get_pipeline_parallel_rank() == pipeline.pipeline_group_size - 1:
            while True:
                sync_setting(args, pipeline, device)
                pipeline.update_processors(args)

                pipeline.comm.broadcast(input_ids, src=0)
                pipeline.comm.broadcast(attention_mask, src=0)

                output_ids_list = []
                pipeline.inference_batch(input_ids, output_ids_list, attention_mask=attention_mask)

                for i in range(pipeline.num_completions):
                    result = output_ids_list[i]
                    token_len = torch.tensor(result['token_ids'].size(1), dtype=torch.long).cuda()
                    pipeline.comm.send(token_len, dst=0)
                    pipeline.comm.send(result['token_ids'].cuda(), dst=0)
                # s.send((json.dumps(output_ids_list)).encode())
        else:
            while True:
                sync_setting(args, pipeline, device)
                pipeline.update_processors(args)
                pipeline.comm.broadcast(input_ids, src=0)
                pipeline.comm.broadcast(attention_mask, src=0)
                pipeline.inference_batch(input_ids, attention_mask=attention_mask)


if __name__ == '__main__':
    main()
