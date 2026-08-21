import re
import os

filepath = 'brilcalc.log' if os.path.exists('brilcalc.log') else 'Ex2/brilcalc.log'
if not os.path.exists(filepath):
    filepath = '../Ex2/brilcalc.log'

with open(filepath, 'r') as f:
    text = f.read()

summary_text = text.split('#Summary:')[-1] if '#Summary:' in text else text
lines = [line for line in summary_text.splitlines() if '|' in line]

recorded_pb = None

# Percorre as linhas do resumo de baixo para cima para pegar a linha final
for line in reversed(lines):
    if any(header in line.lower() for header in ['nfill', 'nrun', 'hltpath', 'totrecorded', 'totdelivered']):
        continue
    
    numbers = re.findall(r'[\d\.]+', line)
    floats = []
    for n in numbers:
        try:
            floats.append(float(n))
        except ValueError:
            pass
    
    # Filtra apenas os valores de luminosidade (> 100 /pb)
    valid_vals = [f for f in floats if f > 100]
    if valid_vals:
        recorded_pb = valid_vals[-1]
        break

if recorded_pb is not None:
    recorded_fb = recorded_pb / 1000.0
    print(f"Luminosidade integrada recorded: {recorded_fb:.1f} fb-1")
else:
    print("Erro: Nao foi possivel extrair o valor de brilcalc.log")
