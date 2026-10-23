import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

PROCESSED = Path('data/processed')
RAW = Path('data/raw')
df_clean = pd.read_pickle(PROCESSED / 'station_hour_clean.pkl')
stations = pd.read_csv(RAW / 'stations.csv')

data_merged = df_clean.merge(stations[['StationId', 'City']], on='StationId', how='left')
data_merged['Datetime'] = pd.to_datetime(data_merged['Datetime'])
data_merged['Date'] = data_merged['Datetime'].dt.normalize()

season_map = {
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Summer', 4: 'Summer', 5: 'Summer',
    6: 'Monsoon', 7: 'Monsoon', 8: 'Monsoon', 9: 'Monsoon',
    10: 'Post-monsoon', 11: 'Post-monsoon'
}
SEASONS = ['Winter', 'Summer', 'Monsoon', 'Post-monsoon']
POLLUTANTS = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
              'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
KEY_POLLUTANTS = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']
BUCKETS = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']

agg_cols = POLLUTANTS + ['AQI_calculated']
city_hour = data_merged.groupby(['City', 'Datetime'])[agg_cols].mean().reset_index()
city_hour['Datetime'] = pd.to_datetime(city_hour['Datetime'])
city_hour['Date'] = city_hour['Datetime'].dt.normalize()
city_hour['Year'] = city_hour['Datetime'].dt.year
city_hour['Month'] = city_hour['Datetime'].dt.month
city_hour['Hour'] = city_hour['Datetime'].dt.hour
city_hour['IsWeekend'] = city_hour['Datetime'].dt.dayofweek >= 5
city_hour['Season'] = pd.Categorical(city_hour['Month'].map(season_map), categories=SEASONS, ordered=True)

city_day = data_merged.groupby(['City', 'Date'])[agg_cols].mean().reset_index()
city_day['Date'] = pd.to_datetime(city_day['Date'])
city_day['Year'] = city_day['Date'].dt.year
city_day['Month'] = city_day['Date'].dt.month
city_day['IsWeekend'] = city_day['Date'].dt.dayofweek >= 5
city_day['Season'] = pd.Categorical(city_day['Month'].map(season_map), categories=SEASONS, ordered=True)
city_day['Bucket'] = pd.cut(
    city_day['AQI_calculated'],
    bins=[-np.inf, 50, 100, 200, 300, 400, np.inf],
    labels=BUCKETS
)

