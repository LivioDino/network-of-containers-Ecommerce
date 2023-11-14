import subprocess
import time
# print(subprocess.run(["/home/desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/SMC/run.sh",], shell=True))


# to start postgrest API (in directory MYCODE/DB)

# to start the 3 redis instances


proc = [None,None,None,None,None,None,None]

def turnOn():
    global proc
    for i in proc:
        if i is None:
            check= True
        else:
            check= False
            break

    if (check):    
            print('Starting proc')
            print(subprocess.run(["echo 0000 | sudo -S docker start tutorial",], shell=True))
            print(subprocess.run(["echo 0000 | sudo -S systemctl start redis-server.service",], shell=True))
            print(subprocess.run(["echo 0000 | sudo -S systemctl start redis-server2.service",], shell=True))
            print(subprocess.run(["echo 0000 | sudo -S systemctl start redis-server3.service",], shell=True))

            proc[0] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/DB; ./postgrest tutorial.conf"],  shell=True)
            proc[1] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/01_ServerCliente; python3 ServerCliente.py",], shell=True)
            proc[2] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/02_ServerTrasportatore; python3 ServerTrasportatore.py",], shell=True)
            proc[3] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/03_ServerFornitore; python3 ServerFornitore.py",], shell=True)
            proc[4] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/01_Cliente; python3 GeneratoreCliente.py",], shell=True)
            proc[5] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/02__Trasportatore; python3 GeneratoreTrasp.py",], shell=True)
            proc[6] = subprocess.Popen(["cd /home/livio/Desktop/TirocinioTronci/network-of-ECOMMERCE-DockerTest/MYCODE/03_Fornitore; python3 GeneratoreFornitori.py",], shell=True)

    return proc

def turnOff():
    global proc
    for i,x in enumerate(reversed(proc)):
        if x is not None:
            proc[i].terminate()
            proc[i] = None

    print('Stopping proc')
    print(subprocess.run(["echo 0000 | sudo -S docker stop tutorial",], shell=True))
    print(subprocess.run(["echo 0000 | sudo -S systemctl stop redis-server.service",], shell=True))
    print(subprocess.run(["echo 0000 | sudo -S systemctl stop redis-server2.service",], shell=True))
    print(subprocess.run(["echo 0000 | sudo -S systemctl stop redis-server3.service",], shell=True))
    




        # proc[1].terminate()
        # proc[1] = None
        # proc[2].terminate()
        # proc[2] = None
        # proc[3].terminate()
        # proc[3] = None
        # proc[4].terminate()
        # proc[4] = None
        # proc[5].terminate()
        # proc[5] = None
        # proc[6].terminate()
        # proc[6] = None


    return proc

if __name__ == '__main__':

    proc = turnOn()
    print(proc)

    time.sleep(2)

    proc = turnOff()
    print(proc)