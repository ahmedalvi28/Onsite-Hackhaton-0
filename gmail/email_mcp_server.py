"""
Email MCP Server - Model Context Protocol server for sending emails.

This server provides tools for Claude Code to send emails via SMTP.

Usage:
    python email_mcp_server.py --port 3000
"""

import argparse
import asyncio
import json
import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Optional, List, Dict, Any
import yaml

# MCP Server imports (if using the official MCP SDK)
# For this implementation, we'll use a simple HTTP server
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class EmailSender:
    """Handles email sending via SMTP."""

    def __init__(self, config_path: str = 'config/email_config.yaml'):
        """
        Initialize Email Sender.

        Args:
            config_path: Path to email configuration file
        """
        self.config = self._load_config(config_path)
        self.vault_path = Path('C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon')
        self.logs = self.vault_path / 'Logs'
        self.logs.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        default_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_username': '',
            'smtp_password': '',
            'use_tls': True,
            'from_email': '',
            'from_name': 'Personal AI Employee',
            'templates_path': 'templates/emails',
        }

        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
            default_config.update(user_config)

        return default_config

    def validate_config(self) -> tuple[bool, str]:
        """
        Validate email configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.config.get('smtp_server'):
            return False, "SMTP server not configured"

        if not self.config.get('smtp_username'):
            return False, "SMTP username not configured"

        if not self.config.get('smtp_password'):
            return False, "SMTP password not configured"

        if not self.config.get('from_email'):
            return False, "From email not configured"

        return True, ""

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = True,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email.

        Args:
            to: Recipient email address
            subject: Email subject line
            body: Email body
            html: True if body is HTML, False for plain text
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            reply_to: Reply-to address

        Returns:
            Dictionary with success status and message
        """
        # Validate configuration
        is_valid, error = self.validate_config()
        if not is_valid:
            return {
                'success': False,
                'message': f"Configuration error: {error}"
            }

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config['from_name']} <{self.config['from_email']}>"
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = cc
            if reply_to:
                msg['Reply-To'] = reply_to

            # Add body
            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type))

            # Add BCC recipients (they're not in headers)
            recipients = [to]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(',')])
            if bcc:
                recipients.extend([addr.strip() for addr in bcc.split(',')])

            # Send email
            if self.config['use_tls']:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.starttls(context=context)
                    server.login(self.config['smtp_username'], self.config['smtp_password'])
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.login(self.config['smtp_username'], self.config['smtp_password'])
                    server.send_message(msg)

            # Log the sent email
            self._log_email(to, subject, body, cc, bcc)

            return {
                'success': True,
                'message': f"Email sent to {to}",
                'timestamp': datetime.now().isoformat()
            }

        except smtplib.SMTPAuthenticationError as e:
            return {
                'success': False,
                'message': f"Authentication failed: {str(e)}. Check your app password."
            }
        except smtplib.SMTPException as e:
            return {
                'success': False,
                'message': f"SMTP error: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to send email: {str(e)}"
            }

    def send_with_attachments(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: List[str],
        html: bool = True,
        cc: Optional[str] = None,
        bcc: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email with attachments.

        Args:
            to: Recipient email address
            subject: Email subject line
            body: Email body
            attachments: List of file paths to attach
            html: True if body is HTML, False for plain text
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)

        Returns:
            Dictionary with success status and message
        """
        # Validate configuration
        is_valid, error = self.validate_config()
        if not is_valid:
            return {
                'success': False,
                'message': f"Configuration error: {error}"
            }

        try:
            # Create message
            msg = MIMEMultipart('mixed')
            msg['From'] = f"{self.config['from_name']} <{self.config['from_email']}>"
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = cc

            # Create body part
            body_part = MIMEMultipart('alternative')
            content_type = 'html' if html else 'plain'
            body_part.attach(MIMEText(body, content_type))
            msg.attach(body_part)

            # Add attachments
            for file_path in attachments:
                path = Path(file_path)
                if not path.exists():
                    return {
                        'success': False,
                        'message': f"Attachment not found: {file_path}"
                    }

                with open(path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), Name=path.name)
                    attachment['Content-Disposition'] = f'attachment; filename="{path.name}"'
                    msg.attach(attachment)

            # Build recipients list
            recipients = [to]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(',')])
            if bcc:
                recipients.extend([addr.strip() for addr in bcc.split(',')])

            # Send email
            if self.config['use_tls']:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.starttls(context=context)
                    server.login(self.config['smtp_username'], self.config['smtp_password'])
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                    server.login(self.config['smtp_username'], self.config['smtp_password'])
                    server.send_message(msg)

            # Log the sent email
            self._log_email(to, subject, body, cc, bcc, attachments)

            return {
                'success': True,
                'message': f"Email with {len(attachments)} attachment(s) sent to {to}",
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to send email: {str(e)}"
            }

    def send_template(
        self,
        template_name: str,
        to: str,
        data: Dict[str, Any],
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email using a template.

        Args:
            template_name: Name of template file (without .html extension)
            to: Recipient email address
            data: Dictionary of variables to replace in template
            subject: Optional custom subject (extracted from template if not provided)

        Returns:
            Dictionary with success status and message
        """
        template_path = Path(self.config['templates_path']) / f'{template_name}.html'

        if not template_path.exists():
            return {
                'success': False,
                'message': f"Template not found: {template_path}"
            }

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            # Extract subject from template
            if not subject:
                for line in template.split('\n'):
                    if 'subject:' in line.lower():
                        subject = line.split(':', 1)[1].strip()
                        break

            if not subject:
                subject = "Email from Personal AI Employee"

            # Replace variables in template
            for key, value in data.items():
                placeholder = f"{{{key}}}"
                template = template.replace(placeholder, str(value))

            return self.send_email(to, subject, template, html=True)

        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to send template: {str(e)}"
            }

    def _log_email(self, to: str, subject: str, body: str, cc: str = "",
                   bcc: str = "", attachments: List[str] = None):
        """Log sent email to vault."""
        log_file = self.logs / f'email_sent_{datetime.now().strftime("%Y%m%d")}.log'

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attachments_str = f", Attachments: {attachments}" if attachments else ""

        log_entry = (
            f"[{timestamp}] TO: {to} | CC: {cc} | BCC: {bcc} | "
            f"SUBJECT: {subject}{attachments_str}\n"
        )

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass


class MCPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP server."""

    def __init__(self, *args, email_sender: EmailSender, **kwargs):
        self.email_sender = email_sender
        super().__init__(*args, **kwargs)

    def _send_json_response(self, data: Dict[str, Any]):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, status: int, message: str):
        """Send error response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': message}).encode())

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/send':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())

                to = data.get('to')
                subject = data.get('subject', '')
                body = data.get('body', '')
                html = data.get('html', True)
                cc = data.get('cc')
                bcc = data.get('bcc')

                if not to or not subject:
                    self._send_error(400, "Missing required fields: to, subject")
                    return

                result = self.email_sender.send_email(to, subject, body, html, cc, bcc)
                self._send_json_response(result)

            except json.JSONDecodeError:
                self._send_error(400, "Invalid JSON")
            except Exception as e:
                self._send_error(500, str(e))

        elif self.path == '/send-template':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())

                template = data.get('template')
                to = data.get('to')
                template_data = data.get('data', {})
                subject = data.get('subject')

                if not template or not to:
                    self._send_error(400, "Missing required fields: template, to")
                    return

                result = self.email_sender.send_template(template, to, template_data, subject)
                self._send_json_response(result)

            except Exception as e:
                self._send_error(500, str(e))

        else:
            self._send_error(404, "Endpoint not found")

    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self._send_json_response({'status': 'healthy'})
        elif self.path == '/':
            self._send_json_response({
                'service': 'Email MCP Server',
                'version': '1.0.0',
                'endpoints': {
                    'POST /send': 'Send an email',
                    'POST /send-template': 'Send email from template',
                    'GET /health': 'Health check'
                }
            })
        else:
            self._send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server(port: int):
    """Run the HTTP server."""
    email_sender = EmailSender()

    # Create handler with email_sender dependency
    def handler(*args, **kwargs):
        return MCPRequestHandler(*args, email_sender=email_sender, **kwargs)

    server = HTTPServer(('localhost', port), handler)
    print(f"📧 Email MCP Server running on http://localhost:{port}")
    print(f"📁 Templates: {email_sender.config['templates_path']}")
    print(f"🔧 From: {email_sender.config['from_name']} <{email_sender.config['from_email']}>")
    print("Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Email MCP Server stopped")
        server.shutdown()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Email MCP Server - Send emails via SMTP')
    parser.add_argument('--port', type=int, default=3000,
                       help='Port to run server on (default: 3000)')
    parser.add_argument('--config', type=str, default='config/email_config.yaml',
                       help='Path to email config (default: config/email_config.yaml)')

    args = parser.parse_args()

    # Check if config exists
    if not Path(args.config).exists():
        print(f"❌ Config file not found: {args.config}")
        print("Please create the config file with your SMTP settings.")
        return

    run_server(args.port)


if __name__ == '__main__':
    main()
