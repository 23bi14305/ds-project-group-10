from mpi4py import MPI
import os
import sys
import select
from time import sleep
import numpy as np
import socket
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def find_name_by_rank(list,num):
    for item in list:
        if item['rank'] == num:
            return item['name']
        else: 
            continue
    return "unidentified"

def ensure_fifo(path):
    """Create the FIFO if it does not exist."""
    if not os.path.exists(path):
        print(f"[INFO] Creating FIFO: {path}")
        os.mkfifo(path)

def setup_fifos(path1,path2):
    """Ensure both FIFOs exist."""
    ensure_fifo(path1)
    ensure_fifo(path2)
    


if rank == 0:
    size = comm.Get_size()
    rankls = []
    while True:
        for i in range (1,size):
            req = comm.Iprobe(source=i, tag=MPI.ANY_TAG)
            if req == True:
                data = comm.recv(source=i)
                #print(data)
                rankls.append(data)
                #print(rankls)
                for client in range (1,size):
                    comm.isend(rankls,dest=client)
            else:
                sleep(0.01)
if rank == 1:
    info = comm.Get_rank()
    name = "ruby"
    data = {'rank': info, 'name': name}
    comm.isend(data,dest=0)
    size = comm.Get_size()
    usrls = []
    # for enviroment test only
    READ_FIFO = "/tmp/fifo_b_to_a1"
    WRITE_FIFO = "/tmp/fifo_a_to_b1"
    # the pipe path is for the enviroment test only
    setup_fifos(READ_FIFO,WRITE_FIFO)
    read_fd = os.open(READ_FIFO, os.O_RDONLY | os.O_NONBLOCK)
    while True:
        try:
            write_fd = os.open(WRITE_FIFO, os.O_WRONLY | os.O_NONBLOCK)
            break
        except OSError:
            print("[INFO] Waiting for the other side to connect...")
            import time
            time.sleep(0.5)

    while True:
        for i in range (0,size):
            req = comm.Iprobe(source=i, tag=MPI.ANY_TAG)
            if req == True:
                if i == 0:
                    data = comm.recv(source=i)
                    usrls = data
                    print(data)
                else: 
                    data = comm.recv(source=i)
                    name = find_name_by_rank(usrls,i)
                    msg = f"{name}: {data}"
                    os.write(write_fd, msg.encode() + b"\n")
            else:
                sleep(0.01)
        readable, _, _ = select.select([read_fd, sys.stdin], [], [])

        # Incoming message
        if read_fd in readable:
            data = os.read(read_fd, 4096)
            if data:
                data = data.decode().strip()
                for client in usrls:
                    rank = client['rank']
                    comm.isend(data,dest=rank)
            else:
                print("[INFO] Other side closed the pipe.")
                break
if rank == 2:
    info = comm.Get_rank()
    name = "amethyst"
    data = {'rank': info, 'name': name}
    comm.isend(data,dest=0)
    size = comm.Get_size()
    usrls = []
    # for enviroment test only
    READ_FIFO = "/tmp/fifo_b_to_a2" 
    WRITE_FIFO = "/tmp/fifo_a_to_b2"
    # the pipe path is for the enviroment test only
    setup_fifos(READ_FIFO,WRITE_FIFO)
    read_fd = os.open(READ_FIFO, os.O_RDONLY | os.O_NONBLOCK)
    while True:
        try:
            write_fd = os.open(WRITE_FIFO, os.O_WRONLY | os.O_NONBLOCK)
            break
        except OSError:
            print("[INFO] Waiting for the other side to connect...")
            import time
            time.sleep(0.5)

    while True:
        for i in range (0,size):
            req = comm.Iprobe(source=i, tag=MPI.ANY_TAG)
            if req == True:
                if i == 0:
                    data = comm.recv(source=i)
                    usrls = data
                    print(data)
                else: 
                    data = comm.recv(source=i)
                    name = find_name_by_rank(usrls,i)
                    msg = f"{name}: {data}"
                    os.write(write_fd, msg.encode() + b"\n")
            else:
                sleep(0.01)
        readable, _, _ = select.select([read_fd, sys.stdin], [], [])

        # Incoming message
        if read_fd in readable:
            data = os.read(read_fd, 4096)
            if data:
                data = data.decode().strip()
                for client in usrls:
                    rank = client['rank']
                    comm.isend(data,dest=rank)
            else:
                print("[INFO] Other side closed the pipe.")
                break
if rank == 3:
    sleep(5)
    info = comm.Get_rank()
    name = "amethyst"
    data = {'rank': info, 'name': name}
    comm.isend(data,dest=0)
    sleep(3)
    msg = "hi"
    comm.isend(msg,dest=1)

    """
while True:
        for i in range (0,size):
            req = comm.Iprobe(source=i, tag=MPI.ANY_TAG)
            if req == True:
                if i == 0:
                    data = comm.recv(source=i)
                    usrls = data
                    print(data)
                else: 
                    data = comm.recv(source=i)
                    name = find_name_by_rank(usrls,i)
                    print(f"{name}: {data}")
            else:
                sleep(0.01)
    
    
    """