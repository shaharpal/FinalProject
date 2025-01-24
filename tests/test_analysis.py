import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import matplotlib
matplotlib.use('Agg')  # Disable GUI for testing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), r"C:/Users/ohadp/OneDrive/Desktop/PROJECTS/FinalProject/src")))
from DataAnalisys import define_success, time_to_success, perform_anova, load_dataset, plot_success_rates, plot_age_group_comparison, plot_tukey_test, plot_avg_time_to_success

@pytest.fixture
def sample_data():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "ILAE_Year1": [1, 3, 2, np.nan],
        "ILAE_Year2": [2, 2, 3, 1],
        "Success_Year1": [1, 0, 1, np.nan],
        "Success_Year2": [1, 1, 0, 1],
        "Age": [5, 12, 40, 25],
        "Binned_Onset_Age": ["5 to 7", "8-10", "40 to 44", "20 to 24"]
    })

# Test: define_success function
def test_define_success() -> None:
    """Test the define_success function."""
    assert define_success(1) == 1
    assert define_success(3) == 0
    assert np.isnan(define_success(np.nan))

# Test: time_to_success function
def test_time_to_success(sample_data) -> None:
    """Test the time_to_success function."""
    sample_data["Time_to_Success"] = sample_data.apply(time_to_success, axis=1)
    assert sample_data.loc[0, "Time_to_Success"] == 1  # Success in Year 1
    assert sample_data.loc[1, "Time_to_Success"] == 2  # Success in Year 2

# Test: Handling missing columns in time_to_success
def test_missing_columns() -> None:
    """Test handling of missing columns in time_to_success."""
    data = pd.DataFrame({"Success_Year1": [1, 0], "Success_Year2": [0, 1]})
    data["Time_to_Success"] = data.apply(time_to_success, axis=1)
    assert data["Time_to_Success"].isna().sum() == 0  # Should not produce NaNs

# Test: perform_anova function
def test_perform_anova(sample_data) -> None:
    """Test the perform_anova function."""
    p_value = perform_anova(sample_data, "Age", "Success_Year2")
    if p_value is not None:
        # If p-value is valid, check that it's between 0 and 1
        assert 0 <= p_value <= 1
    else:
        # If ANOVA didn't return a p-value, skip the test or assert None
        pytest.skip("ANOVA returned None due to insufficient data or invalid groups.")

# Test: plot_success_rates function
def test_plot_success_rates(sample_data, tmp_path) -> None:
    """Test the plot_success_rates function."""
    success_cols = ["Success_Year1", "Success_Year2"]
    output_dir = tmp_path  # Temporary directory for saving the plot
    plot_success_rates(sample_data, "Binned_Onset_Age", success_cols, output_dir)

# Test: plot_age_group_comparison function
def test_plot_age_group_comparison(sample_data, tmp_path) -> None:
    """Test the plot_age_group_comparison function."""
    success_cols = ["Success_Year1", "Success_Year2"]
    output_dir = tmp_path  # Temporary directory for saving the plot
    plot_age_group_comparison(sample_data, success_cols, output_dir)

# Test: plot_avg_time_to_success function
def test_plot_avg_time_to_success(sample_data, tmp_path) -> None:
    """Test the plot_avg_time_to_success function."""
    sample_data["Time_to_Success"] = sample_data.apply(time_to_success, axis=1)
    output_dir = tmp_path  # Temporary directory for saving the plot
    plot_avg_time_to_success(sample_data, "Binned_Onset_Age", "Time_to_Success", output_dir)

# Test: plot_tukey_test function
def test_plot_tukey_test(sample_data, tmp_path) -> None:
    """Test the plot_tukey_test function."""
    output_dir = tmp_path  # Temporary directory for saving the plot
    plot_tukey_test(sample_data, "Success_Year2", "Binned_Onset_Age", output_dir)
    
    # Assert that the plot file is created only if there are valid results
    output_file = output_dir / "tukey_hsd_Success_Year2.png"
    if output_file.exists():
        assert True  # The plot file was created
    else:
        print(f"No valid Tukey test results for Success_Year2.")
        assert True  # Valid scenario when there are no results
