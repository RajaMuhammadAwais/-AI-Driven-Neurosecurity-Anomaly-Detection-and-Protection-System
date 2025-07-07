import numpy as np

def add_laplace_noise(data, sensitivity, epsilon):
    """
    Adds Laplace noise to data for differential privacy.

    Args:
        data (np.ndarray): The original data.
        sensitivity (float): The maximum change in the output of a query
                             when a single individual's data is changed.
        epsilon (float): The privacy budget. Smaller epsilon means more privacy.

    Returns:
        np.ndarray: Data with Laplace noise added.
    """
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, data.shape)
    return data + noise

if __name__ == '__main__':
    # Simulate a simple neurodata feature (e.g., average brain activity)
    # In a real scenario, this would be a specific query result or aggregate statistic
    original_neurodata_feature = np.array([10.0, 12.5, 9.8, 11.2, 13.0])
    print(f"Original Neurodata Feature: {original_neurodata_feature}")

    # Define sensitivity and epsilon
    # Sensitivity: If we consider the maximum possible change in a single data point
    # for this feature is 5.0 (e.g., from 0 to 5 or 10 to 15).
    sensitivity = 5.0
    epsilon = 1.0 # A common starting point for epsilon (1.0 means reasonable privacy)

    # Add Laplace noise for differential privacy
    private_neurodata_feature = add_laplace_noise(original_neurodata_feature, sensitivity, epsilon)
    print(f"Differentially Private Neurodata Feature (epsilon={epsilon}): {private_neurodata_feature}")

    # Demonstrate the effect of different epsilon values
    epsilon_high_privacy = 0.1
    private_neurodata_high_privacy = add_laplace_noise(original_neurodata_feature, sensitivity, epsilon_high_privacy)
    print(f"Differentially Private Neurodata Feature (epsilon={epsilon_high_privacy}, high privacy): {private_neurodata_high_privacy}")

    epsilon_low_privacy = 5.0
    private_neurodata_low_privacy = add_laplace_noise(original_neurodata_feature, sensitivity, epsilon_low_privacy)
    print(f"Differentially Private Neurodata Feature (epsilon={epsilon_low_privacy}, low privacy): {private_neurodata_low_privacy}")

    # In a real system, this noisy data would be used for analysis, not the original.
    # The key is that the noise makes it difficult to infer individual data points
    # from the aggregate results, while still allowing for meaningful analysis.


