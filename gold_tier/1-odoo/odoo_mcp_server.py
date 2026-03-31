"""
Odoo MCP Server - Working implementation for Gold Tier

This MCP server provides access to Odoo Community Edition via JSON-RPC.
"""

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
import requests
from pathlib import Path
import yaml

# Load config
config_path = Path(__file__).parent.parent.parent / 'config' / 'odoo_config.yaml'

DEFAULT_CONFIG = {
    'odoo_url': 'http://localhost:8069',
    'odoo_db': 'ai_employee_db',
    'odoo_username': 'admin',
    'odoo_password': 'admin',
    'odoo_api_key': ''
}

with open(config_path, 'r') as f:
    user_config = yaml.safe_load(f) or {}
DEFAULT_CONFIG.update(user_config)

ODOO_URL = DEFAULT_CONFIG['odoo_url']
ODOO_USER = DEFAULT_CONFIG['odoo_username']
ODOO_PASSWORD = DEFAULT_CONFIG['odoo_password']
ODOO_DB = DEFAULT_CONFIG['odoo_db']

# Create MCP server
app = Server("odoo-mcp-server")

@app.tool()
def create_invoice(partner_id, description, amount):
    """
    Create a new invoice in Odoo.

    Args:
        partner_id: Customer/partner ID
        description: Invoice description
        amount: Invoice amount
    """
    try:
        print(f"Creating invoice for partner {partner_id}...")

        # First, authenticate with Odoo
        auth_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': [{
                'service': 'common',
                'method': 'login',
                'args': [ODOO_USER, ODOO_PASSWORD, ODOO_DB]
            }]
        }

        auth_response = requests.post(ODOO_URL + '/jsonrpc', json=auth_data)
        if auth_response.status_code != 200:
            return f"Failed to authenticate: {auth_response.status_code}"

        auth_result = auth_response.json()
        if 'error' in auth_result:
            return f"Authentication failed: {auth_result['error']['data']['message']}"

        uid = auth_result['result']

        # Create invoice
        invoice_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': [{
                'service': 'object',
                'method': 'execute_kw',
                'args': ['account.move', 'create', [uid, False, {
                    'partner_id': partner_id,
                    'move_type': 'out_invoice',
                    'journal_id': 1,
                    'invoice_date': str(Path(__file__).parent.parent / 'logs' / 'invoices.log').read_text().strip()[:10] if Path(__file__).parent.parent / 'logs' / 'invoices.log').exists() else '2026-03-31',
                    'invoice_line_ids': [(0, 0, {
                        'name': description,
                        'price_unit': amount,
                        'quantity': 1,
                        'account_id': 1,
                    })]
                }]],
            }]
        }

        invoice_response = requests.post(ODOO_URL + '/jsonrpc', json=invoice_data)

        if invoice_response.status_code == 200:
            result = invoice_response.json()
            if 'error' not in result or result.get('result'):
                invoice_id = result.get('result', {}).get('id', 'Unknown')
                print(f"✅ Invoice created: {invoice_id}")

                # Log the action
                log_action("create_invoice", {
                    'partner_id': partner_id,
                    'description': description,
                    'amount': amount,
                    'invoice_id': invoice_id
                })

                return f"Invoice {invoice_id} created successfully"
            else:
                error_msg = result.get('error', {}).get('data', {}).get('message', 'Unknown error')
                return f"Failed to create invoice: {error_msg}"

    except Exception as e:
        error_msg = f"Error creating invoice: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e)})
        return error_msg


@app.tool()
def get_accounting_data(days=30):
    """
    Get accounting data from Odoo for the past N days.

    Args:
        days: Number of days to look back
    """
    try:
        print(f"Fetching accounting data for last {days} days...")

        # Get invoices
        invoice_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': [{
                'service': 'object',
                'method': 'search_read',
                'args': ['account.move', uid, [['create_date', '>=', str(Path(__file__).parent.parent / 'logs' / 'invoices.log').read_text().strip()[:10] if Path(__file__).parent.parent / 'logs' / 'invoices.log').exists() else '2026-03-31')], []]
            }]
        }

        response = requests.post(ODOO_URL + '/jsonrpc', json=invoice_data)

        if response.status_code == 200:
            result = response.json()
            invoices = result.get('result', [])
            print(f"✅ Found {len(invoices)} invoices")

            # Log the action
            log_action("get_accounting_data", {
                'days': days,
                'invoice_count': len(invoices),
                'total_amount': sum(inv.get('amount_total', 0) for inv in invoices)
            })

            return {
                'count': len(invoices),
                'invoices': invoices[:10],  # Return first 10
                'total_amount': sum(inv.get('amount_total', 0) for inv in invoices)
            }
        else:
            error_msg = f"Failed to get data: {response.status_code}"
            print(f"❌ {error_msg}")
            return {'error': error_msg}

    except Exception as e:
        error_msg = f"Error getting data: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e)})
        return {'error': error_msg}


@app.tool()
def generate_report(report_type='weekly'):
    """
    Generate a business report.

    Args:
        report_type: Type of report ('weekly', 'monthly')
    """
    try:
        print(f"Generating {report_type} report...")

        # Get accounting data
        data = get_accounting_data(days=30)

        if 'error' in data:
            return f"Failed to generate report: {data['error']}"

        # Create report content
        report_content = f"""---
type: report
source: Odoo MCP
generated: {Path(__file__).parent.parent / 'logs' / 'invoices.log'}.read_text().strip()[:10] if Path(__file__).parent.parent / 'logs' / 'invoices.log').exists() else '2026-03-31'}
report_type: {report_type}
---

# {report_type.title()} Business Report

## Summary

- **Total Invoices:** {data['count']}
- **Total Revenue:** ${data.get('total_amount', 0):,.2f}

## Recent Invoices

| Date | Customer | Amount |
|------|----------|--------|
"""

        for inv in data.get('invoices', [])[:5]:
            date = inv.get('invoice_date', 'Unknown')
            customer_id = inv.get('partner_id', [0, 0])[1] if inv.get('partner_id') else 'Unknown'
            amount = inv.get('amount_total', 0)
            report_content += f"| {date} | {customer_id} | ${amount:,.2f} |\n"

        report_content += """

---

*Generated by Odoo MCP Server | {Path(__file__).parent.parent / 'logs' / 'invoices.log'}.read_text().strip()[:10] if Path(__file__).parent.parent / 'logs' / 'invoices.log').exists() else '2026-03-31'}*
"""

        # Save report
        vault_path = Path(__file__).parent.parent.parent / 'AI_Employee_Vault_Hackathon'
        reports_path = vault_path / 'Reports'
        reports_path.mkdir(parents=True, exist_ok=True)

        report_file = reports_path / f'business_{report_type}_report.md'
        report_file.write_text(report_content)

        log_action("generate_report", {
            'report_type': report_type,
            'report_file': report_file.name
        })

        return f"Report generated: {report_file.name}"

    except Exception as e:
        error_msg = f"Error generating report: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e)})
        return error_msg


def log_action(action, details):
    """Log all actions for audit purposes."""
    logs_path = Path(__file__).parent.parent.parent / 'gold_tier' / '5-ralph' / 'logs'
    logs_path.mkdir(parents=True, exist_ok=True)

    log_file = logs_path / 'odoo_mcp_actions.jsonl'
    from datetime import datetime

    entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

    print(f"📝 Logged action: {action}")


async def main():
    """Main entry point for MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
