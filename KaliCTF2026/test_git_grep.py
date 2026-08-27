import subprocess
import re

out = subprocess.check_output(['git', 'log', '-p'], cwd='skyline-parser').decode('utf-8', errors='ignore')
matches = re.findall(r'(?i)(abdoun|shmeisani|jabal|weibdeh|dabouq|khalda|sweifieh|rabieh|abdali|marka|taj|hussein|sweileh|tla|kursi|amman|location|address|neighborhood)', out)
if matches:
    print("Found matches:")
    for line in out.split('\n'):
        if any(m.lower() in line.lower() for m in matches):
            print(line)
else:
    print("No matches found.")
