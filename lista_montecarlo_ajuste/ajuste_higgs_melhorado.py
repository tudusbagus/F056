import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
from iminuit import Minuit
import os

# --- Módulo de Entrada de Dados (Suporte a ROOT ou Dados Sintéticos) ---
def carregar_dados():
    file_path = "pythia_higgs.root"
    if os.path.exists(file_path):
        try:
            import uproot
            tree = uproot.open(file_path)["events"]
            return tree["mH"].array(library="np")
        except ImportError:
            pass
            
    # Gerador sintético de contingência caso o arquivo ROOT não esteja presente
    print("[Aviso] pythia_higgs.root não encontrado ou 'uproot' indisponível. Gerando dados de teste equivalente...")
    np.random.seed(42)
    N = 50000
    n_sig = int(0.05 * N)
    n_bw = int(0.35 * N)
    n_exp = N - n_sig - n_bw
    
    m_sig = np.random.normal(125.0, 3.0, n_sig)
    # Correção: Uso de standard_cauchy com loc=91.0 e scale=2.5
    m_bw = 91.0 + 2.5 * np.random.standard_cauchy(n_bw * 2)
    m_bw = m_bw[(m_bw >= 50) & (m_bw <= 400)][:n_bw]
    
    tau = 60.0
    u = np.random.uniform(0, 1, n_exp)
    m_exp = 50.0 - tau * np.log(1 - u * (1 - np.exp(-(400-50)/tau)))
    
    data = np.concatenate([m_sig, m_bw, m_exp])
    return data[(data >= 50.0) & (data <= 400.0)]

# --- Funções PDF Normalizadas em [50, 400] GeV ---
MMIN, MMAX = 50.0, 400.0

def fs_gauss(m, mu, sigma):
    from scipy.special import erf
    norm = np.sqrt(np.pi / 2.0) * sigma * (erf((MMAX - mu) / (np.sqrt(2) * sigma)) - erf((MMIN - mu) / (np.sqrt(2) * sigma)))
    return np.exp(-0.5 * ((m - mu) / sigma)**2) / norm

def fbw(m, gamma, mu_bw=91.0):
    norm = (np.arctan((MMAX - mu_bw) / (gamma / 2.0)) - np.arctan((MMIN - mu_bw) / (gamma / 2.0))) * (gamma / 2.0)
    return (1.0 / ((m - mu_bw)**2 + (gamma / 2.0)**2)) * (gamma / (2.0 * np.pi)) / (norm * (gamma / (2.0 * np.pi)))

def fexp(m, tau):
    norm = tau * (np.exp(-MMIN / tau) - np.exp(-MMAX / tau))
    return np.exp(-m / tau) / norm

# --- Funções de Custo ---
def nll(dados, mu, sigma, bw_gamma, tau, s, b_bw, b_exp):
    f_s = fs_gauss(dados, mu, sigma)
    f_b1 = fbw(dados, bw_gamma)
    f_b2 = fexp(dados, tau)
    
    densidade = s * f_s + b_bw * f_b1 + b_exp * f_b2
    densidade = np.maximum(densidade, 1e-300)
    
    # NLL Estendido
    return (s + b_bw + b_exp) - np.sum(np.log(densidade))

