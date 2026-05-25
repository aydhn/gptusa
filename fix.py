with open("phase113_builder.py", "r") as f:
    lines = f.readlines()

with open("phase113_builder.py", "w") as f:
    for line in lines:
        if line.startswith('    provider_governance:'):
            f.write('        provider_governance: ProviderGovernanceConfig = field(default_factory=ProviderGovernanceConfig)\n')
        elif line.startswith('    phase113_governance_policy:'):
            f.write('        phase113_governance_policy: Phase113GovernancePolicyConfig = field(default_factory=Phase113GovernancePolicyConfig)\n')
        elif line.startswith('    phase113_lineage:'):
            f.write('        phase113_lineage: Phase113LineageConfig = field(default_factory=Phase113LineageConfig)\n')
        elif line.startswith('    phase113_audit:'):
            f.write('        phase113_audit: Phase113AuditConfig = field(default_factory=Phase113AuditConfig)\n')
        elif line.startswith('    phase113_notifications:'):
            f.write('        phase113_notifications: Phase113NotificationsConfig = field(default_factory=Phase113NotificationsConfig)\n')
        else:
            f.write(line)
