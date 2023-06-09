# IMPORTING PACKAGES

import pandas as pd # data processing
import numpy as np # working with arrays
import matplotlib.pyplot as plt # visualization

import itertools # advanced tools

from sklearn.preprocessing import StandardScaler # data normalization
from sklearn.model_selection import train_test_split # data split
from sklearn.tree import DecisionTreeClassifier # Decision tree algorithm
from sklearn.neighbors import KNeighborsClassifier # KNN algorithm
from sklearn.linear_model import LogisticRegression # Logistic regression algorithm
from sklearn.svm import SVC # SVM algorithm
from sklearn.ensemble import RandomForestClassifier # Random forest tree algorithm

from sklearn.metrics import confusion_matrix # evaluation metric
from sklearn.metrics import accuracy_score # evaluation metric
from sklearn.metrics import f1_score # evaluation metric
# IMPORTING DATA

df = pd.read_csv('creditcard.csv')
df.drop('Time', axis = 1, inplace = True)

print(df.head())
cases = len(df)
nonfraud_count = len(df[df.Class == 0])
fraud_count = len(df[df.Class == 1])
fraud_percentage = round(fraud_count/nonfraud_count*100, 2)

print(('CASE COUNT'))
print(('--------------------------------------------'))
print(('Total number of cases are {}'.format(cases)))
print(('Number of Non-fraud cases are {}'.format(nonfraud_count)))
print(('Number of Non-fraud cases are {}'.format(fraud_count)))
print(('Percentage of fraud cases is {}'.format(fraud_percentage)))
print(('--------------------------------------------'))

nonfraud_cases = df[df.Class == 0]
fraud_cases = df[df.Class == 1]

print(('CASE AMOUNT STATISTICS'))
print(('--------------------------------------------'))
print(('NON-FRAUD CASE AMOUNT STATS'))
print(nonfraud_cases.Amount.describe())
print(('--------------------------------------------'))
print(('FRAUD CASE AMOUNT STATS'))
print(fraud_cases.Amount.describe())
print(('--------------------------------------------'))

sc = StandardScaler()
amount = df['Amount'].values

df['Amount'] = sc.fit_transform(amount.reshape(-1, 1))

print((df['Amount'].head(10)))

# DATA SPLIT

X = df.drop('Class', axis = 1).values
y = df['Class'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

print(('X_train samples : '), X_train[:1])
print(('X_test samples : '), X_test[0:1])
print(('y_train samples : '), y_train[0:20])
print(('y_test samples : '), y_test[0:20])

# MODELING

# 1. Decision Tree

tree_model = DecisionTreeClassifier(max_depth = 4, criterion = 'entropy')
tree_model.fit(X_train, y_train)
tree_yhat = tree_model.predict(X_test)

# 2. K-Nearest Neighbors

n = 5

knn = KNeighborsClassifier(n_neighbors = n)
knn.fit(X_train, y_train)
knn_yhat = knn.predict(X_test)

# 3. Logistic Regression

lr = LogisticRegression()
lr.fit(X_train, y_train)
lr_yhat = lr.predict(X_test)

# 4. SVM 

svm = SVC()
svm.fit(X_train, y_train)
svm_yhat = svm.predict(X_test)

# 5. Random Forest Tree

rf = RandomForestClassifier(max_depth = 4)
rf.fit(X_train, y_train)
rf_yhat = rf.predict(X_test)

print(('ACCURACY SCORE'))
print(('------------------------------------------------------------------------'))
print(('Accuracy score of the Decision Tree model is {}'.format(accuracy_score(y_test, tree_yhat))))
print(('------------------------------------------------------------------------'))
print(('Accuracy score of the KNN model is {}'.format(accuracy_score(y_test, knn_yhat))))
print(('------------------------------------------------------------------------'))
print(('Accuracy score of the Logistic Regression model is {}'.format(accuracy_score(y_test, lr_yhat))))
print(('------------------------------------------------------------------------'))
print(('Accuracy score of the SVM model is {}'.format(accuracy_score(y_test, svm_yhat))))
print(('------------------------------------------------------------------------'))
print(('Accuracy score of the Random Forest Tree model is {}'.format(accuracy_score(y_test, rf_yhat))))
print(('------------------------------------------------------------------------'))

print(('F1 SCORE'))
print(('------------------------------------------------------------------------'))
print(('F1 score of the Decision Tree model is {}'.format(f1_score(y_test, tree_yhat))))
print(('------------------------------------------------------------------------'))
print(('F1 score of the KNN model is {}'.format(f1_score(y_test, knn_yhat))))
print(('------------------------------------------------------------------------'))
print(('F1 score of the Logistic Regression model is {}'.format(f1_score(y_test, lr_yhat))))
print(('------------------------------------------------------------------------'))
print(('F1 score of the SVM model is {}'.format(f1_score(y_test, svm_yhat))))
print(('------------------------------------------------------------------------'))
print(('F1 score of the Random Forest Tree model is {}'.format(f1_score(y_test, rf_yhat))))
print(('------------------------------------------------------------------------'))

# 3. Confusion Matrix

# defining the plot function

def plot_confusion_matrix(cm, classes, title, normalize = False, cmap = plt.cm.Blues):
    title = 'Confusion Matrix of {}'.format(title)
    if normalize:
        cm = cm.astype(float) / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation = 'nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment = 'center',
                 color = 'white' if cm[i, j] > thresh else 'black')

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Compute confusion matrix for the models

tree_matrix = confusion_matrix(y_test, tree_yhat, labels = [0, 1]) # Decision Tree
knn_matrix = confusion_matrix(y_test, knn_yhat, labels = [0, 1]) # K-Nearest Neighbors
lr_matrix = confusion_matrix(y_test, lr_yhat, labels = [0, 1]) # Logistic Regression
svm_matrix = confusion_matrix(y_test, svm_yhat, labels = [0, 1]) # Support Vector Machine
rf_matrix = confusion_matrix(y_test, rf_yhat, labels = [0, 1]) # Random Forest Tree


# Plot the confusion matrix

plt.rcParams['figure.figsize'] = (6, 6)

# 1. Decision tree

tree_cm_plot = plot_confusion_matrix(tree_matrix, 
                                classes = ['Non-fraud(0)','fraud(1)'], 
                                normalize = False, title = 'Decision Tree')
plt.savefig('tree_cm_plot.png')
plt.show()

# 2. K-Nearest Neighbors

knn_cm_plot = plot_confusion_matrix(knn_matrix, 
                                classes = ['Non-fraud(0)','fraud(1)'], 
                                normalize = False, title = 'KNN')
plt.savefig('knn_cm_plot.png')
plt.show()

# 3. Logistic regression

lr_cm_plot = plot_confusion_matrix(lr_matrix, 
                                classes = ['Non-fraud(0)','fraud(1)'], 
                                normalize = False, title = 'Logistic Regression')
plt.savefig('lr_cm_plot.png')
plt.show()

# 4. Support Vector Machine

svm_cm_plot = plot_confusion_matrix(svm_matrix, 
                                classes = ['Non-fraud(0)','fraud(1)'], 
                                normalize = False, title = 'SVM')
plt.savefig('svm_cm_plot.png')
plt.show()

# 5. Random forest tree

rf_cm_plot = plot_confusion_matrix(rf_matrix, 
                                classes = ['Non-fraud(0)','fraud(1)'], 
                                normalize = False, title = 'Random Forest Tree')
plt.savefig('rf_cm_plot.png')
plt.show()