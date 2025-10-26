import nflreadpy as nfl
import numpy as np
import pandas as pd

# Load data
seasons = [s for s in range(1999, 2026)]
data = nfl.load_pbp(seasons).to_pandas()
cols = data.columns

# Remove rows with bad data and where WP == 0 or 1
clean_data = data.loc[
    (~data['wp'].isna()) & (data['wp'] > 0) & (data['wp'] < 1)
    & (~data['home_wp_post'].isna()) & (data['home_wp_post'] > 0) & (data['home_wp_post'] < 1)
    & (~data['away_wp_post'].isna()) & (data['away_wp_post'] > 0) & (data['away_wp_post'] < 1)
]

# Create post-play WP col since data doesn't have it
clean_data.loc[:, 'wp_post'] = np.where(clean_data['posteam'] == clean_data['home_team'], clean_data['home_wp_post'], clean_data['away_wp_post'])

# Derive log-odds ratio of pre vs. post play WP
clean_data.loc[:, 'wp_lor'] = np.log(clean_data['wp_post'] / clean_data['wp'])

# Aggregate results
print('Pass Average WPA: '+str(np.mean(clean_data.loc[clean_data['play_type'] == 'pass', 'wpa'])))
print('Rush Average WPA: '+str(np.mean(clean_data.loc[clean_data['play_type'] == 'run', 'wpa'])))
print('Pass Average WPLOR: '+str(np.mean(clean_data.loc[clean_data['play_type'] == 'pass', 'wp_lor'])))
print('Rush Average WPLOR: '+str(np.mean(clean_data.loc[clean_data['play_type'] == 'run', 'wp_lor'])))

# Year-by-year results
print('Year\tPasses\tRushes\tPass WPA\tRush WPA\tPass WPLOR\tRush WPLOR\tWPA Diff\tLOR Diff')
print('-'*100)
for s in seasons:
    pass_data = clean_data.loc[(data['season'] == s) & (clean_data['play_type'] == 'pass'), ['wpa', 'wp_lor']]
    rush_data = clean_data.loc[(data['season'] == s) & (clean_data['play_type'] == 'run'), ['wpa', 'wp_lor']]
    pass_wpa = pass_data['wpa'].mean()
    rush_wpa = rush_data['wpa'].mean()
    pass_lor = pass_data['wp_lor'].mean()
    rush_lor = rush_data['wp_lor'].mean()
    print(f'{s}\t{len(pass_data)}\t{len(rush_data)}\t{pass_wpa}\t{rush_wpa}\t{pass_lor}\t{rush_lor}\t{pass_wpa-rush_wpa}\t{pass_lor-rush_lor}')
