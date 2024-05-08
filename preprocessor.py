import pandas as pd

#
#
# def preprocess():
#     global df, region_df
#     # Modifying df only having Season as Summer
#     df = df[df['Season'] == 'Summer']
#
#     # Merging df with region_df based on column NOC using left join technique i.e, the final o/p will be based on df
#     df = df.merge(region_df, on='NOC', how='left')
#     # Removing duplicates in df
#     df.drop_duplicates(inplace=True)
#     # let's stack this dummies with original df along rows i.e, axis=1 as both has equal no of rows by using pd.concat()
#     df = pd.concat([df, pd.get_dummies(df['Medal'], dtype=int)], axis=1)
#     return df
# import pandas as pd

def preprocess(df,region_df):
    # filtering for summer olympics
    df = df[df['Season'] == 'Summer']
    # merge with region_df
    df = df.merge(region_df, on='NOC', how='left')
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df