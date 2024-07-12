import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable

warnings.filterwarnings("ignore")

# Function to generate and save images for a given sport
def generate_and_save_images(sport):
    os.chdir('/Users/harsha/Desktop/Codedex/archive/')
    olympic_data = pd.read_csv('olympic_dataset.csv')

    sport_data = olympic_data[olympic_data['Sport'] == sport]

    # Styles for the plots
    plt.style.use('ggplot')

    os.chdir('/Users/harsha/Desktop/Codedex/Website/static/ne_110m_admin_0_countries/')
    world = gpd.read_file('ne_110m_admin_0_countries.shp')

    # Aggregate the number of athletes by region
    region_dist = sport_data['region'].value_counts().reset_index()
    region_dist.columns = ['region', 'athletes']

    os.chdir('/Users/harsha/Desktop/Codedex/Website/static/images/')
    # Merge with the world map
    world_data = world.merge(region_dist, left_on='ADMIN', right_on='region', how='left').fillna(0)

    # Plot 1: Athlete Representation by Region
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    world.boundary.plot(ax=ax, linewidth=1)
    world_data.plot(column='athletes', ax=ax, legend=True, cax=cax, legend_kwds={'label': "Number of Athletes"}, cmap='OrRd')
    ax.set_title(f'Athlete Representation by Region: {sport}', fontsize=16)
    plt.savefig(f'{sport}_plot01.png')


    # Plot 2: Medal Distribution by Country
    plt.figure(figsize=(12, 8))
    medal_dist = sport_data[sport_data['Medal'] != 'No Medal'].groupby('region')['Medal'].count().sort_values(ascending=False)
    sns.barplot(x=medal_dist.values, y=medal_dist.index, palette='viridis')
    plt.title('Medal Distribution by Country', fontsize=16)
    plt.xlabel('Number of Medals')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot02.png')

    sport_data = olympic_data[olympic_data['Sport'] == 'Cross Country Skiing']

    # Events Breakdown
    plt.figure(figsize=(12, 8))
    event_dist = sport_data['Event'].value_counts()
    sns.barplot(x=event_dist.values, y=event_dist.index, palette='crest')
    plt.title(f'Events Breakdown: {sport}')
    plt.xlabel('Number of Participants')
    plt.ylabel('Event')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot03.png')

    # Plot 3: Gender Distribution
    plt.figure(figsize=(12, 8))
    gender_dist = sport_data['Sex'].value_counts()
    plt.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
    plt.title('Gender Distribution', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{sport}_plot04.png')

    # Plot 4: Age Distribution
    plt.figure(figsize=(12, 8))
    sns.histplot(sport_data['Age'], bins=20, kde=False, color='blue')
    plt.title('Age Distribution', fontsize=16)
    plt.xlabel('Age')
    plt.ylabel('Number of Athletes')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot05.png')

    # Performance by Age Group
    age_groups = pd.cut(sport_data['Age'], bins=[0, 20, 25, 30, 35, 40, 100], right=False)
    age_group_medals = sport_data[sport_data['Medal'] != 'No Medal'].groupby(age_groups)['Medal'].count()

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=age_group_medals.index.astype(str), y=age_group_medals.values, palette='Reds')
    plt.title('Performance by Age Group', fontsize=16)
    plt.xlabel('Age Group')
    plt.ylabel('Number of Medals')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot06.png')

    # Medals Over Time by Country
    medals_over_time_country = sport_data[sport_data['Medal'] != 'No Medal'].groupby(['Year', 'region'])[
        'Medal'].count().unstack().fillna(0)

    # Plotting the line chart
    plt.figure(figsize=(12, 8))
    medals_over_time_country.plot(kind='line', marker='o', ax=plt.gca())
    plt.title('Medals Over Time by Country', fontsize=16)
    plt.xlabel('Year')
    plt.ylabel('Number of Medals')
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot07.png')

    # Top Athletes
    top_athletes = sport_data[sport_data['Medal'] != 'No Medal']['Name'].value_counts().head(10)

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_athletes.values, y=top_athletes.index, palette='coolwarm')
    plt.title('Top Athletes', fontsize=16)
    plt.xlabel('Number of Medals')
    plt.ylabel('Athlete')
    plt.tight_layout()
    plt.savefig(f'{sport}_plot08.png')


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_graphs.py <sport_name>")
        sys.exit(1)
    sport = sys.argv[1]
    generate_and_save_images(sport)

