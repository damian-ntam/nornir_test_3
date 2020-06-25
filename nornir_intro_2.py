from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command

commands = ["show arp", "show ip interface brief"]

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)
for command in commands:
    results = nr.run(
        task=netmiko_send_command, command_string = command
    )
    print_title(command)
    print_result(results)