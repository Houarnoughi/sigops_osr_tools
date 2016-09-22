#!/bin/bash
if [ $# -lt 1 ]; then
  echo 'Usage: $0 <command> [vm]'
  echo 'command : '
  echo '          list: list of all virtual machines'
  echo '          run <vm_name>: run a virtual machine (followed by a virtual machine name)'
  echo '          stop <vm_name>: stop a virtual machine (followed by a virtual machine name)'
  exit 1
fi
ARGS=$#
COMMAND=$1
VM=$2

vm_list()
{
  echo 'The list of virtual machines in the domain'
  sudo virsh -c qemu:///system list --all
}

vm_run()
{
 if [ $ARGS -lt 2 ]; then
	echo 'ERROR: virtual machine name missing'
	exit 1
  fi
  
  if [ $VM = all ];
  then
  
        echo 'Run all virtual machines'
        VAR=$(sudo virsh -c qemu:///system list --all | grep vm | awk '{print $2}')
        
        for i in $VAR;
        do
                echo $i
                sudo virsh -c qemu:///system start $i
        done
  else
  
        echo 'Run virtual machine ' $VM
        sudo virsh -c qemu:///system start $VM
  fi

}

vm_stop()
{
  if [ $ARGS -lt 2 ]; then
	echo 'ERROR: virtual machine name missing'
	exit 1
  fi
  
  if [ $VM = 'all' ];then
  
        sudo echo 'Stop all virtual machines'
        VAR=$(sudo virsh -c qemu:///system list --all | grep vm | awk '{print $2}')
        
        for i in $VAR;
        do
                echo $i
                sudo virsh -c qemu:///system shutdown $i
        done
  else
  
        echo 'Stop virtual machine ' $VM
        sudo virsh -c qemu:///system shutdown $VM
  fi
}


case $COMMAND in
  'list') vm_list;;
  'run') vm_run &;;
  'stop') vm_stop;;
  *) echo 'Error: command not found';;
esac
