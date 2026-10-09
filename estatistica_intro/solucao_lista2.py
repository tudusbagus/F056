import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import brentq

# ==========================================
# PROBLEMA 1
# ==========================================
with open('decay.txt', 'r') as f:
    t = [float(line.strip()) for line in f if line.strip()]

t_arr = np.array(t)
N_events = len(t_arr)

figure, axis = plt.subplots(ncols=2, figsize=(12, 6))

# Histograma Simples
axis[0].hist(t_arr, bins=50)
axis[0].set(xlabel='t [s]', ylabel='N')
axis[0].set_title("Histograma das Medidas de Decaimento")

# Histograma com Barras de Erro Poisson
counts_obs, bin_edges_obs = np.histogram(t_arr, bins=50)
bin_centres_obs = (bin_edges_obs[:-1] + bin_edges_obs[1:]) / 2.0
err = np.sqrt(counts_obs)

axis[1].errorbar(bin_centres_obs, counts_obs, yerr=err, fmt='o')
axis[1].set(xlabel='t [s]', ylabel='N')
axis[1].set_title("Histograma com Barras de Erro (sqrt(N))")

plt.tight_layout()
plt.savefig("E2_Problem_1.pdf")
plt.clf()

# ==========================================
# PROBLEMA 2
# ==========================================
def decay_pdf(t_val, tau):
    return (1.0 / tau) * np.exp(-1.0 * t_val / tau)

x_p2 = np.linspace(0.0, 10.0, 1000)
f1_p2 = decay_pdf(x_p2, 1.0)
f2_p2 = decay_pdf(x_p2, 2.0)
f3_p2 = decay_pdf(x_p2, 0.5)

plt.figure(figsize=(8, 5))
plt.plot(x_p2, f1_p2, label=r"$\tau = 1.0$ s")
plt.plot(x_p2, f2_p2, label=r"$\tau = 2.0$ s")
plt.plot(x_p2, f3_p2, label=r"$\tau = 0.5$ s")
plt.xlabel('t [s]')
plt.ylabel('f(t; tau)')
plt.title('PDF Exponencial para Diferentes Valores de Tau')
plt.legend(loc="upper right")
plt.savefig("E2_Problem_2.pdf")
plt.clf()

# Probabilidade t <= 1s sob tau = 2.0s
prob_p2 = integrate.quad(lambda val: decay_pdf(val, 2.0), 0.0, 1.0)[0]
print(f"Problema 2 - P(t <= 1s | tau = 2.0s) = {prob_p2 * 100:.2f}%")

# ==========================================
# PROBLEMA 3
# ==========================================
def likelihood_single(tau, t_measured=1.0):
    return (1.0 / tau) * np.exp(-t_measured / tau)

x_p3 = np.linspace(0.1, 4.0, 1000)
L_single = likelihood_single(x_p3, t_measured=1.0)

plt.figure(figsize=(8, 5))
plt.plot(x_p3, L_single)
plt.xlabel(r'$\tau$ [s]')
plt.ylabel(r'$L(\tau)$')
plt.title(r'Função de Verossimilhança para Uma Medida ($t = 1$ s)')
plt.savefig("E2_Problem_3.pdf")
plt.clf()

# ==========================================
# PROBLEMAS 4 e 5
# ==========================================
def nll(tau, n_obs, sum_t):
    return 2.0 * n_obs * np.log(tau) + 2.0 * sum_t / tau

sum_t_val = np.sum(t_arr)
x_p4 = np.linspace(1.0, 2.5, 1000)
log_likelihood = nll(x_p4, N_events, sum_t_val)

plt.figure(figsize=(8, 5))
plt.plot(x_p4, log_likelihood)
plt.xlabel(r'$\tau$ [s]')
plt.ylabel(r'$-2 \ln L(\tau)$')
plt.title(r'Curva de $-2 \ln L(\tau)$ para o Conjunto de Dados')
plt.savefig("E2_Problem_4.pdf")
plt.clf()

