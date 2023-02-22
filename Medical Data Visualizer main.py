import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

df.dropna(how = 'any')

# Add 'overweight' column
# First calculate and store BMI
df['BMI'] = df['weight'] / (df['height'] / 100) ** 2
# Check if BMI > 25 and type cast to int
df['overweight'] = (df['BMI'] > 25).astype(int)

# normalize 'cholesterol' and 'gluc' data. use this method to change df values in place
df.loc[df.cholesterol == 1, 'cholesterol'] = 0
df.loc[df.cholesterol > 1, 'cholesterol'] = 1
df.loc[df.gluc == 1, 'gluc'] = 0
df.loc[df.gluc > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df[["cardio", 'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']], id_vars="cardio")

    # Draw the catplot with 'sns.catplot()'
    graph = sns.catplot(x="variable", col="cardio", hue="value", data=df_cat, kind="count", sharey=True)
    graph.set_axis_labels("variable", "total")
    fig = graph.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    df2 = df.copy()
    # drop the BMI column
    df2.drop(columns=['BMI'], inplace = True)

    # Keep only the following patient segments that represent correct data
    df_heat = df2[(df2['ap_lo'] <= df2['ap_hi']) & 
                (df2['height'] >= df2['height'].quantile(0.025)) & (df2['height'] <= df2['height'].quantile(0.975)) & 
                (df2['weight'] >= df2['weight'].quantile(0.025)) & (df2['weight'] <= df2['weight'].quantile(0.975))]
  
    # calculate correlation matrix and store it in corr dataframe
    corr = df_heat.corr()
    
    # Set up the matplotlib figure
    plt.figure(figsize = (12,6))
    sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})

    # Generate a mask for the upper triangle
    # ones_like builds a matrix of booleans with the same shape as corr
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Draw the heatmap with 'sns.heatmap()'
    fig = sns.heatmap(corr, mask=mask, square=True, linewidths=1, center=0.0, vmin=-0.1, vmax=0.3, annot=True, fmt='.1f').get_figure()

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
