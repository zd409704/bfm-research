# Baseline 01: Theoretical Derivation of Forward-Backward (FB) Representations and Zero-Shot Value Readout

## 1. Scope and Purpose

This baseline provides a complete, step-by-step mathematical derivation of the **Forward-Backward (FB) representation framework** in a finite state space, answering three foundational questions:
1. How is the successor measure $M_z(s,a,x)$ defined, how is it factorized into $F(s,a,z)$ and $B(x)$ via the normalized density $m_z(s,a,x)$, and why can its temporal-difference (TD) loss be trained purely from expectations without explicitly evaluating the state distribution $\rho(x)$?
2. What exact physical and probabilistic quantities do $F(s,a,z)$, $B(x)$, the one-step contribution vector $c(s,a,z)$, and the covariance matrix $\Sigma_B$ represent after convergence?
3. Why does the inner product $F(s,a,z)^\top z_r$ recover the action-value function $Q_r^{\pi_z}(s,a)$ for any reward function $r(x)$ in the linear span of $B(x)$?

---

## 2. Chapter I: From Value Functions to Successor Measure Factorization

### 2.1 Why Separate Dynamics from Rewards?

In standard reinforcement learning, an agent starting at $(s_0, a_0) = (s, a)$ under a policy $\pi$ with reward function $r(x)$ has action-value function:
$$
Q_r^\pi(s,a) = \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t r(s_{t+1}) \,\middle|\, s_0=s, a_0=a, \pi\right], \qquad \gamma \in (0,1).
$$
Here, environment dynamics, policy behavior, and the task reward $r$ are collapsed into a single scalar $Q_r^\pi(s,a)$. Changing $r$ requires re-estimating $Q_r^\pi$.

For a fixed target state $x$, define the indicator reward:
$$
\mathbf{1}_{\{s_{t+1}=x\}} = \begin{cases} 1, & s_{t+1} = x, \\ 0, & s_{t+1} \neq x. \end{cases}
$$
Every reward function on a finite state space can be expanded as a linear combination of state indicators:
$$
r(s_{t+1}) = \sum_x r(x) \mathbf{1}_{\{s_{t+1}=x\}}.
$$
Substituting this into $Q_r^\pi(s,a)$ and using linearity of expectation yields:
$$
Q_r^\pi(s,a) = \sum_x \underbrace{\mathbb{E}\left[\sum_{t=0}^\infty \gamma^t \mathbf{1}_{\{s_{t+1}=x\}} \,\middle|\, s_0=s, a_0=a, \pi\right]}_{M^\pi(s,a,x)} r(x).
$$
Thus:
$$
Q_r^\pi(s,a) = \sum_x M^\pi(s,a,x) r(x),
$$
where $M^\pi(s,a,x)$ is the **discounted future state visitation measure** (successor measure) for state $x$. It depends only on environment transition dynamics and policy $\pi$, and is completely independent of the task reward $r(x)$.

### 2.2 Bellman Equation for the Successor Measure

