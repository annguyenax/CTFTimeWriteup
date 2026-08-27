import subprocess
import re

out = subprocess.check_output(['git', 'log', '-p'], cwd='skyline-parser').decode('utf-8', errors='ignore')
ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', out)
print("IPs found:", set(ips))
