sudo nmap -sS -sU -T4 -A -v -PE -PP -PS80,443 -PA3389 -PU40125 -PY -g 53 –script "default or (discovery and safe)" REMOTE_HOST
