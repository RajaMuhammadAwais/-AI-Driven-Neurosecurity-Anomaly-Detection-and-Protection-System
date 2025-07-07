import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def create_autoencoder(timesteps, n_features):
    inputs = Input(shape=(timesteps, n_features))
    encoded = LSTM(128, activation='relu')(inputs)
    encoded = RepeatVector(timesteps)(encoded)
    decoded = LSTM(128, activation='relu', return_sequences=True)(encoded)
    decoded = TimeDistributed(Dense(n_features))(decoded)
    model = Model(inputs, decoded)
    model.compile(optimizer='adam', loss='mse')
    return model

if __name__ == '__main__':
    # Load synthetic neurodata
    neurodata = np.load('synthetic_neurodata.npy')

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    neurodata_scaled = scaler.fit_transform(neurodata)

    # Prepare data for LSTM (timesteps, features)
    timesteps = 10 # Define sequence length
    n_features = neurodata.shape[1]

    X = []
    for i in range(len(neurodata_scaled) - timesteps + 1):
        X.append(neurodata_scaled[i:i + timesteps])
    X = np.array(X)

    # Split data into training and testing sets
    # Assuming most of the data is 'normal' for training the autoencoder
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")

    # Create and train the autoencoder
    model = create_autoencoder(timesteps, n_features)
    model.summary()

    print("\nTraining Autoencoder...")
    history = model.fit(X_train, X_train, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

    # Evaluate the model on the test set
    print("\nEvaluating Autoencoder...")
    test_loss = model.evaluate(X_test, X_test, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")

    # Save the trained model
    model.save('neurosecurity_autoencoder.keras')
    print("Model saved to neurosecurity_autoencoder.keras")

    # Predict on test data to get reconstruction errors
    X_test_pred = model.predict(X_test)
    mse = np.mean(np.power(X_test - X_test_pred, 2), axis=(1, 2))

    # Determine a threshold for anomaly detection (e.g., based on a percentile of MSE on normal data)
    # For simplicity, let's use a high percentile of the training MSE as a threshold
    X_train_pred = model.predict(X_train)
    train_mse = np.mean(np.power(X_train - X_train_pred, 2), axis=(1, 2))
    threshold = np.percentile(train_mse, 95) # 95th percentile as threshold
    print(f"Anomaly Threshold (95th percentile of training MSE): {threshold:.4f}")

    # Identify anomalies in the test set
    anomalies = mse > threshold
    print(f"Number of anomalies detected in test set: {np.sum(anomalies)}")
    print(f"Anomaly detection rate: {np.sum(anomalies) / len(X_test) * 100:.2f}%")

    # You would typically have true anomaly labels to calculate precision, recall, F1-score
    # For synthetic data, we know anomalies were introduced randomly, so this is just a demonstration.


