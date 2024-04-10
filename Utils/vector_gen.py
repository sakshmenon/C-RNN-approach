from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import numpy as np

def vec_split(df):
    secure_vector = []
    insecure_vector = []

    for label in enumerate(df['Label']):
        if label[1] == 1:
            insecure_vector.append(df.loc[label[0]])
        else:
            if len(df.loc[label[0]]['Lines']) == 14:
                pass
            else:           
                secure_vector.append(df.loc[label[0]])

    secure_df = pd.DataFrame(secure_vector)
    insecure_df = pd.DataFrame(insecure_vector)

    # return secure_df, insecure_df
    
    # secure_df.reset_index(drop=True, inplace=True)
    # rand_idx = np.random.choice(np.arange(0, len(secure_df)), size=1000, replace=False)
    # for i in rand_idx:
    #     secure_df.drop([i],inplace=True)
    # secure_df.reset_index(drop = True, inplace=True)

    x_train_secure, x_test_secure, y_train_secure, y_test_secure = train_test_split(secure_df.index.tolist(), secure_df['Label'], random_state=32, test_size = 0.2)
    x_train_secure, x_val_secure, y_train_secure, y_val_secure = train_test_split(x_train_secure, secure_df['Label'][0:len(x_train_secure)], random_state=32, test_size = (1/8))
    x_train_insecure, x_test_insecure, y_train_insecure, y_test_insecure = train_test_split(insecure_df.index.tolist(), insecure_df['Label'], random_state=32, test_size = 0.2)
    x_train_insecure, x_val_insecure, y_train_insecure, y_val_insecure = train_test_split(x_train_insecure, insecure_df['Label'][0:len(x_train_insecure)], random_state=32, test_size = (1/8))

    #80%
    tester = [{'Lines' : secure_df.Lines[i], 'Encoded Lines' : secure_df.Lines[i], 'Label': secure_df.Label[i]} for i in x_train_secure]
    training_df = pd.DataFrame(tester)
    rand_idx = np.random.choice(np.arange(0, len(training_df)), size=len(x_train_insecure), replace=False)

    for i in enumerate(rand_idx):
        new_row = pd.DataFrame({'Lines':insecure_df['Lines'][x_train_insecure[i[0]]],'Encoded Lines' : insecure_df['Lines'][x_train_insecure[i[0]]],'Label':[insecure_df['Label'][x_train_insecure[i[0]]]]})
        training_df = pd.concat([training_df.iloc[:i[1]], new_row, training_df.iloc[i[1]:]], ignore_index=True)
    
    tester = [{'Lines' : secure_df.Lines[i], 'Encoded Lines' : secure_df.Lines[i], 'Label': secure_df.Label[i]} for i in x_val_secure]
    validation_df = pd.DataFrame(tester)
    rand_idx = np.random.choice(np.arange(0, len(validation_df)), size=len(x_val_insecure), replace=False)
    for i in enumerate(rand_idx):
        new_row = pd.DataFrame({'Lines':insecure_df['Lines'][x_val_insecure[i[0]]],'Encoded Lines' : insecure_df['Lines'][x_val_insecure[i[0]]],'Label':[insecure_df['Label'][x_val_insecure[i[0]]]]})
        validation_df = pd.concat([validation_df.iloc[:i[1]], new_row, validation_df.iloc[i[1]:]], ignore_index=True)

    tester = [{'Lines' : secure_df.Lines[i], 'Encoded Lines' : secure_df.Lines[i], 'Label': secure_df.Label[i]} for i in x_test_secure]
    testing_df = pd.DataFrame(tester)
    rand_idx = np.random.choice(np.arange(0, len(testing_df)), size=len(x_test_insecure), replace=False)
    for i in enumerate(rand_idx):
        new_row = pd.DataFrame({'Lines':insecure_df['Lines'][x_test_insecure[i[0]]],'Encoded Lines':insecure_df['Lines'][x_test_insecure[i[0]]],'Label':[insecure_df['Label'][x_test_insecure[i[0]]]]})
        testing_df = pd.concat([testing_df.iloc[:i[1]], new_row, testing_df.iloc[i[1]:]], ignore_index=True)

    return training_df, validation_df, testing_df

def emptyline_pop(dataframe):
    """Remove lines with only empty values from a dataframe"""
    mask = ~((dataframe.isnull().sum(axis=1))==len(dataframe.columns))
    return dataframe[mask].reset_index(drop=True)

def tensor_gen(vectors):

    for i in vectors:
        i['Label']=i['Label'].map({0 : [1, 0], 1:[0, 1]})


    x_train = vectors[0]['Encoded Lines']
    x_val = vectors[1]['Encoded Lines']
    x_test = vectors[2]['Encoded Lines']
    y_train = vectors[0]['Label']
    y_val = vectors[1]['Label']
    y_test = vectors[2]['Label']

    tensor_x_train_proto = [i for i in (x_train)]
    tensor_x_train_proto = tf.constant(tensor_x_train_proto, dtype=tf.float32)

    tensor_x_val_proto = [i for i in (x_val)]
    tensor_x_val_proto = tf.constant(tensor_x_val_proto, dtype=tf.float32)

    tensor_x_test_proto = [i for i in (x_test)]
    tensor_x_test_proto = tf.constant(tensor_x_test_proto, dtype=tf.float32)

    tensor_y_train_proto = [i for i in (y_train)]
    tensor_y_train_proto = tf.constant(tensor_y_train_proto, dtype=tf.float32)

    tensor_y_val_proto = [i for i in (y_val)]
    tensor_y_val_proto = tf.constant(tensor_y_val_proto, dtype=tf.float32)

    tensor_y_test_proto = [i for i in (y_test)]
    tensor_y_test_proto = tf.constant(tensor_y_test_proto, dtype=tf.float32)
        
    return tensor_x_train_proto, tensor_x_val_proto, tensor_x_test_proto, tensor_y_train_proto, tensor_y_val_proto, tensor_y_test_proto