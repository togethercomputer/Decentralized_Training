# file=../lm-eval-harness-adapter/winogrande.jsonl
# file=../lm-eval-harness-adapter/openbookqa.jsonl
# file=../lm-eval-harness-adapter/rte.jsonl
#file=../lm-eval-harness-adapter/piqa.jsonl
# file=../lm-eval-harness-adapter/copa.jsonl
# file=../lm-eval-harness-adapter/hellaswag.jsonl
#file=../lm-eval-harness-adapter/lambada_openai.jsonl
#file=../lm-eval-harness-adapter/wic.jsonl
#file=../lm-eval-harness-adapter/wsc.jsonl
# file=../lm-eval-harness-adapter/cb.jsonl
file=../lm-eval-harness-adapter/record.jsonl
echo "start running ${file}"

ARGS="--model-name /mnt/workspace/checkpoint/opt-175b-new \
--model-type opt-baseline \
--seed 42 \
--fp16 \
--num-layers 16 \
--max-layers 96 \
--budget 10800 \
--num-iters 100000000 \
--dist-url tcp://127.0.0.1:9031 \
--token-micro-batch-size 2 \
--world-size 6 --pipeline-group-size 6 --data-group-size 1 \
--pp-mode pipe_sync_sample_mask_token_pipe \
--infer-data ${file}"

(trap 'kill 0' SIGINT; \
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 6 --rank 0 \
    &
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 1 --rank 1 \
    &
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 2 --rank 2 \
    &
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 3 --rank 3 \
    &
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 4 --rank 4 \
    &
python dist_inference_runner.py $(echo ${ARGS}) --cuda-id 5 --rank 5 \
    & \
wait)
