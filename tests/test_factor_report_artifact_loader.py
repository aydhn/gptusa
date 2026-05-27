import pytest
from pathlib import Path
import pandas as pd
from usa_signal_bot.feature_engine.factor_explainability.factor_report_artifact_loader import load_factor_table_csv, FactorReportArtifactLoaderError

def test_load_factor_table_csv_forbidden_columns(tmp_path):
    df = pd.DataFrame({"factor": [1,2], "buy": [0,1]})
    p = tmp_path / "test.csv"
    df.to_csv(p, index=False)
    with pytest.raises(FactorReportArtifactLoaderError, match="Forbidden execution columns found"):
        load_factor_table_csv(p)

def test_load_factor_table_csv_path_traversal():
    with pytest.raises(FactorReportArtifactLoaderError, match="Path traversal"):
        load_factor_table_csv(Path("../some_path.csv"))
