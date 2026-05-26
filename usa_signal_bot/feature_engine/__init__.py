"""
Feature Factor Engine Foundation (Phase 116)
This module acts as the core technical foundation for advanced indicators, features and factor computations.
It strictly limits all execution to local data reads, schema verification, and metadata production.
It expressly forbids broker interaction, automated trading executions, paper state mutations,
and unauthorized transmission of signals or data. Output from this module is designed for
local research and debugging only and IS NOT investment advice.
"""

from .phase116_models import *
from .kickoff_gate_ingestion import *
from .indicator_registry import *
from .feature_registry import *
from .factor_registry import *
from .feature_input_contract import *
from .feature_schema import *
from .feature_computation_planner import *
from .feature_transform_pipeline import *
from .feature_output_contract import *
from .feature_lineage import *
from .feature_safety_validator import *
from .feature_foundation_report import *
from .feature_foundation_store import *
from .feature_foundation_validation import *
from .feature_foundation_reporting import *
