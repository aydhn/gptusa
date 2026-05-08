# Maintenance Workflow

The system establishes daily, weekly, monthly, and pre-release maintenance workflows.

Tasks can be validated without destructive or side-effect executions. Broker integration is explicitly avoided.

## Frequencies
- **Daily**: Validates config, tests health, checks locks and scan status.
- **Weekly**: Runs regression tests, evaluates acceptance metrics, backs up reports.
- **Monthly**: Full rehearsal tests, validates backups and configs.
- **Pre-Release**: Executes release rehearsal on golden samples and generates a local release bundle.

## Execution
```bash
python -m usa_signal_bot maintenance-check --frequency daily --write
python -m usa_signal_bot maintenance-check --frequency weekly --write
```
