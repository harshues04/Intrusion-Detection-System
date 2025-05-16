import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from imblearn.over_sampling import SMOTE
import joblib

# Define column names
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
    'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
    'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'class'
]

# Load data with comma separator
train_data = pd.read_csv('data/KDDTrain+.txt', sep=',', names=columns + ['extra'], header=None)
test_data = pd.read_csv('data/KDDTest+.txt', sep=',', names=columns + ['extra'], header=None)

# Drop extra column
train_data = train_data.drop(['extra'], axis=1)
test_data = test_data.drop(['extra'], axis=1)

# Debugging: Check data
print("Train data shape:", train_data.shape)
print("Sample protocol_type values:", train_data['protocol_type'].unique())

# Combine for consistent encoding
data = pd.concat([train_data, test_data], axis=0)

# Encode categorical features
categorical_cols = ['protocol_type', 'service', 'flag']
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    encoders[col] = le
    joblib.dump(le, f'model/{col}_encoder.pkl')

# Map labels to binary (normal: 0, attack: 1)
data['class'] = np.where(data['class'] == 'normal', 0, 1)

# Split back
train_data = data.iloc[:len(train_data)]
test_data = data.iloc[len(train_data):]

# Features and labels
X_train = train_data.drop(['class'], axis=1)
y_train = train_data['class']
X_test = test_data.drop(['class'], axis=1)
y_test = test_data['class']

# Debugging: Check for non-numeric columns
print("X_train dtypes:\n", X_train.dtypes)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
joblib.dump(scaler, 'model/scaler.pkl')

# Handle class imbalance
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Train SVM
model = SVC(kernel='rbf', probability=True, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"F1-Score: {f1_score(y_test, y_pred):.2f}")

# Save model
joblib.dump(model, 'model/svm_model.pkl')