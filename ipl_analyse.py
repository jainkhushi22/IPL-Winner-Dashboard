
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="IPL Winner Analysis", layout="wide")

# Title
st.title("🏏 IPL Winner Analysis Dashboard")
st.markdown("Welcome to the ultimate breakdown of IPL match results! Dive into toss decisions, team performances, and venue dominance.")

# Load Data
df = pd.read_csv("IPL Matches Dataset.csv")
data = df[["id", "season", "team1", "team2", "toss_winner", "toss_decision", "winner", "venue"]]

# Sidebar
st.sidebar.header("Filter the Data")
selected_season = st.sidebar.selectbox("Select a Season", sorted(data['season'].unique(), reverse=True))
filtered_data = data[data["season"] == selected_season]

st.subheader(f"📅 Matches from IPL {selected_season}")
st.dataframe(filtered_data.head())

# Data Summary
st.subheader("🔍 Data Summary")
st.write(f"Total Matches in {selected_season}: {filtered_data.shape[0]}")
st.write("Number of Matches each Team Played:")
team_matches = pd.concat([filtered_data['team1'], filtered_data['team2']]).value_counts()
st.bar_chart(team_matches)


# Toss win vs Match win (Styled + Visual)
st.subheader("🧠 Does Winning the Toss Help Win the Match?")

# Calculate stats
toss_stats = filtered_data["toss_winner"] == filtered_data["winner"]
toss_counts = toss_stats.value_counts()
labels = ['Yes - Toss Winner Also Won Match', 'No - Toss Winner Lost Match']
colors = ['#00cc99', '#ff6666']

# Display as Pie Chart
fig, ax = plt.subplots()
ax.pie(toss_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=[0.05, 0])
ax.set_title("Impact of Toss Win on Match Outcome", fontsize=14)
st.pyplot(fig)

st.write("### 📊 Breakdown:")
st.dataframe(pd.DataFrame({'Result': labels, 'Count': toss_counts.values}))


# Lucky Venue
st.subheader("🍀 Luckiest Venue-Team Combo")
venue_win = filtered_data.groupby(["venue", "winner"]).size().unstack().fillna(0)
lucky_venue = venue_win.stack().idxmax()
st.write(f"The luckiest venue-team combo in {selected_season} was: **{lucky_venue[1]} at {lucky_venue[0]}**")

# Top 10 Venue-Team combos
st.subheader("🏟️ Top 10 Most Dominant Team-Venue Combos")
top10wins_venue = venue_win.stack().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(12,6))
top10wins_venue.plot(kind='bar', color='purple', ax=ax1)
ax1.set_title("Top 10 Most Dominant Team-Venue Combos", fontsize=16)
ax1.set_ylabel("Number of Wins")
ax1.set_xlabel("Venue, Team")
plt.xticks(rotation=45, ha='right')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# Toss Decision vs Venue
st.subheader("🎯 Toss Decision Impact by Venue")
venue_toss_winner = filtered_data.groupby(["venue", "toss_decision", "winner"]).size().reset_index(name='wins')

fig2, ax2 = plt.subplots(figsize=(14,8))
sns.barplot(data=venue_toss_winner, x='venue', y='wins', hue='toss_decision', ci=None, ax=ax2)
ax2.set_title("Toss Decision vs Venue vs Wins", fontsize=16)
ax2.set_ylabel("Number of Wins")
ax2.set_xlabel("Venue")
plt.xticks(rotation=45, ha='right')
ax2.legend(title="Toss Decision")
ax2.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig2)

# Top winner per season
st.subheader("🏆 Top Winner of the Season")
top_per_season = data.groupby(['season', 'winner']).size().reset_index(name='wins')
top_winner = top_per_season.loc[top_per_season.groupby('season')['wins'].idxmax()]
st.dataframe(top_winner[top_winner['season'] == selected_season])

