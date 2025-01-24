import logging
from pathlib import Path
from typing import List, Union, Optional
import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


# Constants
SUCCESS_THRESHOLD = 2  # Used for ILAE success definition
P_VALUE_THRESHOLD = 0.1  # For significance testing

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_dataset(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load the dataset from a CSV file.

    Args:
        file_path (Union[str, Path]): Path to the dataset file.

    Returns:
        pd.DataFrame: Loaded dataset.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    data = pd.read_csv(file_path)
    if data.empty:
        raise ValueError(f"File is empty: {file_path}")

    logging.info("Dataset loaded successfully.")
    return data

def define_success(ilae_score: Optional[float]) -> Optional[int]:
    """Define success based on ILAE score.

    Args:
        ilae_score (Optional[float]): ILAE score.

    Returns:
        Optional[int]: 1 for success, 0 for no success, NaN if input is NaN.
    """
    if pd.isna(ilae_score):
        return np.nan
    return 1 if ilae_score <= SUCCESS_THRESHOLD else 0

def time_to_success(row: pd.Series) -> Optional[int]:
    """Calculate time to success based on Success_Year columns.

    Args:
        row (pd.Series): Row from the DataFrame.

    Returns:
        Optional[int]: Year of first success or NaN if none.
    """
    for year in range(1, 6):
        if row.get(f"Success_Year{year}") == 1:
            return year
    return np.nan

def perform_anova(data: pd.DataFrame, group_col: str, value_col: str) -> Optional[float]:
    """Perform ANOVA test for a specified column grouped by another column.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        group_col (str): Column to group by.
        value_col (str): Column to analyze.

    Returns:
        Optional[float]: p-value of the ANOVA test, or None if insufficient data or invalid groups.
    """
    # Remove any rows where the value column is NaN
    data = data.dropna(subset=[value_col])
    
    # Group the data by the specified column
    groups = [group[value_col] for _, group in data.groupby(group_col)]
    
    # Check if there are enough groups with more than 1 value
    if len(groups) > 1 and all(len(group) > 1 for group in groups):
        try:
            p_value = f_oneway(*groups).pvalue
            return p_value
        except ValueError:
            # Return None if ANOVA cannot be computed
            return None
    return None  # Not enough data or invalid groups for ANOVA



def plot_success_rates(data: pd.DataFrame, group_col: str, success_cols: List[str], output_dir: Path):
    """Plot success rates over years by group.

    Args:
        data (pd.DataFrame): DataFrame with success rates.
        group_col (str): Grouping column.
        success_cols (List[str]): Columns representing success rates.
        output_dir (Path): Directory to save the plot.
    """
    # Calculate average success rate per group and per year
    grouped = data.groupby(group_col)[success_cols].mean().T  # Transpose to have years as rows
    grouped.index = [f"Year {i}" for i in range(1, len(success_cols) + 1)]  # Set the years dynamically
    
    # Plot the success rates
    grouped.plot(kind="line", marker="o", figsize=(10, 6))
    plt.title("Success Rates Over Years by Group", fontsize=16)
    plt.xlabel("Years After Surgery", fontsize=14)
    plt.ylabel("Success Rate", fontsize=14)
    plt.legend(title="Age Groups", fontsize=12, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_dir / "success_rates_by_group.png")
    plt.close()


def plot_age_group_comparison(data: pd.DataFrame, success_cols: List[str], output_dir: Path):
    """Plot success trends for children vs adults with averaged trends.

    Args:
        data (pd.DataFrame): DataFrame with success rates.
        success_cols (List[str]): Columns representing success rates.
        output_dir (Path): Directory to save the plot.
    """
    # Define the age groups
    age_groups = {"Children": ["< 1", "1 to 2", "3-4", "5 to 7", "8-10", "11 to 14"],
                  "Adults": ["15 to 19", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40 to 44", "45 to 49", "> 50"]}

    # Filter the data by age groups
    children_data = data[data['Binned_Onset_Age'].isin(age_groups["Children"])]
    adults_data = data[data['Binned_Onset_Age'].isin(age_groups["Adults"])]

    # Calculate average success for each age group for each year
    children_avg = children_data[success_cols].mean()
    adults_avg = adults_data[success_cols].mean()

    # Dynamically define years based on the available data in success_cols
    years = [f"Year {i}" for i in range(1, len(success_cols) + 1)]

    # Ensure the lengths of years and averages match
    if len(children_avg) != len(years) or len(adults_avg) != len(years):
        raise ValueError(f"Mismatch between the number of years ({len(years)}) and the number of success values ({len(children_avg)})")

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, children_avg, marker='o', label="Children", linewidth=2)
    plt.plot(years, adults_avg, marker='o', label="Adults", linewidth=2)
    plt.title("Average Success Rates: Children vs Adults", fontsize=16)
    plt.xlabel("Years After Surgery", fontsize=14)
    plt.ylabel("Average Success Rate", fontsize=14)
    plt.legend(title="Group", fontsize=12, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_dir / "success_rates_children_vs_adults.png")
    plt.close()
    plt.close()



def plot_avg_time_to_success(data: pd.DataFrame, group_col: str, time_col: str, output_dir: Path):
    """Plot the average time to success for each age group.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        group_col (str): Column representing the age groups.
        time_col (str): Column representing the time to success.
        output_dir (Path): Directory to save the plot.
    """
    avg_time = data.groupby(group_col)[time_col].mean().dropna()
    avg_time = avg_time.sort_index()

    plt.figure(figsize=(10, 6))
    avg_time.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Average Time to Success by Age Group", fontsize=16)
    plt.xlabel("Age Groups", fontsize=14)
    plt.ylabel("Average Time to Success (Years)", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_dir / "avg_time_to_success.png")
    plt.close()

def plot_tukey_test(data: pd.DataFrame, year_col: str, group_col: str, output_dir: Optional[Path] = None):
    """Perform and plot Tukey's HSD test results.

    Args:
        data (pd.DataFrame): DataFrame with the data.
        year_col (str): Column representing the year.
        group_col (str): Column representing the groups.
        output_dir (Optional[Path]): Directory to save the plot (optional, defaults to None).
    """
    data = data[[group_col, year_col]].dropna()
    tukey = pairwise_tukeyhsd(endog=data[year_col], groups=data[group_col], alpha=0.05)
    print(tukey.summary())

    # Filter out nan values before plotting
    tukey_results = tukey.summary().data[1:]  # Skip header row
    tukey_results = [row for row in tukey_results if not any(pd.isna(val) for val in row[1:])]

    if tukey_results:  # If there are valid results
        tukey.plot_simultaneous(ylabel=group_col, xlabel="Mean Difference")
        plt.title(f"Tukey HSD Test: {year_col}", fontsize=14)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Save the plot only if output_dir is provided
        if output_dir is not None:
            plt.savefig(output_dir / f"tukey_hsd_{year_col}.png")
        else:
            plt.show()  # If no output_dir, display the plot instead of saving it
        plt.close()
    else:
        print(f"No valid Tukey test results for {year_col}")



def main():
    """Main function to execute the analysis pipeline."""
    try:
        # Define paths
        data_dir = Path("C:/Users/ohadp/OneDrive/Desktop/PROJECTS/FinalProject/data").resolve()
        results_dir = Path("C:/Users/ohadp/OneDrive/Desktop/PROJECTS/FinalProject/results/visualizations").resolve()
        results_dir.mkdir(parents=True, exist_ok=True)

        # Load dataset
        file_path = data_dir / "Metadata_Release_Anon.csv"
        data = load_dataset(file_path)

        # Preprocess data
        for year in range(1, 6):
            col_name = f"ILAE_Year{year}"
            success_col = f"Success_Year{year}"
            if col_name in data.columns:
                data[success_col] = data[col_name].apply(define_success)

        data["Time_to_Success"] = data.apply(time_to_success, axis=1)

        # Perform ANOVA for children vs adults for all years
        age_groups = {
            "Children": ["< 1", "1 to 2", "3-4", "5 to 7", "8-10", "11 to 14"],
            "Adults": ["15 to 19", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "40 to 44", "45 to 49", "> 50"]
        }
        children_data = data[data['Binned_Onset_Age'].isin(age_groups["Children"])]
        adults_data = data[data['Binned_Onset_Age'].isin(age_groups["Adults"])]

        for year_col in [f"Success_Year{year}" for year in range(1, 6)]:
            children_success = children_data[year_col].dropna()
            adults_success = adults_data[year_col].dropna()

            if len(children_success) > 1 and len(adults_success) > 1:
                p_value = f_oneway(children_success, adults_success).pvalue
                logging.info(f"ANOVA p-value for Children vs Adults ({year_col}): {p_value}")
                if p_value < P_VALUE_THRESHOLD:
                    logging.info(f"Significant difference found between Children and Adults for {year_col}. Performing Tukey's HSD test.")
                    plot_tukey_test(data, year_col, "Binned_Onset_Age", results_dir)

        # Perform ANOVA and Tukey's HSD tests for all age groups
        success_cols = [f"Success_Year{year}" for year in range(1, 6)]
        for year_col in success_cols:
            p_value = perform_anova(data, "Binned_Onset_Age", year_col)
            if p_value is not None:
                logging.info(f"ANOVA p-value for {year_col}: {p_value}")
                if p_value < P_VALUE_THRESHOLD:
                    logging.info(f"Significant differences found for {year_col}, performing Tukey's HSD test.")
                    plot_tukey_test(data, year_col, "Binned_Onset_Age", results_dir)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


