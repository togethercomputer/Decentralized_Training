deepspeed --hostfile='./ZeRO_benchmark/hostfile' --master_addr 172.31.33.164 --master_port=8000 dist_zero_dp.py --num-layers 12 --embedding-dim 768 --deepspeed --deepspeed_config './ZeRO_benchmark/zero_dp_s3_config.json'
NCCL_SOCKET_IFNAME=ens3  deepspeed --hostfile='./ZeRO_benchmark/hostfile' --master_addr='172.31.35.33' --num_nodes=2 --master_port=8000 dist_zero_dp.py --num-layers 12 --embedding-dim 768 --deepspeed --deepspeed_config './ZeRO_benchmark/zero_dp_s3_config.json'
NCCL_SOCKET_IFNAME=ens3  deepspeed --hostfile='./ZeRO_benchmark/hostfile' --master_addr='172.31.35.33' --num_nodes=2 --num_gpus=1 --master_port=8000 dist_zero_dp.py --num-layers 12 --embedding-dim 768 --deepspeed --deepspeed_config './ZeRO_benchmark/zero_dp_s3_config.json'