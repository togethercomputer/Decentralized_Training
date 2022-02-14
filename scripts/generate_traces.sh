source ./ip_list_12.sh

# Current valid prefix includes:
# gpt3_gpipe_b64_1_l2048_m768_w3_p3_d1,
# gpt3_gpipe_b64_1_l2048_m768_w12_p3_d4
# gpt3_gpipe_b64_1_l2048_m768_w48_p3_d16
# gpt3_gpipe_b64_1_l2048_m2048_w12_p12_d1
# gpt3_gpipe_b64_1_l2048_m2048_w48_p12_d4

profix=$1

postfixes=(
"tidy_profiling_default"
"tidy_profiling_d1b5"
"tidy_profiling_d5b2"
"tidy_profiling_d10b1"
)

world_size=${#ips[@]}

for postfix in "${postfixes[@]}"
do
  python ./merge_trace_file.py --world-size "$world_size" --profix "$profix" --postfix "$postfix"
done