import pandas as pd
df = pd.DataFrame()
df1 = pd.DataFrame(
    {
        'Courses': ["Spark","PySpark","Python","pandas"],
        'Fee' : [20000,25000,22000,24000]  
    }
)
df2 = pd.DataFrame(
    {
        'Courses': ["Pandas","Hadoop","Hyperion","Java"],
        'Fee': [25000,25200,24500,24900]  
    }
)
df3 = pd.DataFrame(
    {
        'Courses': ["Spark2"],
        'Fee' : [20000]  
    }
)
df4 = pd.DataFrame(
    {
        'Courses': ["Spark4"],
        'Fee' : [20],
        'tool': [400]  
    }
)

df_01 = pd.concat([df, df1, df2, df3, df4], ignore_index=True, sort=False)
print(df)
print(df_01)