def main():
    dados = carregar_dados()
    N_total = len(dados)
    print(f"Total de Eventos Carregados: {N_total}")
    
    # 1. Ajuste NLL (Unbinned Extended Maximum Likelihood)
    loss_nll = lambda mu, sigma, bw_gamma, tau, s, b_bw, b_exp: nll(dados, mu, sigma, bw_gamma, tau, s, b_bw, b_exp)
    
    fit_nll = Minuit(loss_nll, mu=125.0, sigma=3.0, bw_gamma=4.0, tau=50.0,
                     s=0.05*N_total, b_bw=0.35*N_total, b_exp=0.60*N_total)
    
    fit_nll.limits["sigma"] = (0.5, 20.0)
    fit_nll.limits["mu"] = (110.0, 140.0)
    fit_nll.limits["s"] = (0, N_total)
    fit_nll.limits["b_bw"] = (0, N_total)
    fit_nll.limits["b_exp"] = (0, N_total)
    
    fit_nll.migrad()
    fit_nll.hesse()
    
    print("\n=== Resultado do Ajuste NLL ===")
    print(f"mu    = {fit_nll.values['mu']:.3f} +/- {fit_nll.errors['mu']:.3f} GeV")
    print(f"sigma = {fit_nll.values['sigma']:.3f} +/- {fit_nll.errors['sigma']:.3f} GeV")
    print(f"s     = {fit_nll.values['s']:.1f} +/- {fit_nll.errors['s']:.1f} eventos")
    
    # 2. Estudo da Dependência de NBINS no Qui-Quadrado
    nbins_list = [50, 100, 200, 500, 1000]
    results_chi2 = []
    
    print("\n" + "="*70)
    print("ESTUDO DA DEPENDÊNCIA DE NBINS NO AJUSTE CHI-QUADRADO")
    print("="*70)
    print(f"{'NBINS':<8} | {'mu (GeV)':<16} | {'sigma (GeV)':<16} | {'s (eventos)':<18} | {'chi2/ndof':<10} | {'p-value':<8}")
    print("-" * 78)
    
    for nbins in nbins_list:
        counts, bin_edges = np.histogram(dados, bins=nbins, range=(MMIN, MMAX))
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        delta_m = (MMAX - MMIN) / nbins
        
        def cost_chi2(mu, sigma, bw_gamma, tau, s, b_bw, b_exp):
            pred = (s * fs_gauss(bin_centers, mu, sigma) + 
                    b_bw * fbw(bin_centers, bw_gamma) + 
                    b_exp * fexp(bin_centers, tau)) * delta_m
            
            var = np.maximum(counts, 1.0)
            return np.sum((counts - pred)**2 / var)
        
        fit_c2 = Minuit(cost_chi2, mu=125.0, sigma=3.0, bw_gamma=4.0, tau=50.0,
                        s=0.05*N_total, b_bw=0.35*N_total, b_exp=0.60*N_total)
        
        fit_c2.limits["sigma"] = (0.5, 20.0)
        fit_c2.limits["mu"] = (110.0, 140.0)
        fit_c2.errordef = Minuit.LEAST_SQUARES
        fit_c2.migrad()
        
        val_chi2 = fit_c2.fval
        ndof = nbins - len(fit_c2.parameters)
        pval = chi2.sf(val_chi2, ndof) if ndof > 0 else 0.0
        
        res = {
            'nbins': nbins,
            'mu': fit_c2.values['mu'], 'mu_err': fit_c2.errors['mu'],
            'sigma': fit_c2.values['sigma'], 'sigma_err': fit_c2.errors['sigma'],
            's': fit_c2.values['s'], 's_err': fit_c2.errors['s'],
            'chi2_ndof': val_chi2 / ndof if ndof > 0 else 0,
            'p_value': pval
        }
        results_chi2.append(res)
        
        print(f"{nbins:<8} | {res['mu']:.2f} +/- {res['mu_err']:.2f}    | {res['sigma']:.2f} +/- {res['sigma_err']:.2f}    | {res['s']:.1f} +/- {res['s_err']:.1f}    | {res['chi2_ndof']:<10.2f} | {res['p_value']:<8.3f}")

    os.makedirs('figuras', exist_ok=True)
    
    # Plot Comparativo dos Parâmetros vs NBINS
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    axes[0].errorbar([r['nbins'] for r in results_chi2], [r['mu'] for r in results_chi2], 
                     yerr=[r['mu_err'] for r in results_chi2], fmt='o-', label=r'$\chi^2$ Fit')
    axes[0].axhline(fit_nll.values['mu'], color='r', linestyle='--', label='NLL (Referência)')
    axes[0].set_xlabel('NBINS')
    axes[0].set_ylabel(r'$\mu$ (GeV)')
    axes[0].set_title(r'Massa do Sinal ($\mu$)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].errorbar([r['nbins'] for r in results_chi2], [r['sigma'] for r in results_chi2], 
                     yerr=[r['sigma_err'] for r in results_chi2], fmt='s-', color='green', label=r'$\chi^2$ Fit')
    axes[1].axhline(fit_nll.values['sigma'], color='r', linestyle='--', label='NLL (Referência)')
    axes[1].set_xlabel('NBINS')
    axes[1].set_ylabel(r'$\sigma$ (GeV)')
    axes[1].set_title(r'Largura do Sinal ($\sigma$)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    axes[2].errorbar([r['nbins'] for r in results_chi2], [r['s'] for r in results_chi2], 
                     yerr=[r['s_err'] for r in results_chi2], fmt='^-', color='purple', label=r'$\chi^2$ Fit')
    axes[2].axhline(fit_nll.values['s'], color='r', linestyle='--', label='NLL (Referência)')
    axes[2].set_xlabel('NBINS')
    axes[2].set_ylabel('Rendimento $s$ (eventos)')
    axes[2].set_title('Eventos de Sinal ($s$)')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figuras/ajuste_melhorado.png', dpi=300)
    plt.close()
    
    print("\n[SUCESSO] Gráfico comparativo gerado em 'figuras/ajuste_melhorado.png'.")

if __name__ == '__main__':
    main()
