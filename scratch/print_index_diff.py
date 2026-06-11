import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
diff_content = subprocess.check_output(['git', 'diff', 'templates/index.html']).decode('utf-8', errors='ignore')
lines = diff_content.splitlines()

# Print only lines starting with + or - to see what was changed
for line in lines:
    if line.startswith('+') or line.startswith('-'):
        # Skip header lines
        if line.startswith('+++') or line.startswith('---'):
            continue
        print(line)
