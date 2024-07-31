import pandas as pd
from aif360.datasets import StandardDataset
from aif360.metrics import BinaryLabelDatasetMetric, ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.inprocessing import AdversarialDebiasing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import tensorflow as tf
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_business = db.Column(db.Boolean, default=False)
    is_professional = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    

def load_data(file_path, label, protected_attr):
    data = pd.read_csv(file_path)
    return data, label, protected_attr

def create_dataset(data, label, protected_attr):
    dataset = StandardDataset(data, label_names=[label], protected_attribute_names=[protected_attr])
    return dataset

def evaluate_bias(dataset, protected_attr):
    metric = BinaryLabelDatasetMetric(dataset, privileged_groups=[{protected_attr: 1}], unprivileged_groups=[{protected_attr: 0}])
    bias_metrics = {
        'mean_difference': metric.mean_difference(),
        'disparate_impact': metric.disparate_impact()
    }
    return bias_metrics

def train_model(dataset, label):
    X_train = dataset.features
    y_train = dataset.labels.ravel()
    model = LogisticRegression(solver='liblinear')
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, dataset):
    X_test = dataset.features
    y_test = dataset.labels.ravel()
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def mitigate_bias(dataset, protected_attr):
    reweighing = Reweighing(unprivileged_groups=[{protected_attr: 0}], privileged_groups=[{protected_attr: 1}])
    dataset_transformed = reweighing.fit_transform(dataset)
    return dataset_transformed

def adversarial_debiasing(dataset, label, protected_attr):
    sess = tf.Session()
    debias_model = AdversarialDebiasing(privileged_groups=[{protected_attr: 1}], unprivileged_groups=[{protected_attr: 0}],
                                        scope_name='debiasing_classifier', sess=sess)
    debias_model.fit(dataset)
    return debias_model

def run_bias_detection(file_path, label, protected_attr):
    data, label, protected_attr = load_data(file_path, label, protected_attr)
    dataset = create_dataset(data, label, protected_attr)
    bias_metrics = evaluate_bias(dataset, protected_attr)
    model = train_model(dataset, label)
    accuracy = evaluate_model(model, dataset)
    return {
        'bias_metrics': bias_metrics,
        'accuracy': accuracy
    }

def run_bias_mitigation(file_path, label, protected_attr):
    data, label, protected_attr = load_data(file_path, label, protected_attr)
    dataset = create_dataset(data, label, protected_attr)
    dataset_transformed = mitigate_bias(dataset, protected_attr)
    debias_model = adversarial_debiasing(dataset_transformed, label, protected_attr)
    return debias_model



# if __name__ == '__main__':
#     file_path = 'path/to/your/data.csv'
#     label = 'your_label_column'
#     protected_attr = 'your_protected_attribute'
#     results = run_bias_detection(file_path, label, protected_attr)
#     print("Bias Metrics:", results['bias_metrics'])
#     print("Model Accuracy:", results['accuracy'])
