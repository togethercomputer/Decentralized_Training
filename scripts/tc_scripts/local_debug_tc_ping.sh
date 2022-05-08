# Update this list before use.
private_ips=(
"172.31.36.100"
"172.31.39.103"
"172.31.35.99"
"172.31.41.104"
"172.31.43.105"
"172.31.45.103"
"172.31.32.232"
"172.31.36.116"
"172.31.38.118"
"172.31.38.235"
"172.31.43.112"
"172.31.47.122"
"172.31.47.123"
"172.31.45.119"
"172.31.39.248"
"172.31.32.67"
"172.31.37.68"
"172.31.47.124"
"172.31.35.255"
"172.31.37.78"
"172.31.44.80"
"172.31.39.203"
"172.31.34.204"
"172.31.47.214"
"172.31.43.87"
"172.31.47.85"
"172.31.35.214"
"172.31.37.90"
"172.31.32.220"
"172.31.39.215"
"172.31.38.88"
"172.31.37.32"
"172.31.38.164"
"172.31.33.220"
"172.31.45.222"
"172.31.38.40"
"172.31.46.40"
"172.31.35.168"
"172.31.43.40"
"172.31.41.173"
"172.31.38.47"
"172.31.33.171"
"172.31.45.43"
"172.31.42.57"
"172.31.33.60"
"172.31.41.50"
"172.31.37.55"
"172.31.36.191"
"172.31.47.130"
"172.31.47.188"
"172.31.42.189"
"172.31.47.139"
"172.31.40.11"
"172.31.43.3"
"172.31.44.6"
"172.31.32.151"
"172.31.38.23"
"172.31.46.139"
"172.31.32.141"
"172.31.44.154"
"172.31.33.157"
"172.31.37.153"
"172.31.41.154"
"172.31.46.30"
)


for ip in "${private_ips[@]}"
do
  ping -c 5 $ip
done
