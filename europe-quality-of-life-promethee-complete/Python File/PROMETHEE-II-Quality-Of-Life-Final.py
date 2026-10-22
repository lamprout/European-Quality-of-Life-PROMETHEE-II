import math
import eurostat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from pathlib import Path


OUTPUT_DIR = Path.home() / "Desktop" / "QoL"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
os.chdir(OUTPUT_DIR)



COUNTRIES = ['DK', 'EL', 'ES', 'LU', 'NL', 'PT', 'RO', 'SK', 'SE', 'HU', 'FR', 'IT', 'HR', 'FI', 'AT', 'DE', 'BE', 'CZ', 'PL', 'IE'
]
CRITERIA_INFO = {
    'C.1 Median_Income': ('ilc_di03', {'unit': 'EUR', 'age': 'TOTAL', 'sex': 'T', 'statinfo': 'MED_EI'}),
    'C.2 GDP_Per_Capita': ('nama_10_pc', {'unit': 'CP_PPS_EU27_2020_HAB', 'na_item': 'B1GQ'}),
    'C.3 Ends_Meet': ('ilc_mdes09', {'unit': 'PC', 'lev_diff': 'GRT', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL'}),
    'C.4 H_Deprivation': ('ilc_mdho01', {'unit': 'PC', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL', 'sex': 'T', 'age': 'TOTAL'}),
    'C.5 H_Overcrowding': ('ilc_lvho05a', {'unit': 'PC', 'rskpovth': 'TOTAL', 'age': 'TOTAL', 'sex': 'T'}),
    'C.6 Unemployment': ('lfsa_urgaed', {'sex': 'T', 'age': 'Y15-74', 'isced11': 'TOTAL'}),
    'C.7 Unexpected_Expenses': ('ilc_mdes04', {'unit': 'PC', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL'}),
    'C.8 Arrears': ('ilc_mdes05', {'unit': 'PC', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL'}),
    'C.9 Criminality': ('ilc_mddw03', {'unit': 'PC', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL'}),
    'C.10 Pollution': ('ilc_mddw02', {'unit': 'PC', 'hhcomp': 'TOTAL', 'rskpovth': 'TOTAL'}),
    'C.11 Working_Hours': ('lfsa_ewhan2', {'freq': 'A', 'unit': 'HR', 'nace_r2': 'TOTAL', 'wstatus': 'EMP', 'worktime': 'TOTAL', 'age': 'Y15-64', 'sex': 'T'}),
    'C.12 Tertiary_Education': ('edat_lfse_03', {'freq': 'A', 'unit': 'PC', 'sex': 'T', 'age': 'Y25-74', 'isced11': 'ED5-8'}),
    'C.13 Road_Fatalities': ('tran_sf_roadus', {'freq': 'A','sex': 'T','age': 'TOTAL','unit': 'P_MHAB','pers_cat': 'TOTAL'})
}
CRITERIA = {
    'C.1 Median_Income': 'max',
    'C.2 GDP_Per_Capita': 'max',
    'C.3 Ends_Meet': 'min',
    'C.4 H_Deprivation': 'min',
    'C.5 H_Overcrowding': 'min',
    'C.6 Unemployment': 'min',
    'C.7 Unexpected_Expenses': 'min',
    'C.8 Arrears': 'min',
    'C.9 Criminality': 'min',
    'C.10 Pollution': 'min',
    'C.11 Working_Hours': 'min',
    'C.12 Tertiary_Education': 'max',
    'C.13 Road_Fatalities': 'min',
}
C = [1 if direction == 'max' else 0 for direction in CRITERIA.values()]
WEIGHTS = np.array([0.15, 0.04, 0.11, 0.09, 0.06, 0.14, 0.12, 0.08, 0.07, 0.04, 0.05, 0.02, 0.03])
VALID_FUNCTIONS = ['u', 'us', 'vs', 'le', 'li', 'g']

def Preprocessing(dataset_code, filters, value_name, countries):
    data = eurostat.get_data_df(dataset_code)
    print(f"\n{value_name} ({dataset_code})")
    for column, condition in filters.items():
        if column not in data.columns:
            raise ValueError(
                f"{dataset_code}: missing filter dimension {column!r}. "
                f"Available dimensions: {list(data.columns)}"
            )
        available = data[column].dropna().unique()
        if condition not in available:
            raise ValueError(
                f"{dataset_code}: {column}={condition!r} does not exist. "
                f"Available values: {list(available)[:40]}"
            )
        print(f"Filtering {column} == {condition}")
        data = data.loc[data[column] == condition]

    years = [str(year) for year in range(2014, 2024)]
    missing_years = [year for year in years if year not in data.columns]
    if missing_years:
        print(f"WARNING: {dataset_code}: unavailable year columns {missing_years}; "
              "they will be treated as missing observations and filled by "
              "the existing country-mean imputation when possible.")
        for year in missing_years:
            data[year] = np.nan
    data = data.loc[data['geo\\TIME_PERIOD'].isin(countries)]
    data = pd.melt(data, id_vars=['geo\\TIME_PERIOD'], value_vars=years,
                   var_name='Year', value_name=value_name)
    data.rename(columns={'geo\\TIME_PERIOD': 'Country'}, inplace=True)
    data['Year'] = data['Year'].astype(int)
    data[value_name] = pd.to_numeric(data[value_name], errors='coerce')

    duplicates = data.duplicated(['Country', 'Year'], keep=False)
    if duplicates.any():
        print(data.loc[duplicates, ['Country', 'Year', value_name]].head(15))
        raise ValueError(
            f"{dataset_code}: multiple rows for the same Country-Year. "
            "Check filter dimensions before merging."
        )
    expected = pd.MultiIndex.from_product(
        [countries, range(2014, 2024)], names=['Country', 'Year'])
    data = (data.set_index(['Country', 'Year'])
            .reindex(expected).reset_index())
    print(f"Nonmissing values: {data[value_name].notna().sum()} / {len(data)}")
    if data[value_name].notna().sum() == 0:
        raise ValueError(f"{dataset_code}: no numerical observations for {value_name}")
    return data


def load_data():
    datasets = []
    for criterion, (dataset_code, filters) in CRITERIA_INFO.items():
        print(f'Processing {criterion}...')
        datasets.append(Preprocessing(dataset_code, filters, criterion, COUNTRIES))
    combined_data = datasets[0]
    for dataset in datasets[1:]:
        combined_data = combined_data.merge(
            dataset, on=['Country', 'Year'], how='outer', validate='one_to_one')
    print("\nMissing values before imputation:")
    print(combined_data.isna().sum())
    for column in CRITERIA_INFO:
        combined_data[column] = combined_data.groupby('Country')[column].transform(
            lambda x: x.fillna(x.mean()))
    remaining = combined_data[list(CRITERIA_INFO)].isna().sum()
    if remaining.any():
        raise ValueError(
            'Missing values remain after country-mean imputation. '
            'A country has no observations for one or more criteria:\n'
            + remaining[remaining > 0].to_string()
        )
    aggregated_data = combined_data.groupby('Country').mean(numeric_only=True).reset_index()
    aggregated_data = aggregated_data[['Country'] + list(CRITERIA_INFO)]
    return combined_data, aggregated_data


def choose_preference_function():
    print('\nAvailable Preference Functions:', VALID_FUNCTIONS)
    while True:
        user_input = input('Select a preference function for all criteria: ').strip().lower()
        if user_input in VALID_FUNCTIONS:
            return user_input
        print('Invalid choice, please choose a correct preference function')

def unical(diff_value, q, p, s, f):
    if f == 'u':
        return 1 if diff_value > 0 else 0
    elif f == 'us':
        return 1 if diff_value > q else 0
    elif f == 'vs':
        if diff_value <= 0:
            return 0
        elif p <= 0:
            return 1
        elif diff_value >= p:
            return 1
        return diff_value / p
    elif f == 'le':
        if diff_value <= q:
            return 0
        elif diff_value <= p:
            return 0.5
        return 1
    elif f == 'li':
        if diff_value <= q:
            return 0
        elif p <= q:
            return 1
        elif diff_value >= p:
            return 1
        return (diff_value - q) / (p - q)
    elif f == 'g':
        if diff_value <= 0:
            return 0
        elif s <= 0:
            return 1
        return 1 - math.exp(-(diff_value ** 2) / (2 * s ** 2))

    else:
        raise ValueError(f"Unknown preference function: {f}")


def compute_differences(x, c):
    diff_matrices = {}
    for i, criterion in enumerate(CRITERIA):
        if c[i]:
            diff_matrix = x[:, i:i + 1] - x[:, i]
        else:
            diff_matrix = x[:, i] - x[:, i:i + 1]
        diff_matrices[criterion] = diff_matrix
    return diff_matrices


def compute_thresholds(data):
    data = data[[col for col in data.columns if col in CRITERIA]]
    q_values = data.std() * 0.25
    p_values = data.std() * 0.75
    s_values = data.std() * 0.45
    return np.array([q_values, p_values, s_values])


def compute_preference_matrix(diff_matrices, q, p, s, f):
    pref_matrices = {}
    for i, (criterion, diff_matrix) in enumerate(diff_matrices.items()):
        pref_matrix = np.zeros(diff_matrix.shape)
        for row in range(diff_matrix.shape[0]):
            for col in range(diff_matrix.shape[1]):
                pref_matrix[row, col] = unical(diff_matrix[row, col], q[i], p[i], s[i], f[i])
        pref_matrices[criterion] = pref_matrix
    return pref_matrices


def compute_flows(preference_matrices):
    return {
        criterion: {
            'Positive_Flow': matrix.sum(axis=1) / (len(matrix) - 1),
            'Negative_Flow': matrix.sum(axis=0) / (len(matrix) - 1),
            'Net_Flow': (matrix.sum(axis=1) - matrix.sum(axis=0)) / (len(matrix) - 1),
        }
        for criterion, matrix in preference_matrices.items()
    }


def compute_weighted_flows(unicriterion_flows, weights):
    weighted_flows = {
        f'Weighted_{criterion}': weights[i] * flows['Net_Flow']
        for i, (criterion, flows) in enumerate(unicriterion_flows.items())
    }
    global_net_flow = sum(weighted_flows.values())
    return weighted_flows, global_net_flow


def run_promethee(data, preference_function):
    x = data[list(CRITERIA)].to_numpy()
    q, p, s = compute_thresholds(data)
    differences = compute_differences(x, C)
    preferences = compute_preference_matrix(differences, q, p, s,
                                            [preference_function] * len(CRITERIA))
    flows = compute_flows(preferences)
    weighted, global_net_flow = compute_weighted_flows(flows, WEIGHTS)
    return differences, preferences, flows, weighted, global_net_flow


def save_results_to_excel(aggregated_data, combined_data, avg, yearly):
    diff_matrices, preference_matrices, unicriterion_flows, weighted_flows, global_net_flow = avg
    diff_matrices_yearly, preference_matrices_yearly, _, _, global_net_flow_yearly = yearly
    with pd.ExcelWriter('Quality of Life EU.xlsx', engine='openpyxl') as writer:
        avg_results = aggregated_data.copy()
        avg_results['Global_NetFlow'] = global_net_flow
        avg_results['Rank'] = avg_results['Global_NetFlow'].rank(ascending=False, method='dense')
        avg_results = avg_results.sort_values('Rank')
        avg_results.to_excel(writer, sheet_name='Global NetFlows', index=False)

        yearly_results = combined_data.copy()
        yearly_results['Global_NetFlow'] = global_net_flow_yearly
        yearly_results['Rank'] = yearly_results['Global_NetFlow'].rank(ascending=False, method='dense')
        yearly_results = yearly_results.sort_values(by=['Country', 'Year'],ascending=[True, True])
        yearly_results.to_excel(writer, sheet_name='Global_NetFlow_Yearly', index=False)

        for criterion in CRITERIA:
            sheet_name = criterion[:31]
            labels = aggregated_data['Country']
            diff_df = pd.DataFrame(diff_matrices[criterion], index=labels, columns=labels)
            pref_df = pd.DataFrame(preference_matrices[criterion], index=labels, columns=labels)
            criterion_flows = unicriterion_flows[criterion]
            flow_df = pd.DataFrame({
                'Country': labels,
                'Positive_Flow (Φ⁺)': criterion_flows['Positive_Flow'],
                'Negative_Flow (Φ⁻)': criterion_flows['Negative_Flow'],
                'Net_Flow (Φ)': criterion_flows['Net_Flow'],
                'Weighted_NetFlow': weighted_flows[f'Weighted_{criterion}'],
            }).sort_values('Net_Flow (Φ)', ascending=False)
            diff_df.to_excel(writer, sheet_name=sheet_name, startrow=0, index=True)
            pref_df.to_excel(writer, sheet_name=sheet_name, startrow=len(diff_df) + 5, index=True)
            flow_df.to_excel(writer, sheet_name=sheet_name,
                             startrow=len(diff_df) + len(pref_df) + 10, index=False)

        selected_criterion = 'C.6 Unemployment'
        labels_yearly = combined_data['Country'] + combined_data['Year'].astype(str)
        diff_df_yearly = pd.DataFrame(diff_matrices_yearly[selected_criterion],
                                      index=labels_yearly, columns=labels_yearly)
        pref_df_yearly = pd.DataFrame(preference_matrices_yearly[selected_criterion],
                                      index=labels_yearly, columns=labels_yearly)
        diff_df_yearly.to_excel(writer, sheet_name=f'{selected_criterion}_Diff_Yearly')
        pref_df_yearly.to_excel(writer, sheet_name=f'{selected_criterion}_Pref_Yearly')
    print('PROMETHEE results saved with Difference Matrices, Preference Matrices, and Flows!')

def plot_all_action_profiles(aggregated_data, unicriterion_flows):

    os.makedirs('figures/action_profiles', exist_ok=True)
    
    labels = [criterion.split(' ', 1)[1].replace('_', ' ') for criterion in CRITERIA]

    for idx, country in enumerate(aggregated_data['Country']):

        values = [unicriterion_flows[criterion]['Net_Flow'][idx] for criterion in CRITERIA]
        colors = ['forestgreen' if value >= 0 else 'indianred' for value in values]

        fig, ax = plt.subplots(figsize=(15, 6))
        bars = ax.bar(labels, values, color=colors, width=0.7)
        
        ax.bar_label(bars, labels=[f'{value:.3f}' for value in values], padding=3, fontsize=9)
        ax.axhline(0, color='black', linewidth=1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_ylabel('Unicriterion Net Flow (Φ)')
        ax.set_title(f'{country} — Quality of Life Action Profile (2014–2023)', fontsize=15, fontweight='bold')

        plt.xticks(rotation=40, ha='right')
        plt.tight_layout()
        plt.savefig(f'figures/action_profiles/{country}_action_profile.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

    print('Action profiles created for all countries!')
    
def plot_criterion_rankings(aggregated_data, unicriterion_flows):

    os.makedirs('figures/criterion_rankings', exist_ok=True)

    for criterion in CRITERIA:

        results = pd.DataFrame({'Country': aggregated_data['Country'],'Net_Flow': unicriterion_flows[criterion]['Net_Flow']})
        results = results.sort_values('Net_Flow', ascending=False)
        
        colors = ['forestgreen' if value >= 0 else 'indianred' for value in results['Net_Flow']]
        fig, ax = plt.subplots(figsize=(11, 9))
        bars = ax.barh(results['Country'], results['Net_Flow'], color=colors)
        
        ax.invert_yaxis()
        ax.bar_label(bars, labels=[f'{v:.3f}' for v in results['Net_Flow']], padding=3, fontsize=9)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_xlim(-1.15, 1.15)

        criterion_name = criterion.split(' ', 1)[1].replace('_', ' ')

        ax.set_title(f'{criterion_name} — Country Ranking (2014–2023)', fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('PROMETHEE II Unicriterion Net Flow (Φ)')
        ax.set_ylabel('Country')
        ax.grid(axis='x', linestyle='--', alpha=0.2)
        ax.set_axisbelow(True)

        plt.tight_layout()
        filename = criterion.replace(' ', '_').replace('.', '')
        fig.savefig(f'figures/criterion_rankings/{filename}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
    print('All 13 criterion ranking charts created!')

def main():
    combined_data, aggregated_data = load_data()
    function = choose_preference_function()
    print('\nWeights per Criterion:')
    for criterion, weight in zip(CRITERIA, WEIGHTS):
        print(f'{criterion} has weight: {weight:.4f}')

    avg = run_promethee(aggregated_data, function)
    yearly = run_promethee(combined_data, function)
    plot_all_action_profiles(aggregated_data, avg[2])
    plot_criterion_rankings(aggregated_data, avg[2])
    save_results_to_excel(aggregated_data, combined_data, avg, yearly)


if __name__ == '__main__':
    main()