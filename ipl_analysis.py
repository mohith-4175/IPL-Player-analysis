import os
import pandas as pd

folder_path = r'C:\Users\DINESH\OneDrive\Documents\player analysis'

# Show all files being read
all_files = [
    os.path.join(folder_path, f)
    for f in os.listdir(folder_path)
    if f.endswith('.csv') and '_info' not in f
]

print(f"Files being read: {len(all_files)}")
print(all_files[:5])  # Show first 5 files

df_list = []
for file in all_files:
    try:
        df_match = pd.read_csv(file)
        df_list.append(df_match)
    except Exception as e:
        print(f"Skipping {file} due to error: {e}")


# Combine all matches into one DataFrame
if df_list:
    df = pd.concat(df_list, ignore_index=True)
    print("Sample data:")
    print(df.head())
    print(f"Columns: {df.columns.tolist()}")
else:
    print("⚠️ No valid match files loaded.")

# Group by player and sum runs
top_scorers = df.groupby('striker')['runs_off_bat'].sum().reset_index()

# Sort by highest runs
top_scorers = top_scorers.sort_values(by='runs_off_bat', ascending=False).head(10)

print("🏏 Top 10 Run Scorers:")
print(top_scorers)

# Calculate balls faced (excluding extras)
balls_faced = df[df['wides'].isna()].groupby('striker').size().reset_index(name='balls_faced')

# Merge with runs
batting_stats = pd.merge(top_scorers, balls_faced, on='striker')

# Calculate Strike Rate
batting_stats['strike_rate'] = (batting_stats['runs_off_bat'] / batting_stats['balls_faced']) * 100

# Sort by Strike Rate
batting_stats = batting_stats.sort_values(by='strike_rate', ascending=False)

print("🎯 Top Batters by Strike Rate (among top run scorers):")
print(batting_stats[['striker', 'runs_off_bat', 'balls_faced', 'strike_rate']])

# Filter rows where a player was dismissed
wickets = df[df['player_dismissed'].notna()]

# Count dismissals per bowler
top_wicket_takers = wickets.groupby('bowler').size().reset_index(name='wickets')

# Sort and take top 10
top_wicket_takers = top_wicket_takers.sort_values(by='wickets', ascending=False).head(10)

print("🔥 Top 10 Wicket Takers:")
print(top_wicket_takers)

# Total runs conceded by bowler (runs + extras)
df['total_runs_conceded'] = df['runs_off_bat'] + df['extras']
bowler_runs = df.groupby('bowler')['total_runs_conceded'].sum().reset_index()

# Valid deliveries (exclude wides and no-balls)
valid_balls = df[df['wides'].isna() & df['noballs'].isna()]
bowler_balls = valid_balls.groupby('bowler').size().reset_index(name='balls_bowled')

# Merge runs and balls
bowling_stats = pd.merge(top_wicket_takers, bowler_runs, on='bowler')
bowling_stats = pd.merge(bowling_stats, bowler_balls, on='bowler')

# Calculate overs and economy
bowling_stats['overs'] = bowling_stats['balls_bowled'] / 6
bowling_stats['economy'] = bowling_stats['total_runs_conceded'] / bowling_stats['overs']

# Sort by economy
bowling_stats = bowling_stats.sort_values(by='economy')

print("🎯 Economy Rate of Top Wicket Takers:")
print(bowling_stats[['bowler', 'wickets', 'economy']])

# Group by season and striker, sum runs
season_runs = df.groupby(['season', 'striker'])['runs_off_bat'].sum().reset_index()

# For each season, get top 1-3 scorers
top_per_season = season_runs.sort_values(['season', 'runs_off_bat'], ascending=[True, False]).groupby('season').head(3)

print("🏆 Top 3 Run Scorers Each Season:")
print(top_per_season)

#export
top_batters.to_csv('top_batters.csv', index=False)
strike_rates.to_csv('strike_rates.csv', index=False)
top_bowlers.to_csv('top_wicket_takers.csv', index=False)
economy_rates.to_csv('bowler_economy.csv', index=False)
top_per_season.to_csv('seasonal_top_run_scorers.csv', index=False)




import matplotlib.pyplot as plt

#plot for best batsmen conidering runs
plt.figure(figsize=(10,6))
plt.bar(top_scorers['striker'], top_scorers['runs_off_bat'], color='orange')
plt.title('Top 10 Run Scorers in IPL')
plt.xlabel('Player')
plt.ylabel('Total Runs')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#plot for best batsmen considering strike rate
plt.figure(figsize=(10,6))
plt.bar(batting_stats['striker'], batting_stats['strike_rate'], color='green')
plt.title('Top 10 Run Scorers by Strike Rate')
plt.xlabel('Player')
plt.ylabel('Strike Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#top bowlers cosidering wickets
plt.figure(figsize=(10,6))
plt.bar(top_wicket_takers['bowler'], top_wicket_takers['wickets'], color='blue')
plt.title('Top 10 Wicket Takers in IPL')
plt.xlabel('Bowler')
plt.ylabel('Wickets')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#top bowler considering economy
plt.figure(figsize=(10,6))
plt.bar(bowling_stats['bowler'], bowling_stats['economy'], color='purple')
plt.title('Economy Rate of Top 10 Wicket Takers')
plt.xlabel('Bowler')
plt.ylabel('Economy Rate')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#top run scorer in each season
top1_per_season = season_runs.sort_values(['season', 'runs_off_bat'], ascending=[True, False]).groupby('season').head(1)

plt.figure(figsize=(12,6))
plt.bar(top1_per_season['season'].astype(str), top1_per_season['runs_off_bat'], color='darkorange')
plt.title("Top Run Scorer Each Season")
plt.xlabel("Season")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
