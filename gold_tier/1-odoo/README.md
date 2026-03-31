# Odoo Integration

## Requirements
- Odoo Community (self-hosted, local)
- MCP server for JSON-RPC API integration
- Odoo 19+ compatibility

## Architecture

```
Claude Code ←→ MCP Server ←→ Odoo Community (JSON-RPC)
```

## Status
🚧 Not Started

## Files
- [ ] `odoo_mcp_server.py` - Main MCP server
- [ ] `odoo_config.yaml` - Configuration
- [ ] `models/` - Odoo models reference

## Next Steps
1. Set up Odoo Community locally
2. Create MCP server with JSON-RPC client
3. Define tools for:
   - Create invoice
   - Get accounting data
   - Add journal entry
   - Generate reports

---

*Odoo Integration | Gold Tier*
