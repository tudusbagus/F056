import re
import os

filepath = 'brilcalc.log'
if not os.path.exists(filepath) and os.path.exists('Ex2/brilcalc.log'):
    filepath = 'Ex2/brilcalc.log'

with open(filepath, 'r') as f:
    content = f.read()

summary_block = content.split('#Summary:')[-1]

pattern = r'\|\s*[\d\.]+\s*\|\s*[\d\.]+\s*\|\s*[\d\.]+\s*\|\s*[\d\.]+\s*\|\s*[\d\.]+\s*\|\s*([\d\.]+)\s*\|'
match = re.search(pattern, summary_block)

if match:
    recorded_pb = float(match.group(1))
    recorded_fb = recorded_pb / 1000.0
    print(f"Luminosidade integrada recorded: {recorded_fb:.1f} fb-1")
