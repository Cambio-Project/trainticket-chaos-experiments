import subprocess

pods = subprocess.getoutput("kubectl get pods")
pod_rows = pods.splitlines()
del pod_rows[0]
faulty_pods_exist = False
for row in pod_rows:
    faulty_pods_exist = not ("1/1" in row and "Running" in row)
    if faulty_pods_exist:
        break

print(f"Do faulty pods exist? The answer is: {faulty_pods_exist}")