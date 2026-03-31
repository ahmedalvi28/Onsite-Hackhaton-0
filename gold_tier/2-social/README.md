# Social Media Integration

## Requirements
- Facebook: Post messages + generate summary
- Instagram: Post messages + generate summary
- Twitter (X): Post messages + generate summary

## Architecture

```
                    Claude Code
                        ↓
              ┌──────────────┐
              │ Social Router   │
              │ (MCP Hub)      │
              └────┬─────┘────┘
                   │
        ┌──────────┴───────────┐
        ↓                      ↓           ↓
    Facebook MCP       Instagram MCP     Twitter MCP
        ↓                       ↓           ↓
    Watcher                Watcher       Watcher
        ↓                       ↓           ↓
    Post + Summary        Post + Summary   Post + Summary
```

## Status
🚧 Not Started

## Files to Create
- [ ] `facebook_mcp_server.py` - FB Graph API integration
- [ ] `instagram_mcp_server.py` - IG Basic Display API
- [ ] `twitter_mcp_server.py` - X API integration
- [ ] `config/social_config.yaml` - All API keys

## Next Steps
1. Get API access tokens for each platform
2. Create MCP servers for each
3. Create unified routing layer
4. Implement watchers
5. Implement summary generation

---

*Social Integration | Gold Tier*
