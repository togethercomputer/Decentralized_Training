import socket
import argparse
from collections import OrderedDict
import os
import json
import time


crusoe_node_types = {'a40.1x', 'a40.2x', 'a40.4x', 'a40.8x',
                     'a100.1x', 'a100.2x', 'a100.4x', 'a100.8x',
                     'a100-80gb.1x', 'a100-80gb.2x', 'a100-80gb.4x', 'a100-80gb.8x'}


class CrusoeCoordinatorServer:
    def __init__(self, args):
        self.host = args.coordinator_server_ip
        self.port = args.coordinator_server_port
        self.token = args.token
        self.meta_key_value_store = OrderedDict()
        # An array of dict object to store worker info
        self.node_info = {}

    def _handle_launch_new_vm(self, msg_dict):
        node_type = msg_dict['node_type']
        assert node_type in crusoe_node_types
        name = 'together_vm' + str(len(self.node_info))
        output = os.popen(f'bash ./crusoe_scripts/launch_crusoe_vm.sh {name} {node_type}').read()
        json_start = output.find('{')
        json_end = output.rfind("}")
        meta_dict = json.loads(output[json_start: json_end+1])
        ip_end = meta_dict['ssh_destination'].find(':22')
        assign_ip = meta_dict['ssh_destination'][0: ip_end]
        self.node_info[assign_ip] = {'name': meta_dict['name'],
                                     'crusoe_id': meta_dict['id'],
                                     'created_time': meta_dict['created_at'],
                                     'state': 'initialized'}
        print(f"Install cuda and pip lib in <{assign_ip}>")
        time.sleep(10)
        os.popen(f'ssh-keyscan -H {assign_ip} >> ~/.ssh/known_hosts')
        os.popen(f'ssh root@{assign_ip} bash -s < ./crusoe_scripts/startup_install.sh {self.token} &> ./exe_log/{assign_ip}_install.log &')
        return f"Succeed! Launched node <{assign_ip}>"

    def _handle_recv_message_vm(self, ip, msg_dict):
        print(msg_dict['message'])
        if msg_dict['message'] == 'Install CUDA: done.':
            assert ip in self.node_info
            self.node_info[ip]['state'] = 'cuda_ready'
        elif msg_dict['message'] == 'Install Python Libs: done.':
            assert ip in self.node_info
            self.node_info[ip]['state'] = 'pip_ready'
        return "Get it!"

    def _handle_check_node_status(self):
        return json.dumps(self.node_info)

    def execute_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                connection, address = s.accept()
                with connection:
                    ip, port = address
                    msg_raw = connection.recv(1024)
                    msg_dict = json.loads(msg_raw)
                    print(f"====<Ip:{ip}> op: {msg_dict['op']}====")
                    print(msg_dict)
                    print("----------------------------------------")
                    if msg_dict['op'] == 'send_message_vm':
                        return_msg = self._handle_recv_message_vm(ip, msg_dict)
                    elif msg_dict['op'] == 'launch_vm_user':
                        return_msg = self._handle_launch_new_vm(msg_dict)
                    elif msg_dict['op'] == 'check_node_status_user':
                        return_msg = self._handle_check_node_status()
                    else:
                        assert False, "Not recognized op"
                    connection.sendall(return_msg.encode())
                    connection.close()


def main():
    parser = argparse.ArgumentParser(description='Test Coordinator-Server')
    parser.add_argument('--coordinator-server-port', type=int, default=9002, metavar='N',
                        help='The port of coordinator-server.')
    parser.add_argument('--coordinator-server-ip', type=str, default='0.0.0.0', metavar='S',
                        help='The IP of coordinator-server.')
    parser.add_argument('--token', type=str, default='-', metavar='S',
                        help='The token to of this repo to pull code.')
    args = parser.parse_args()
    print("====Crusoe coordinator starts!====")
    print(vars(args))
    coordinator = CrusoeCoordinatorServer(args)
    coordinator.execute_server()


if __name__ == '__main__':
    main()