# Estimador de Máxima Verossimilhança
tau_hat_analytical = sum_t_val / N_events
idx_min = np.argmin(log_likelihood)
tau_hat_num = x_p4[idx_min]
min_nll_val = nll(tau_hat_analytical, N_events, sum_t_val)

def moved_nll(tau):
    return nll(tau, N_events, sum_t_val) - (min_nll_val + 1.0)

tau_low = brentq(moved_nll, 1.0, tau_hat_analytical)
tau_high = brentq(moved_nll, tau_hat_analytical, 2.5)

sigma_down = tau_hat_analytical - tau_low
sigma_up = tau_high - tau_hat_analytical

print(f"Problemas 4 e 5 - Estimador tau_hat = {tau_hat_analytical:.4f} s")
print(f"Incerteza +sigma = {sigma_up:.4f} s")
print(f"Incerteza -sigma = {sigma_down:.4f} s")

# ==========================================
# PROBLEMA 6
# ==========================================
def gaussian(x_val, mu, sigma):
    return (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x_val - mu)**2 / (2 * sigma**2))

x_p6 = np.linspace(-5, 5, 1000)
g1 = gaussian(x_p6, 0.0, 1.0)
g2 = gaussian(x_p6, 1.0, 1.0)
g3 = gaussian(x_p6, 0.0, 2.0)

plt.figure(figsize=(8, 5))
plt.plot(x_p6, g1, label=r"$\mu=0, \sigma=1$")
plt.plot(x_p6, g2, label=r"$\mu=1, \sigma=1$")
plt.plot(x_p6, g3, label=r"$\mu=0, \sigma=2$")
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('Distribuição Gaussiana para Diferentes Parâmetros')
plt.legend(loc="upper left")
plt.savefig("E1_Problem_1.pdf")
plt.clf()

# Cálculos de Probabilidade
p_205 = integrate.quad(lambda val: gaussian(val, 200.0, 2.0), 205.0, np.inf)[0]
p_203_single = integrate.quad(lambda val: gaussian(val, 200.0, 2.0), 203.0, np.inf)[0]
p_203_double = p_203_single ** 2

print(f"Problema 6 - P(m >= 205 GeV) = {p_205 * 100:.2f}%")
print(f"Problema 6 - P(duas partículas m >= 203 GeV) = {p_203_double * 100:.2f}%")

# ==========================================
# PROBLEMA 7
# ==========================================
np.random.seed(42)
x_histo_3, x_histo_30, x_histo_60, x_histo_100 = [], [], [], []

for _ in range(10000):
    for N_sample, h_list in zip([3, 30, 60, 100], [x_histo_3, x_histo_30, x_histo_60, x_histo_100]):
        vals = [np.random.exponential(scale=j + 1.0) for j in range(N_sample)]
        h_list.append(np.sum(vals) / N_sample)

fig, axis_p7 = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
axis_p7[0, 0].hist(x_histo_3, bins=30, color='skyblue', edgecolor='black')
axis_p7[0, 0].set_title("N = 3")
axis_p7[0, 0].set_xlabel("x")

axis_p7[0, 1].hist(x_histo_30, bins=30, color='skyblue', edgecolor='black')
axis_p7[0, 1].set_title("N = 30")
axis_p7[0, 1].set_xlabel("x")

axis_p7[1, 0].hist(x_histo_60, bins=30, color='skyblue', edgecolor='black')
axis_p7[1, 0].set_title("N = 60")
axis_p7[1, 0].set_xlabel("x")

axis_p7[1, 1].hist(x_histo_100, bins=30, color='skyblue', edgecolor='black')
axis_p7[1, 1].set_title("N = 100")
axis_p7[1, 1].set_xlabel("x")

plt.savefig("E1_Problem_2.pdf")
plt.clf()
print("Todos os gráficos foram gerados com sucesso!")
