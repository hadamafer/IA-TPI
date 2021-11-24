from pandas import read_csv

df = read_csv("los_hipertensos.csv",sep='[;,,]', engine= 'python')


# Shuffle your dataset 
shuffle_df = df.sample(frac=1)

# Define a size for your train set 
train_size = int(0.7 * len(df))

# Split your dataset 
train_set = shuffle_df[:train_size]
test_set = shuffle_df[train_size:]

print(train_set)
print(test_set)