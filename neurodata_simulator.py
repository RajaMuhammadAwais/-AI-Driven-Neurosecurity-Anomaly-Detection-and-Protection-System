import numpy as np

def generate_neurodata(num_samples, num_channels, sampling_rate, anomaly_prob=0.01):
    """
    Generates synthetic neurodata with optional anomalies.

    Args:
        num_samples (int): Number of data points to generate.
        num_channels (int): Number of neurodata channels.
        sampling_rate (int): Sampling rate in Hz.
        anomaly_prob (float): Probability of introducing an anomaly at any given sample.

    Returns:
        np.ndarray: Generated neurodata array (num_samples, num_channels).
    """
    time = np.arange(num_samples) / sampling_rate
    neurodata = np.zeros((num_samples, num_channels))

    for i in range(num_channels):
        # Simulate normal brain rhythms (e.g., alpha, beta, theta, delta)
        alpha = 10 * np.sin(2 * np.pi * 10 * time + np.random.rand() * 2 * np.pi)  # 8-12 Hz
        beta = 5 * np.sin(2 * np.pi * 20 * time + np.random.rand() * 2 * np.pi)   # 13-30 Hz
        theta = 7 * np.sin(2 * np.pi * 6 * time + np.random.rand() * 2 * np.pi)    # 4-7 Hz
        delta = 15 * np.sin(2 * np.pi * 2 * time + np.random.rand() * 2 * np.pi)    # 1-3 Hz

        # Combine rhythms and add random noise
        neurodata[:, i] = alpha + beta + theta + delta + np.random.normal(0, 2, num_samples)

        # Introduce anomalies
        for j in range(num_samples):
            if np.random.rand() < anomaly_prob:
                anomaly_type = np.random.choice(['spike', 'shift', 'burst'])
                if anomaly_type == 'spike':
                    neurodata[j, i] += np.random.uniform(50, 100) * np.sign(np.random.rand() - 0.5)
                elif anomaly_type == 'shift':
                    neurodata[j:, i] += np.random.uniform(20, 40) * np.sign(np.random.rand() - 0.5)
                elif anomaly_type == 'burst':
                    burst_len = np.random.randint(10, 50)
                    neurodata[j:min(j + burst_len, num_samples), i] += np.random.uniform(30, 60) * np.sign(np.random.rand() - 0.5)

    return neurodata

if __name__ == '__main__':
    # Example usage:
    num_samples = 10000
    num_channels = 8
    sampling_rate = 250  # Hz

    synthetic_neurodata = generate_neurodata(num_samples, num_channels, sampling_rate, anomaly_prob=0.001)
    print(f"Generated neurodata shape: {synthetic_neurodata.shape}")
    print(f"First 5 samples of channel 0:\n{synthetic_neurodata[:5, 0]}")

    # Save to a file (e.g., .npy for numpy array)
    np.save('synthetic_neurodata.npy', synthetic_neurodata)
    print("Synthetic neurodata saved to synthetic_neurodata.npy")


