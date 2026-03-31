# API Documentation

## Overview

This document describes all APIs used in the Personal AI Employee system, including internal MCP servers and external service integrations.

---

## Internal MCP Servers

### Email MCP Server

**Port:** 3000
**Base URL:** `http://localhost:3000`

#### Endpoints

##### Send Email
```http
POST /email/send
Content-Type: application/json

{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content",
  "html": false
}
```

**Response:**
```json
{
  "status": "success",
  "message_id": "1234567890"
}
```

##### Get Unread Emails
```http
GET /email/unread?limit=10
```

**Response:**
```json
{
  "emails": [
    {
      "id": "123",
      "from": "sender@example.com",
      "subject": "Subject",
      "body": "Content",
      "timestamp": "2026-03-31T10:00:00Z"
    }
  ],
  "count": 5
}
```

##### Search Emails
```http
GET /email/search?q=keyword&limit=20
```

**Response:**
```json
{
  "emails": [...],
  "count": 10
}
```

---

### LinkedIn MCP Server

**Port:** 3001
**Base URL:** `http://localhost:3001`

#### Endpoints

##### Create Post
```http
POST /linkedin/post
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>

{
  "content": "Post content with hashtags",
  "visibility": "PUBLIC"
}
```

**Response:**
```json
{
  "status": "success",
  "post_id": "urn:li:ugcPost:123456789",
  "url": "https://linkedin.com/posts/..."
}
```

##### Get Profile Info
```http
GET /linkedin/profile
Authorization: Bearer <ACCESS_TOKEN>
```

**Response:**
```json
{
  "id": "urn:li:person:123",
  "name": "John Doe",
  "headline": "Software Engineer",
  "url": "https://linkedin.com/in/johndoe"
}
```

##### Get Engagement Metrics
```http
GET /linkedin/metrics?post_id=urn:li:ugcPost:123456789
Authorization: Bearer <ACCESS_TOKEN>
```

**Response:**
```json
{
  "post_id": "urn:li:ugcPost:123456789",
  "likes": 42,
  "comments": 5,
  "shares": 2,
  "impressions": 500
}
```

---

### WhatsApp MCP Server

**Port:** 3002
**Base URL:** `http://localhost:3002`

#### Endpoints

##### Send Message
```http
POST /whatsapp/send
Content-Type: application/json

{
  "to": "+1234567890",
  "message": "Message content"
}
```

**Response:**
```json
{
  "status": "sent",
  "message_id": "wa_abc123"
}
```

##### Get Messages
```http
GET /whatsapp/messages?limit=20
```

**Response:**
```json
{
  "messages": [
    {
      "id": "wa_abc123",
      "from": "+1234567890",
      "to": "+0987654321",
      "message": "Hello",
      "timestamp": "2026-03-31T10:00:00Z"
    }
  ],
  "count": 5
}
```

---

### Odoo MCP Server

**Port:** 3003
**Base URL:** `http://localhost:3003`

#### Endpoints

##### Create Invoice
```http
POST /odoo/invoice
Content-Type: application/json

{
  "partner_id": 1,
  "invoice_line_ids": [
    {
      "product_id": 10,
      "quantity": 2,
      "price_unit": 100.00
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "invoice_id": 123
}
```

##### Get Accounting Data
```http
GET /odoo/accounting?from=2026-03-01&to=2026-03-31
```

**Response:**
```json
{
  "invoices": [...],
  "payments": [...],
  "revenue": 5000.00,
  "expenses": 3000.00
}
```

##### Create Journal Entry
```http
POST /odoo/journal-entry
Content-Type: application/json

{
  "date": "2026-03-31",
  "line_ids": [
    {
      "account_id": 10,
      "debit": 100.00,
      "credit": 0.00
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "entry_id": 456
}
```

---

### Social MCP Server

**Port:** 3004
**Base URL:** `http://localhost:3004`

#### Endpoints

##### Post to Facebook
```http
POST /social/facebook/post
Content-Type: application/json

{
  "content": "Post content",
  "page_id": "page_123"
}
```

##### Post to Instagram
```http
POST /social/instagram/post
Content-Type: application/json

{
  "content": "Caption",
  "media_url": "https://example.com/image.jpg"
}
```

##### Post to Twitter
```http
POST /social/twitter/post
Content-Type: application/json

{
  "content": "Tweet content (280 chars max)"
}
```

---

## External APIs

### Gmail API

**Base URL:** `https://www.googleapis.com/gmail/v1`
**Documentation:** https://developers.google.com/gmail/api

#### Authentication

OAuth 2.0 flow with scopes:
- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.send`

#### Key Endpoints

##### Get Messages
```http
GET https://www.googleapis.com/gmail/v1/users/me/messages
Authorization: Bearer <ACCESS_TOKEN>
```

##### Send Message
```http
POST https://www.googleapis.com/gmail/v1/users/me/messages/send
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "raw": "base64-encoded-email"
}
```

---

### LinkedIn Marketing API

**Base URL:** `https://api.linkedin.com/v2`
**Documentation:** https://learn.microsoft.com/en-us/linkedin/marketing/

