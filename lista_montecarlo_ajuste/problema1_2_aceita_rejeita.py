import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.stats import norm

# --- PROBLEMA 1: Função genérica de Aceitação-Rejeição ---
def random_pdf(pdf, N, x_min, x_max, f_max):
    """
    Gera N números aleatórios segundo a PDF especificada via Aceitação-Rejeição.
    Retorna a lista de números aceitos e o total de pares sorteados.
    """
    x_rand = []
    n_tries = 0
    
    while len(x_rand) < N:
        n_tries += 1
        # Sorteio uniforme de x e y
        x = random.uniform(x_min, x_max)
        y = random.uniform(0.0, f_max)
        
        # Critério de aceitação
        if pdf(x) >= y:
            x_rand.append(x)
            
    return np.array(x_rand), n_tries

# PDFs de Teste
def gaussian_pdf(x, mu=0.0, sigma=1.0):
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

def sin2_pdf(x):
    # PDF proporcional a sin^2(x) em [0, pi]
    return np.sin(x)**2

# --- PROBLEMA 2: Testes e Análise de Eficiência ---
def main():
    np.random.seed(42)
    random.seed(42)
    
    N_samples = 10000
    f_max_gauss = 1.0 / np.sqrt(2.0 * np.pi) # ~0.3989
    
    print("="*60)
    print("PARTE I: MÉTODO DE ACEITAÇÃO-REJEIÇÃO")
    print("="*60)
    
    # 2(a) Teste no intervalo [-5, 5]
    x_min, x_max = -5.0, 5.0
    samples, n_tries = random_pdf(gaussian_pdf, N_samples, x_min, x_max, f_max_gauss)
    
    eff_obs = N_samples / n_tries
    area_box = (x_max - x_min) * f_max_gauss
    # Integral da gaussiana padrão em [-5, 5] é ~ 1.0
    eff_exp = 1.0 / area_box
    
    print(f"\n[Intervalo [{x_min}, {x_max}]]")
    print(f"Sorteios necessários para {N_samples} eventos: {n_tries}")
    print(f"Eficiência Observada: {eff_obs:.4f} ({eff_obs*100:.2f}%)")
    print(f"Eficiência Esperada:  {eff_exp:.4f} ({eff_exp*100:.2f}%)")
    
    # Gerar Gráfico para o Problema 2(a)
    x_plot = np.linspace(-5, 5, 1000)
    plt.figure(figsize=(8, 5))
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='MC Aceitação-Rejeição')
    plt.plot(x_plot, gaussian_pdf(x_plot), 'r-', lw=2, label=r'PDF Analítica $\mathcal{N}(0,1)$')
    plt.title('Validação do Gerador de Aceitação-Rejeição')
    plt.xlabel('x')
    plt.ylabel('Densidade de Probabilidade')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('figuras/gauss_aceita_rejeita.png', dpi=300)
    plt.close()

    # 2(b) Comparação de Intervalos
    intervals = [(-3.0, 3.0), (-5.0, 5.0), (-10.0, 10.0)]
    print("\n" + "-"*50)
    print("Estudo da variação da Eficiência por Intervalo:")
    print(f"{'Intervalo':<15} | {'N_sorteios':<12} | {'Efic. Obs (%)':<15} | {'Efic. Esp (%)':<15}")
    print("-" * 50)
    
    for xmin, xmax in intervals:
        s_list, n_tr = random_pdf(gaussian_pdf, N_samples, xmin, xmax, f_max_gauss)
        e_obs = N_samples / n_tr
        
        # Cálculo da integral exata via CDF da normal
        integral = norm.cdf(xmax) - norm.cdf(xmin)
        e_exp = integral / ((xmax - xmin) * f_max_gauss)
        
        print(f"[{xmin:>4.1f}, {xmax:>4.1f}]       | {n_tr:<12} | {e_obs*100:<15.2f} | {e_exp*100:<15.2f}")

    # Repetição de 100 vezes para o intervalo [-5, 5]
    print("\nExecutando 100 simulações de N=10000 para o intervalo [-5, 5]...")
    tries_distribution = []
    for _ in range(100):
        _, n_tr = random_pdf(gaussian_pdf, N_samples, -5.0, 5.0, f_max_gauss)
        tries_distribution.append(n_tr)
        
    plt.figure(figsize=(8, 5))
    plt.hist(tries_distribution, bins=15, color='orange', edgecolor='black', alpha=0.7)
    plt.title(r'Distribuição de $N_{sorteios}$ para 100 experimentos ($N=10^4$, $[-5,5]$)')
    plt.xlabel(r'Número Total de Sorteios ($N_{sorteios}$)')
    plt.ylabel('Frequência')
    plt.grid(True, alpha=0.3)
    plt.savefig('figuras/distribuicao_sorteios.png', dpi=300)
    plt.close()
    
    # Teste extra com outra PDF: sin^2(x) em [0, pi]
    s_sin, n_tr_sin = random_pdf(sin2_pdf, N_samples, 0.0, np.pi, f_max=1.0)
    print(f"\n[PDF Extra: sin^2(x) em [0, pi]] Sorteios: {n_tr_sin}, Eficiência: {N_samples/n_tr_sin*100:.2f}%")
    
    print("\n[SUCESSO] Figuras salvas na pasta 'figuras/'.")

if __name__ == '__main__':
    main()
