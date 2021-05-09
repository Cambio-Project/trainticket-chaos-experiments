import subprocess
import time

while True:
    result = subprocess.getoutput("kubectl get pods | grep 0/1")
    print(f"Result of the command is: {result}")
    time.sleep(10)