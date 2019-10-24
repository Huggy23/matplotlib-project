"""
CPSC-51100, SUMMER 2019
NAME: JASON HUGGY, JOHN KUAGBENU, COREY PAINTER 
PROGRAMMING ASSIGNMENT #6
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('ss13hil.csv')

# Replaces each value with the first number in the range of amounts from 
# PUMS documentation
def replace(TAXP):
    
    if TAXP == 1:
        return 0
    
    elif (TAXP >= 2) and (TAXP <= 21):
        return (TAXP * 50 - 100)
    
    elif (TAXP >=22) and (TAXP <= 62):
        return ((TAXP-22)*100) + 1000
    
    elif TAXP == 63:
        return 5500
        
    elif TAXP >= 64:
        return ((TAXP-64)*1000) + 6000
    
df['TAXP'] = df.TAXP.apply(replace)


# Plots a figure with four subplots, 2 by 2
fig, axs = plt.subplots(2, 2, figsize=(15, 8))
fig.suptitle('Sample Output', fontsize=20, y = 1)

# Creates a pie chart of HHL with legend
HHLcolor=['Blue','DarkOrange','Green','Red','Purple'] # Colors for chart
HHL=['English only', 'Spanish', 'Other Indo-European', 'Asian and Pacific Island languages', 'Other']
label= list(HHL)
axs[0, 0].pie(df.HHL.value_counts(), colors= HHLcolor, startangle= 242, radius= 1.25, counterclock= True, center= (0.5, 0.5))
axs[0, 0].set_title('Household Languages', fontsize= 12)
axs[0, 0].legend(labels = label, loc=2, fontsize= '10', bbox_to_anchor= (-.72, 0.80, .1, .2), markerscale= .05)
axs[0, 0].set_ylabel('HHL', labelpad = 140)


# Creates a histogram of HINCP with superimposed KDE plot
hincp = df.HINCP.dropna()
hincp = hincp[hincp > 10] 
logbins = np.logspace(np.log10(10), np.log10(max(hincp)),85) #logspaces bins of the x axis
axs[0, 1].hist(hincp, bins = logbins, density=True, color = 'Green', alpha= 0.5)
axs[0, 1].set_xscale('log') # logspaces the x axis ticks
axs[0, 1].set_xlim(5, 10**7.2)
hincp.plot.kde(linestyle='--', linewidth=2, color='Black', ax = axs[0, 1])
axs[0, 1].set_yticks([0.000000, 0.000005, 0.000010, 0.000015, 0.000020])
axs[0, 1].set_title('Distribution of Household Income', fontsize=12)
axs[0, 1].set_xlabel('Household Income ($) - Log Scaled')
axs[0, 1].set_ylabel('Density')


# Creates a bar chart of thousands of households for each vehicle value
veh_x= df.VEH.unique()
veh_y= df.VEH.repeat(df.WGTP).value_counts()
veh_y/=1000
x_label= [1,2,3,0,4,5,6]
axs[1, 0].set_xlabel("# of Vehicles")
axs[1, 0].set_ylabel("Thousands of Households")
axs[1, 0].bar(veh_x[~np.isnan(veh_x)], veh_y, width=.85, bottom= 0.0, align='center', color= 'red', tick_label= x_label)
axs[1, 0].set_title('Vehicles Available in Households', fontsize= 12)

# Creates a scatter plot of property taxes vs property value
# Uses WGTP for size of each dot, and first mortage payment is represented by the color of the dot
# Uses a colorbar for reference of MRGP amount 
scatter = df[df.VALP <= 2000000]
i = axs[1, 1].scatter(scatter.VALP, scatter.TAXP, c=scatter.MRGP, s = scatter.WGTP, cmap='seismic', alpha= 0.1)
cbar = plt.colorbar(i, ax=axs[1, 1], ticks= [1250, 2500, 3750, 5000])
cbar.set_label('First Mortgage Payment (Monthly $)')
axs[1, 1].set_xlim(0, 1200000)
axs[1, 1].set_ylim(ymin=0)
axs[1, 1].set_title('Property Taxes vs. Property Values', fontsize=12)
axs[1, 1].set_xlabel('Property Value ($)')
axs[1, 1].set_ylabel('Taxes ($)')

# Adjusts the space in between subplots
plt.subplots_adjust(wspace=0.22, hspace=0.4)

# Saves figure to default directory as a png file. 
plt.savefig('pums.png')