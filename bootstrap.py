import numpy as np

np.random.seed(42)

def block_bootstrap_diff(ret_normal, ret_stress, block_size=20, n_boot=2000):
    n_normal = len(ret_normal)
    n_stress = len(ret_stress)

    boot_diff = []

    for _ in range(n_boot):

        # Normal-Regime
        n_blocks_normal = int(np.ceil(n_normal / block_size))
        starts_normal = np.random.randint(
            0, n_normal - block_size + 1, size=n_blocks_normal
        )

        indices_normal = np.concatenate([
            np.arange(s, s + block_size)
            for s in starts_normal
        ])[:n_normal]

        sample_normal = ret_normal.iloc[indices_normal]
        mean_normal, _ = avg_pairwise_corr(sample_normal.corr())

        # Stress-Regime
        n_blocks_stress = int(np.ceil(n_stress / block_size))
        starts_stress = np.random.randint(
            0, n_stress - block_size + 1, size=n_blocks_stress
        )

        indices_stress = np.concatenate([
            np.arange(s, s + block_size)
            for s in starts_stress
        ])[:n_stress]

        sample_stress = ret_stress.iloc[indices_stress]
        mean_stress, _ = avg_pairwise_corr(sample_stress.corr())

        # Differenz
        boot_diff.append(mean_stress - mean_normal)

    return np.array(boot_diff)


boot_diff = block_bootstrap_diff(
    ret_normal,
    ret_stress,
    block_size=20,
    n_boot=2000
)

ci_diff = np.percentile(boot_diff, [2.5, 97.5])

print(
    f"Bootstrap 95%-KI der Differenz: "
    f"{boot_diff.mean():.4f} "
    f"[{ci_diff[0]:.4f}, {ci_diff[1]:.4f}]"
)