with open('reports/exact_chart_values.txt', 'w', encoding='utf-8') as out:
    out.write(f"City day rows: {len(city_day)}, City hour rows: {len(city_hour)}\n")
    out.write(f"Number of cities: {city_day['City'].nunique()}\n")
    out.write(f"Date range: {city_day['Date'].min()} to {city_day['Date'].max()}\n\n")

    # SECTION 4.1: 4 FAMILIES
    out.write("================ 4.1 FOUR FAMILIES ================\n")
    stats_cols = KEY_POLLUTANTS + ['AQI_calculated']
    for c in stats_cols:
        s = city_day[c].dropna()
        out.write(f"{c}: Mean={s.mean():.2f}, Median={s.median():.2f}, Mode={s.round(1).mode().iloc[0]:.2f}, "
                  f"Q25={s.quantile(0.25):.2f}, Q75={s.quantile(0.75):.2f}, IQR={s.quantile(0.75)-s.quantile(0.25):.2f}, "
                  f"Std={s.std():.2f}, CV={s.std()/s.mean():.2f}, Skew={s.skew():.2f}, Kurt={s.kurtosis():.2f}\n")

    # RELATIONSHIPS
    out.write("\n--- Spearman Correlation with AQI ---\n")
    corr_sp = city_day[POLLUTANTS + ['AQI_calculated']].corr(method='spearman')
    out.write(corr_sp['AQI_calculated'].sort_values(ascending=False).to_string() + "\n")
    out.write(f"Ozone vs NO: {corr_sp.loc['O3', 'NO']:.2f}\n")
    out.write(f"PM2.5 vs PM10: {corr_sp.loc['PM2.5', 'PM10']:.2f}\n")
    out.write(f"NO vs NO2: {corr_sp.loc['NO', 'NO2']:.2f}\n")
    out.write(f"NO2 vs NOx: {corr_sp.loc['NO2', 'NOx']:.2f}\n")

    # CHART 1: CITY SUMMARY
    out.write("\n================ CHART 1: AQI BY CITY ================\n")
    city_summary = (city_day.groupby('City')
                    .agg(
                        n_days=('AQI_calculated', 'count'),
                        AQI_median=('AQI_calculated', 'median'),
                        AQI_mean=('AQI_calculated', 'mean'),
                        PM25_median=('PM2.5', 'median'),
                        AQI_q25=('AQI_calculated', lambda s: s.quantile(0.25)),
                        AQI_q75=('AQI_calculated', lambda s: s.quantile(0.75)),
                        AQI_iqr=('AQI_calculated', lambda s: s.quantile(0.75) - s.quantile(0.25)),
                        pct_poor_or_worse=('AQI_calculated', lambda s: (s > 200).mean() * 100),
                        pct_good_satisf=('AQI_calculated', lambda s: (s <= 100).mean() * 100)
                    )
                    .sort_values('AQI_median', ascending=False))
    out.write(city_summary.to_string() + "\n")

    # CHART 2: BUCKET SHARE
    out.write("\n================ CHART 2: BUCKET SHARE ================\n")
    share = (pd.crosstab(city_day['City'], city_day['Bucket'], normalize='index') * 100).reindex(columns=BUCKETS)
    share['Poor_plus_VP_plus_Sev'] = share['Poor'] + share['Very Poor'] + share['Severe']
    share_sorted = share.loc[share['Poor_plus_VP_plus_Sev'].sort_values(ascending=False).index]
    out.write(share_sorted.round(1).to_string() + "\n")

    # CHART 3: MONTH X CITY PM2.5 HEATMAP
    out.write("\n================ CHART 3: MONTH X CITY PM2.5 ================\n")
    month_city = city_day.pivot_table(index='City', columns='Month', values='PM2.5', aggfunc='median')
    month_city_sorted = month_city.loc[month_city.mean(axis=1).sort_values(ascending=False).index]
    out.write(month_city_sorted.round(1).to_string() + "\n")

    # CHART 4: DIURNAL
    out.write("\n================ CHART 4: DIURNAL ================\n")
    hourly_city = city_hour.groupby('Hour')[['PM2.5', 'NO2', 'CO', 'O3']].mean()
    hourly_norm = hourly_city / hourly_city.mean()
    out.write("Hourly Means:\n" + hourly_city.round(2).to_string() + "\n")
    out.write("Hourly Normalized:\n" + hourly_norm.round(2).to_string() + "\n")
    out.write("\nHourly PM2.5 by Season:\n")
    for season in SEASONS:
        sub = city_hour[city_hour['Season'] == season].groupby('Hour')['PM2.5'].mean()
        out.write(f"Season: {season}\n")
        out.write(f"  Min: {sub.min():.2f} at {sub.idxmin()}h, Max: {sub.max():.2f} at {sub.idxmax()}h, Ratio Max/Min: {sub.max()/sub.min():.2f}\n")
        out.write(f"  Morning Peak: around {sub.loc[7:11].idxmax()}h ({sub.loc[7:11].max():.2f})\n")
        out.write(f"  Evening Peak: around {sub.loc[19:23].idxmax()}h ({sub.loc[19:23].max():.2f})\n")
        out.write(f"  Afternoon Valley: around {sub.loc[14:18].idxmin()}h ({sub.loc[14:18].min():.2f})\n")

    # CHART 5: LOCKDOWN
    out.write("\n================ CHART 5: LOCKDOWN ================\n")
    def lockdown_window(d, year):
        return d[(d['Date'] >= f'{year}-03-25') & (d['Date'] <= f'{year}-05-31')]

    w19 = lockdown_window(city_day, 2019)
    w20 = lockdown_window(city_day, 2020)
    c19_cities = w19.groupby('City').size().loc[lambda s: s >= 30].index
    c20_cities = w20.groupby('City').size().loc[lambda s: s >= 30].index
    common_cities = c19_cities.intersection(c20_cities)

    m19 = w19[w19['City'].isin(common_cities)].groupby('City')[['PM2.5', 'NO2', 'AQI_calculated']].mean()
    m20 = w20[w20['City'].isin(common_cities)].groupby('City')[['PM2.5', 'NO2', 'AQI_calculated']].mean()
    change = ((m20 - m19) / m19 * 100).dropna()
    change = change.loc[change['NO2'].sort_values().index]
    overall = ((m20.mean() - m19.mean()) / m19.mean() * 100)
    out.write(f"Common cities count: {len(common_cities)}\n")
    out.write(f"Overall change: NO2={overall['NO2']:.2f}%, PM2.5={overall['PM2.5']:.2f}%, AQI={overall['AQI_calculated']:.2f}%\n")
    out.write("City by City:\n")
    out.write(change[['NO2', 'PM2.5', 'AQI_calculated']].round(2).to_string() + "\n")

    # WEEKDAY VS WEEKEND
    out.write("\n================ WEEKDAY VS WEEKEND ================\n")
    wk = city_day.groupby('IsWeekend')[KEY_POLLUTANTS + ['AQI_calculated']].agg(['mean', 'median']).T
    out.write(wk.round(2).to_string() + "\n")

    # SEASON SUMMARY
    out.write("\n================ SEASON SUMMARY ================\n")
    ss = city_day.groupby('Season', observed=True).agg(
        AQI_median=('AQI_calculated', 'median'),
        AQI_mean=('AQI_calculated', 'mean'),
        PM25_median=('PM2.5', 'median'),
        pct_poor_or_worse=('AQI_calculated', lambda s: (s > 200).mean() * 100)
    )
    out.write(ss.round(2).to_string() + "\n")

print("Done extracting exact values!")
