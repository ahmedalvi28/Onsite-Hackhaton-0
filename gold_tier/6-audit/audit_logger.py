"""
Audit System - Comprehensive logging for all system actions
Tracks all actions across different components for audit purposes.
"""

import json
from datetime import datetime
from pathlib import Path


class AuditLogger:
    """Logs all system actions for Gold Tier audit requirements."""

    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.audit_logs_path = self.vault_path / 'Logs' / 'Audit'
        self.audit_logs_path.mkdir(parents=True, exist_ok=True)

    def log_action(self, component, action, details=None, status='success'):
        """
        Log an action with full details.

        Args:
            component: System component (ralph_loop, odoo_mcp, social_mcp, etc.)
            action: Action performed
            details: Additional details
            status: Success or failure status
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'action': action,
            'details': details or {},
            'status': status
        }

        # Append to appropriate log file
        log_file = self.audit_logs_path / f"{component}_audit.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

        print(f"📝 [{component.upper()}] {action}: {status}")

    def get_error_rate(self, component, hours=24):
        """
        Get error rate for a component over time period.

        Args:
            component: Component name
            hours: Time period in hours
        """
        log_file = self.audit_logs_path / f"{component}_audit.jsonl"

        if not log_file.exists():
            return {
                'total_actions': 0,
                'errors': 0,
                'error_rate': 0
            }

        errors = 0
        total_actions = 0

        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    total_actions += 1

                    timestamp = datetime.fromisoformat(entry.get('timestamp', '')).timestamp()
                    if timestamp >= cutoff_time:
                        if entry.get('status') == 'failed':
                            errors += 1
                except:
                    pass

        error_rate = (errors / total_actions * 100) if total_actions > 0 else 0

        return {
            'total_actions': total_actions,
            'errors': errors,
            'error_rate': error_rate
        }

    def generate_weekly_report(self):
        """
        Generate a comprehensive weekly audit report.
        """
        components = ['ralph_loop', 'odoo_mcp', 'social_mcp', 'linkedin', 'gmail']

        report_content = f"""---
type: weekly_audit
generated: {datetime.now().isoformat()}
---

# Weekly System Audit Report

**Period:** {(datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

| Component | Total Actions | Errors | Error Rate | Status |
|-----------|---------------|--------|-------------|--------|
"""

        all_good = True
        for component in components:
            stats = self.get_error_rate(component, hours=168)  # 7 days
            status_icon = "✅" if stats['error_rate'] < 5 else "⚠️"
            all_good = all_good and stats['error_rate'] < 5

            report_content += f"| {component} | {stats['total_actions']} | {stats['errors']} | {stats['error_rate']:.1f}% | {status_icon} |\n"

        overall_status = "🟢 All Systems Healthy" if all_good else "🟡 Some Issues Detected"

        report_content += f"""

Overall Status: {overall_status}

---

## Component Details

"""

        for component in components:
            report_content += f"\n### {component.upper()}\n\n"
            stats = self.get_error_rate(component, hours=168)

            report_content += f"- **Total Actions:** {stats['total_actions']}\n"
            report_content += f"- **Errors:** {stats['errors']}\n"
            report_content += f"- **Error Rate:** {stats['error_rate']:.1f}%\n"

            # Get recent errors
            log_file = self.audit_logs_path / f"{component}_audit.jsonl"
            if log_file.exists():
                report_content += "\n**Recent Errors:**\n\n"

                with open(log_file, 'r') as f:
                    lines = f.readlines()[-10:]  # Last 10 entries
                    for line in lines:
                        try:
                            entry = json.loads(line)
                            if entry.get('status') == 'failed':
                                timestamp = entry.get('timestamp', 'Unknown')
                                action = entry.get('action', 'Unknown')
                                report_content += f"- {timestamp}: {action}\n"
                        except:
                            pass

            report_content += "\n---\n"

        # Save report
        vault_reports = self.vault_path / 'Reports'
        vault_reports.mkdir(parents=True, exist_ok=True)

        report_file = vault_reports / f'weekly_audit_{datetime.now().strftime("%Y%m%d")}.md'
        report_file.write_text(report_content)

        print(f"✅ Weekly audit report: {report_file.name}")

        return report_file.name


def main():
    """Main entry point."""
    vault_path = 'C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon'

    logger = AuditLogger(vault_path)

    # Log startup
    logger.log_action('audit_system', {'action': 'startup'})

    # Generate weekly report
    report_file = logger.generate_weekly_report()

    print(f"\n📊 Weekly audit report generated: {report_file}")
    print(f"\n💡 Check vault: {vault_path}/Reports/")


if __name__ == '__main__':
    main()