For a family of latent-conditioned policies $\{\pi_z\}$ indexed by $z \in \mathbb{R}^d$, write $M_z(s,a,x) := M^{\pi_z}(s,a,x)$. Splitting the $t=0$ transition from $t \ge 1$:
$$
\sum_{t=0}^\infty \gamma^t \mathbf{1}_{\{s_{t+1}=x\}} = \mathbf{1}_{\{s_1=x\}} + \gamma \sum_{k=0}^\infty \gamma^k \mathbf{1}_{\{s_{k+2}=x\}}.
$$
Taking conditional expectations given $(s_0=s, a_0=a)$ and applying the Markov property at $(s_1=s', a_1=a')$:
$$
\mathbb{E}\bigl[\mathbf{1}_{\{s_1=x\}} \mid s_0=s, a_0=a\bigr] = P(s_1=x \mid s,a) = P(x \mid s,a),
$$
$$
\mathbb{E}\left[\sum_{k=0}^\infty \gamma^k \mathbf{1}_{\{s_{k+2}=x\}} \,\middle|\, s_0=s, a_0=a, \pi_z\right] = \mathbb{E}_{s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s')}\bigl[M_z(s', a', x)\bigr].
$$
This gives the exact **successor measure Bellman equation**:
$$
M_z(s,a,x) = P(x \mid s,a) + \gamma \mathbb{E}_{s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s')}\bigl[M_z(s', a', x)\bigr].
$$

### 2.3 Normalized Density $m_z(s,a,x)$ and Low-Rank Bilinear Factorization

Let $\rho(x) > 0$ denote the state distribution in the replay buffer. Define the **relative successor density**:
$$
m_z(s,a,x) := \frac{M_z(s,a,x)}{\rho(x)} \quad \Longleftrightarrow \quad M_z(s,a,x) = \rho(x) m_z(s,a,x).
$$
Then for any reward $r(x)$:
$$
Q_r^{\pi_z}(s,a) = \sum_x \rho(x) m_z(s,a,x) r(x) = \mathbb{E}_{x \sim \rho}\bigl[m_z(s,a,x) r(x)\bigr].
$$
Dividing the Bellman equation by $\rho(x)$ yields the **density Bellman equation**:
$$
m_z(s,a,x) = \frac{P(x \mid s,a)}{\rho(x)} + \gamma \mathbb{E}_{s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s')}\bigl[m_z(s', a', x)\bigr].
$$

Rather than tabulating $m_z(s,a,x)$ for every state pair, FB introduces a rank-$d$ bilinear parameterization:
$$
F: (s,a,z) \mapsto F(s,a,z) \in \mathbb{R}^d, \qquad B: x \mapsto B(x) \in \mathbb{R}^d,
$$
$$
m_z(s,a,x) \approx F(s,a,z)^\top B(x) = \sum_{i=1}^d F_i(s,a,z) B_i(x).
$$
Here $F(s,a,z)$ encodes the **future reachability profile** starting from $(s,a)$ under policy $\pi_z$, while $B(x)$ encodes the **backward outcome representation** of target state $x$.

### 2.4 Why the TD Loss Avoids Explicit Estimation of $\rho(x)$

Let $m_\theta(s,a,z,x) := F_\theta(s,a,z)^\top B_\theta(x)$ and define the stop-gradient target $\bar{m}(s',a',z,x) := F_{\bar{\theta}}(s',a',z)^\top B_{\bar{\theta}}(x)$. The theoretical Bellman target for $m_\theta(s,a,z,x)$ is:
$$
y(s,a,z,x) = \frac{P(x \mid s,a)}{\rho(x)} + \gamma \bar{m}(s',a',z,x).
$$
Consider the weighted squared Bellman error over $(s,a,z)$ and independent $x \sim \rho$:
$$
\mathcal{J}(\theta) = \mathbb{E}_{s,a,z,\, s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s'),\, x \sim \rho}\Bigl[\bigl(m_\theta(s,a,z,x) - y(s,a,z,x)\bigr)^2\Bigr].
$$
Let $\Delta_\theta(s,a,z,s',a',x) := m_\theta(s,a,z,x) - \gamma \bar{m}(s',a',z,x)$. Expanding the square:
$$
\mathcal{J}(\theta) = \mathbb{E}\bigl[\Delta_\theta^2\bigr] - 2 \mathbb{E}\left[\Delta_\theta \frac{P(x \mid s,a)}{\rho(x)}\right] + \mathbb{E}\left[\left(\frac{P(x \mid s,a)}{\rho(x)}\right)^2\right].
$$
The third term is independent of $\theta$, and in the cross term $\gamma \bar{m}(s',a',z,x)$ has stop-gradient so its derivative with respect to $\theta$ is zero. For the active cross term, expanding the expectation over $x \sim \rho$ for fixed $(s,a,z)$ cancels $\rho(x)$ exactly:
$$
\mathbb{E}_{x \sim \rho}\left[m_\theta(s,a,z,x) \frac{P(x \mid s,a)}{\rho(x)}\right] = \sum_x \rho(x) m_\theta(s,a,z,x) \frac{P(x \mid s,a)}{\rho(x)} = \sum_x P(x \mid s,a) m_\theta(s,a,z,x) = \mathbb{E}_{s' \sim P(\cdot \mid s,a)}\bigl[m_\theta(s,a,z,s')\bigr].
$$
Therefore, up to constants with zero gradient wrt $\theta$, the loss reduces to the **practical FB loss**:
$$
\mathcal{L}(\theta) = \mathbb{E}_{s,a,z,\, s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s'),\, x \sim \rho}\Bigl[\bigl(m_\theta(s,a,z,x) - \gamma \bar{m}(s',a',z,x)\bigr)^2\Bigr] - 2\,\mathbb{E}_{s,a,z,\, s' \sim P(\cdot \mid s,a)}\Bigl[m_\theta(s,a,z,s')\Bigr].
$$
- **First term (off-diagonal TD consistency)**: For independently sampled $x \sim \rho$, forces $F(s,a,z)^\top B(x)$ to match $\gamma F(s',a',z)^\top B(x)$.
- **Second term (diagonal real-transition pull-up)**: For the actual observed next state $s' \sim P(\cdot \mid s,a)$, pulls up $F(s,a,z)^\top B(s')$ to account for the one-step arrival $P(x \mid s,a)/\rho(x)$.

---

## 3. Chapter II: Structural Meaning of $F$, $B$, $c$, and $\Sigma_B$ After Convergence

Suppose the bilinear factorization satisfies the density Bellman equation exactly:
$$
F(s,a,z)^\top B(x) = \frac{P(x \mid s,a)}{\rho(x)} + \gamma \mathbb{E}_{s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s')}\bigl[F(s',a',z)^\top B(x)\bigr].
$$

### 3.1 The One-Step Contribution Vector $c(s,a,z)$

Factor out $B(x)$ from the right-hand expectation and define the **one-step contribution vector** $c(s,a,z) \in \mathbb{R}^d$:
$$
c(s,a,z) := F(s,a,z) - \gamma \mathbb{E}_{s' \sim P(\cdot \mid s,a),\, a' \sim \pi_z(\cdot \mid s')}\bigl[F(s',a',z)\bigr].
$$
Then the density Bellman equation takes the compact form:
$$
c(s,a,z)^\top B(x) = \frac{P(x \mid s,a)}{\rho(x)} \quad \Longleftrightarrow \quad P(x \mid s,a) = \rho(x) c(s,a,z)^\top B(x).
$$
Unrolling $F(s,a,z) = c(s,a,z) + \gamma \mathbb{E}[F(s_1,a_1,z)]$ recursively yields:
$$
F(s,a,z) = \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t c(s_t, a_t, z) \,\middle|\, s_0=s, a_0=a, \pi_z\right].
$$
Taking the inner product with $B(x)$ and multiplying by $\rho(x)$ recovers:
$$
M_z(s,a,x) = \rho(x) F(s,a,z)^\top B(x) = \sum_{t=0}^\infty \gamma^t P(s_{t+1}=x \mid s_0=s, a_0=a, \pi_z).
$$

### 3.2 The Covariance / Gram Matrix $\Sigma_B$

Define the second-moment (Gram) matrix of $B(x)$ under $\rho$:
$$
\Sigma_B := \mathbb{E}_{x \sim \rho}\bigl[B(x) B(x)^\top\bigr] = \sum_x \rho(x) B(x) B(x)^\top \in \mathbb{R}^{d \times d}, \qquad (\Sigma_B)_{ij} = \mathbb{E}_{x \sim \rho}[B_i(x) B_j(x)].
$$
Multiplying $\Sigma_B$ by $c(s,a,z)$:
$$
\Sigma_B c(s,a,z) = \sum_x \rho(x) B(x) \bigl(B(x)^\top c(s,a,z)\bigr) = \sum_x \rho(x) B(x) \frac{P(x \mid s,a)}{\rho(x)} = \sum_x P(x \mid s,a) B(x) = \mathbb{E}\bigl[B(s_1) \mid s_0=s, a_0=a\bigr].
$$
Similarly, multiplying $\Sigma_B$ by $F(s,a,z)$:
$$
\Sigma_B F(s,a,z) = \sum_x \rho(x) B(x) \bigl(B(x)^\top F(s,a,z)\bigr) = \sum_x M_z(s,a,x) B(x) = \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t B(s_{t+1}) \,\middle|\, s_0=s, a_0=a, \pi_z\right].
$$
Writing this componentwise for the $d$ scalar coordinates $B_1(x), \dots, B_d(x)$ viewed as $d$ basis reward functions:
$$
Q_{B_i}^{\pi_z}(s,a) := \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t B_i(s_{t+1}) \,\middle|\, s_0=s, a_0=a, \pi_z\right] = \sum_x M_z(s,a,x) B_i(x),
$$
so:
$$
\Sigma_B F(s,a,z) = \begin{bmatrix} Q_{B_1}^{\pi_z}(s,a) \\ \vdots \\ Q_{B_d}^{\pi_z}(s,a) \end{bmatrix}.
$$
When $\Sigma_B$ is invertible:
$$
c(s,a,z) = \Sigma_B^{-1} \mathbb{E}\bigl[B(s_1) \mid s_0=s, a_0=a\bigr], \qquad F(s,a,z) = \Sigma_B^{-1} \begin{bmatrix} Q_{B_1}^{\pi_z}(s,a) \\ \vdots \\ Q_{B_d}^{\pi_z}(s,a) \end{bmatrix}.
$$

### 3.3 Gauge Freedom and Why $\|B(x)\|_2 = \sqrt{d}$ Does Not Imply $\Sigma_B = I$

For any invertible matrix $A \in \mathbb{R}^{d \times d}$, the transformed pair:
$$
\tilde{B}(x) = A B(x), \qquad \tilde{F}(s,a,z) = A^{-\top} F(s,a,z)
$$
preserves the inner product identically:
$$
\tilde{F}(s,a,z)^\top \tilde{B}(x) = F(s,a,z)^\top A^{-1} A B(x) = F(s,a,z)^\top B(x).
$$
Thus, no single coordinate $B_i(x)$ has an intrinsic physical meaning in isolation; only the subspace $\operatorname{span}\{B_1, \dots, B_d\}$ and the bilinear pairing are invariant.

Furthermore, projecting $B(x)$ onto the sphere of radius $\sqrt{d}$ enforces $\|B(x)\|_2^2 = \sum_{i=1}^d B_i(x)^2 = d$ for every $x$, which guarantees only:
$$
\operatorname{tr}(\Sigma_B) = \sum_{i=1}^d \mathbb{E}_{x \sim \rho}[B_i(x)^2] = d.
$$
It does **not** force $\Sigma_B = I$. That is why an explicit orthonormalization regularizer on $B$:
$$
\mathcal{L}_{\mathrm{orth}}(B) = \mathbb{E}_{x, x' \sim \rho}\Bigl[\bigl(B(x)^\top B(x')\bigr)^2\Bigr] - 2\,\mathbb{E}_{x \sim \rho}\Bigl[\|B(x)\|_2^2\Bigr]
$$
is required to drive $\Sigma_B \approx I$. When $\Sigma_B = I$, the formulas simplify directly to:
$$
c_i(s,a,z) = \mathbb{E}[B_i(s_1) \mid s,a], \qquad F_i(s,a,z) = Q_{B_i}^{\pi_z}(s,a).
$$

---

## 4. Chapter III: Zero-Shot Task Reward Encoding $z_r$ and Value Readout

### 4.1 Exact Derivation of $Q_r^{\pi_z}(s,a) = F(s,a,z)^\top z_r$

Suppose a task reward $r(x)$ lies in the linear span of the $d$ basis functions $B_1(x), \dots, B_d(x)$:
$$
r(x) = \sum_{i=1}^d \lambda_i B_i(x) = B(x)^\top \lambda, \qquad \lambda = (\lambda_1, \dots, \lambda_d)^\top \in \mathbb{R}^d.
$$
By linearity of expectation, the action-value function for reward $r$ under policy $\pi_z$ is:
$$
Q_r^{\pi_z}(s,a) = \sum_{i=1}^d \lambda_i Q_{B_i}^{\pi_z}(s,a) = \lambda^\top \begin{bmatrix} Q_{B_1}^{\pi_z}(s,a) \\ \vdots \\ Q_{B_d}^{\pi_z}(s,a) \end{bmatrix} = \lambda^\top \Sigma_B F(s,a,z) = F(s,a,z)^\top (\Sigma_B \lambda).
$$
Now define the **task encoding vector** $z_r \in \mathbb{R}^d$ directly from samples of $\rho$ and $r(x)$:
$$
z_r := \mathbb{E}_{x \sim \rho}\bigl[B(x) r(x)\bigr] = \sum_x \rho(x) B(x) r(x).
$$
Substituting $r(x) = B(x)^\top \lambda$ into the definition of $z_r$:
$$
z_r = \sum_x \rho(x) B(x) B(x)^\top \lambda = \left(\sum_x \rho(x) B(x) B(x)^\top\right) \lambda = \Sigma_B \lambda.
$$
Substituting $\Sigma_B \lambda = z_r$ into $Q_r^{\pi_z}(s,a) = F(s,a,z)^\top (\Sigma_B \lambda)$ yields the fundamental FB value readout identity:
$$
Q_r^{\pi_z}(s,a) = F(s,a,z)^\top z_r.
$$
Crucially, computing $z_r = \mathbb{E}_{x \sim \rho}[B(x) r(x)]$ does **not** require solving for $\lambda$ or inverting $\Sigma_B$, because $\Sigma_B$ is absorbed into $z_r = \Sigma_B \lambda$ while $\Sigma_B^{-1}$ is already absorbed into $F(s,a,z) = \Sigma_B^{-1} Q_B^{\pi_z}(s,a)$.

### 4.2 Single-State Goal Encoding and Intrinsic State-Matching Rewards

For a point-mass preference targeting a single state $g$, where $r_g(x) = \frac{1}{\rho(g)} \mathbf{1}_{\{x=g\}}$:
$$
z_g = \sum_x \rho(x) B(x) r_g(x) = B(g), \qquad Q_{r_g}^{\pi_z}(s,a) = F(s,a,z)^\top B(g) = m_z(s,a,g).
$$
Conversely, given an arbitrary latent command $z \in \mathbb{R}^d$, what one-step intrinsic reward $r_z(y)$ makes the discounted return equal to $F(s,a,z)^\top z$? Since:
$$
F(s,a,z)^\top z = \bigl(\Sigma_B F(s,a,z)\bigr)^\top \Sigma_B^{-1} z = \mathbb{E}\left[\sum_{t=0}^\infty \gamma^t B(s_{t+1})^\top \Sigma_B^{-1} z \,\middle|\, s_0=s, a_0=a, \pi_z\right],
$$
the exact one-step intrinsic reward associated with latent $z$ is:
$$
r_z(y) = B(y)^\top \Sigma_B^{-1} z = \phi(y)^\top z, \qquad \phi(y) := \Sigma_B^{-1} B(y).
$$
Only under exact orthonormalization $\Sigma_B = I$ does $r_z(y)$ reduce to the raw dot product $B(y)^\top z$.

---

## 5. Summary Reference Table

| Symbol | Mathematical Definition | Physical / Algorithmic Interpretation |
|---|---|---|
| $M_z(s,a,x)$ | $\mathbb{E}[\sum_{t=0}^\infty \gamma^t \mathbf{1}_{\{s_{t+1}=x\}} \mid s_0=s, a_0=a, \pi_z]$ | Discounted future visitation count of state $x$ under policy $\pi_z$ |
| $m_z(s,a,x)$ | $M_z(s,a,x) / \rho(x) \approx F(s,a,z)^\top B(x)$ | Relative visitation density normalized by replay distribution $\rho(x)$ |
| $c(s,a,z)$ | $F(s,a,z) - \gamma \mathbb{E}_{s',a'}[F(s',a',z)]$ | One-step forward contribution vector satisfying $\rho(x) c(s,a,z)^\top B(x) = P(x \mid s,a)$ |
| $\Sigma_B$ | $\mathbb{E}_{x \sim \rho}[B(x)B(x)^\top]$ | Feature covariance / Gram matrix linking $F$ to basis action-values |
| $\Sigma_B c(s,a,z)$ | $\mathbb{E}[B(s_1) \mid s_0=s, a_0=a]$ | Expected one-step future backward representation |
| $\Sigma_B F(s,a,z)$ | $[Q_{B_1}^{\pi_z}(s,a), \dots, Q_{B_d}^{\pi_z}(s,a)]^\top$ | Vector of discounted cumulative returns of the $d$ basis features $B_i$ |
| $z_r$ | $\mathbb{E}_{x \sim \rho}[B(x) r(x)] = \Sigma_B \lambda$ | Zero-shot task latent encoding for reward $r(x) = B(x)^\top \lambda$ |
| $F(s,a,z)^\top z_r$ | $Q_r^{\pi_z}(s,a)$ | Zero-shot action-value evaluation of policy $\pi_z$ on reward $r$ |
