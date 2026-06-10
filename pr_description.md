🧪 [Testing Improvement] Add error path tests for validate_research_workflow_review_report

🎯 **What:** The testing gap addressed
The `validate_research_workflow_review_report` function in `usa_signal_bot/research_workflow/workflow_validation.py` contained a `try/except` block where the `except` block mapping a `ResearchWorkflowValidationError` to a report with `ERROR` severity was not covered by any test. Also added the missing enums and exceptions that were preventing imports to actually run this specific test file.

📊 **Coverage:** What scenarios are now tested
- The happy path when validation passes with no exceptions.
- The error path when `validate_research_workflow_review` raises a `ResearchWorkflowValidationError`, verifying that the exception string correctly maps to a `ResearchWorkflowValidationIssue` with severity set to `"ERROR"`.

✨ **Result:** The improvement in test coverage
Test coverage is increased and we verify the proper handling and mapping of validation errors. The test module is now actually executable.