#### Authentication

OAuth 2.0 flow with scope:
- `w_member_social`

#### Key Endpoints

##### Create UGC Post
```http
POST https://api.linkedin.com/v2/ugcPosts
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
X-Restli-Protocol-Version: 2.0.0

{
  "author": "urn:li:person:<PERSON_ID>",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Post content"
      },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

##### Get Profile
```http
GET https://api.linkedin.com/v2/me
Authorization: Bearer <ACCESS_TOKEN>
```

---

### WhatsApp Business API

**Base URL:** `https://graph.facebook.com/v19.0`
**Documentation:** https://developers.facebook.com/docs/whatsapp/

#### Authentication

Bearer token from WhatsApp Business API setup.

#### Key Endpoints

##### Send Message
```http
POST https://graph.facebook.com/v19.0/<PHONE_NUMBER_ID>/messages
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "messaging_product": "whatsapp",
  "to": "PHONE_NUMBER",
  "type": "text",
  "text": {
    "body": "Message content"
  }
}
```

##### Get Messages
```http
GET https://graph.facebook.com/v19.0/<PHONE_NUMBER_ID>/messages
Authorization: Bearer <ACCESS_TOKEN>
```

---

### Odoo JSON-RPC API

**Base URL:** `http://localhost:8069/jsonrpc`
**Documentation:** https://www.odoo.com/documentation/

#### Authentication

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "common",
    "method": "login",
    "args": ["<DATABASE>", "<USERNAME>", "<PASSWORD>"]
  }
}
```

#### Key Operations

##### Read Records
```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "<DATABASE>",
      "<UID>",
      "<PASSWORD>",
      "<MODEL>",
      "read",
      [[1, 2, 3]]
    ]
  }
}
```

##### Create Record
```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "<DATABASE>",
      "<UID>",
      "<PASSWORD>",
      "<MODEL>",
      "create",
      [{ "field": "value" }]
    ]
  }
}
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional context"
  }
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|--------------|
| `INVALID_REQUEST` | Malformed request | 400 |
| `UNAUTHORIZED` | Invalid or missing credentials | 401 |
| `FORBIDDEN` | Insufficient permissions | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `RATE_LIMITED` | Too many requests | 429 |
| `SERVER_ERROR` | Internal server error | 500 |

### Rate Limiting

All MCP servers implement rate limiting:

- Default: 100 requests per minute
- Per-endpoint limits may apply
- Response headers include rate limit info:
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1711862400
  ```

---

## Authentication

### MCP Server Authentication

Local MCP servers use a shared secret:

```bash
export MCP_SECRET="your-secret-here"
```

Include in request headers:
```http
X-MCP-Secret: your-secret-here
```

### OAuth 2.0 Flow

1. **Authorization Code Flow** (for Gmail, LinkedIn)
   - Redirect user to authorization URL
   - User approves permissions
   - Receive authorization code via callback
   - Exchange code for access token

2. **Client Credentials Flow** (for service accounts)
   - Send client_id and client_secret
   - Receive access token directly
   - No user interaction required

---

## Claude Code Skills API

Skills are invoked via the `/skill-name` command:

```
/skill-name param1=value1 param2=value2
```

### Available Skills

| Skill | Parameters | Description |
|-------|------------|-------------|
| `/process-tasks` | none | Process all pending tasks |
| `/create-plan` | task_id | Create plan for specific task |
| `/update-dashboard` | none | Update dashboard stats |
| `/approve-task` | task_id | Approve completed task |
| `/reject-task` | task_id | Reject task |
| `/archive-done` | none | Archive approved tasks |
| `/linkedin-post` | topic, type, tone | Post to LinkedIn |

---

## Webhook Endpoints

### Task Completion Webhook

```http
POST /webhooks/task-completed
Content-Type: application/json

{
  "task_id": "TASK_ID",
  "status": "completed",
  "result": "Task output"
}
```

### Error Alert Webhook

```http
POST /webhooks/error-alert
Content-Type: application/json

{
  "severity": "critical",
  "service": "linkedin",
  "error": "Failed to post",
  "timestamp": "2026-03-31T10:00:00Z"
}
```

---

## Testing

### Test Endpoints

Each MCP server includes test endpoints:

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-03-31T10:00:00Z"
}
```

---

## Versioning

API versioning follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes, backward compatible

Current versions:
- Email MCP: 1.0.0
- LinkedIn MCP: 1.0.0
- WhatsApp MCP: 1.0.0
- Odoo MCP: 1.0.0
- Social MCP: 1.0.0

---

*API Documentation | Gold Tier*
