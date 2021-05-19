from scipy import stats
import pandas as pd
import numpy as np


before = pd.read_csv("steady-log-pre.csv")
after = pd.read_csv("steady-log-post.csv")

before = before["Avg Response Time"]
after = after["Avg Response Time"]

before = before.replace({'0':np.nan, 0:np.nan})
after = after.replace({'0':np.nan, 0:np.nan})

print(f"Mean of before is: {before.mean()}")
print(f"Mean of after is: {after.mean()}")

results = stats.ttest_ind(before.values, after.values, nan_policy='omit')
print(results)