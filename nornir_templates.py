from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.tasks.networking import napalm_get, netmiko_send_command, netmiko_send_config
from nornir.plugins.functions.text import print_title, print_result
from nornir.core.filter import F

def scp_enable(lb_task):
    commands = ['aaa authorization exec default local none', 'ip scp server enable']
    lb_task.run(task = netmiko_send_config, config_commands = commands)

def eigrp_config(eigrp_task):
    # Transform inventory data to configuration via a template file
    r = eigrp_task.run(task=text.template_file,
                 name="EIGRP Configuration",
                 template="eigrp.j2",
                 path=f"templates/{eigrp_task.host['vendor']}")

    # Save the compiled configuration into a host variable
    eigrp_task.host["config"] = r.result

    # Deploy that configuration to the device using NAPALM
    eigrp_task.run(task=networking.napalm_configure,
             name="Loading Configuration on the device",
             replace=False,
             configuration=eigrp_task.host["config"])


def main():
    nr = InitNornir(config_file='config.yaml' , dry_run=True )
    cisco_host = nr.filter(F(groups__contains='ios_switches') |
                        F(groups__contains='ios_routers'))
    scp_config = cisco_host.run(task = scp_enable )
    print_result(scp_config)
    cisco_host.data.dry_run = False
    results = cisco_host.run(task=eigrp_config)
    print_result(results)

if __name__ == '__main__':
    main()