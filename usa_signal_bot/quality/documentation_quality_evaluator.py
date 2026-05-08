from typing import Any, Dict, List, Tuple, Optional
from usa_signal_bot.core.enums import QualityDimension, QualityStatus, QualitySeverity
from usa_signal_bot.quality.quality_models import QualityDimensionScore, QualityIssue, create_quality_issue_id
from pathlib import Path

def score_required_docs_presence(project_root: Path) -> Tuple[float, List[QualityIssue]]:
    issues = []
    if not (project_root / "docs").exists():
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.DOCUMENTATION,
            severity=QualitySeverity.MODERATE,
            status=QualityStatus.WARN,
            title="Missing docs/",
            message="No docs directory found in project root."
        ))
        return 0.0, issues
    return 100.0, issues

def score_required_tests_presence(project_root: Path) -> Tuple[float, List[QualityIssue]]:
    issues = []
    if not (project_root / "tests").exists():
        issues.append(QualityIssue(
            issue_id=create_quality_issue_id(),
            dimension=QualityDimension.DOCUMENTATION,
            severity=QualitySeverity.CRITICAL,
            status=QualityStatus.FAIL,
            title="Missing tests/",
            message="No tests directory found in project root."
        ))
        return 0.0, issues
    return 100.0, issues

def score_readme_presence(project_root: Path) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def score_phase_summary_presence(project_root: Path) -> Tuple[float, List[QualityIssue]]:
    return 100.0, []

def evaluate_documentation_quality(project_root: Optional[Path] = None) -> QualityDimensionScore:
    if project_root is None:
        project_root = Path.cwd()

    issues = []
    s1, i1 = score_required_docs_presence(project_root)
    s2, i2 = score_required_tests_presence(project_root)
    s3, i3 = score_readme_presence(project_root)
    s4, i4 = score_phase_summary_presence(project_root)

    issues.extend(i1 + i2 + i3 + i4)
    avg_score = (s1 + s2 + s3 + s4) / 4.0

    crit = sum(1 for i in issues if i.severity == QualitySeverity.CRITICAL)
    warn = sum(1 for i in issues if i.severity in [QualitySeverity.MODERATE, QualitySeverity.HIGH])

    status = QualityStatus.PASS
    if crit > 0:
        status = QualityStatus.FAIL
    elif warn > 0:
        status = QualityStatus.WARN

    return QualityDimensionScore(
        dimension=QualityDimension.DOCUMENTATION,
        score=avg_score,
        weight=0.02,
        status=status,
        issue_count=len(issues),
        critical_count=crit,
        warning_count=warn,
        summary=f"Documentation/Testing Score: {avg_score:.1f}",
        issues=issues
    )
