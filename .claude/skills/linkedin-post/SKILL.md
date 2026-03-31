---
description: Automatically post business content on LinkedIn to generate sales
---

# LinkedIn Post Skill

## Description
Creates and posts engaging business content on LinkedIn to generate leads and sales.

## Usage
Use this skill when:
- You need to post business content on LinkedIn
- Sharing company updates, product announcements, or industry insights
- Promoting services or generating sales leads

## Parameters
- `topic`: The main topic or theme for the post
- `type`: Post type (insight, announcement, promotion, story, tip)
- `tone`: Tone of voice (professional, casual, enthusiastic, authoritative)
- `include_image`: Whether to include an image URL (optional)

## Expected Actions

1. **Generate compelling content** based on topic and type
2. **Structure the post** for LinkedIn engagement:
   - Hook (first line)
   - Value/content body
   - CTA (call to action)
   - Relevant hashtags

3. **For sensitive posts**, require approval via approve-task skill
4. **For routine posts**, can post directly after confirmation

## Post Templates

### Insight Post
```markdown
🎯 [Attention-grabbing headline]

[3-4 sentences of valuable insight]

Here's what I've learned:
• Point 1
• Point 2
• Point 3

[Closing thought or question]

What's your experience? Share in the comments 👇

#LinkedIn #Business #[Topic]
```

### Announcement Post
```markdown
🚀 BIG ANNOUNCEMENT 🚀

[Exciting news about company, product, or service]

What this means for you:
• Benefit 1
• Benefit 2

[CTA - Learn more, sign up, etc.]

#Launch #[Product] #[Industry]
```

### Promotion Post
```markdown
💡 Struggling with [Pain Point]?

Our [Solution] helps you:
✅ [Benefit 1]
✅ [Benefit 2]
✅ [Benefit 3]

[Social proof - testimonial, stat, or result]

Ready to transform your [area]? 

[CTA with link]

#Business #[Industry] #Growth
```

## Business Topics
When topic isn't specified, rotate through:
- Industry trends and predictions
- Problem-solving tips
- Success stories/case studies
- Behind-the-scenes insights
- Thought leadership pieces
- Product/service benefits

## Approval Required

Always require approval for:
- Promotional posts with pricing
- Major announcements
- Controversial opinions
- Content that mentions specific people or companies

## Example Usage

User: /linkedin-post topic="AI productivity tips" type=insight tone=professional

Response: "Generated LinkedIn post about AI productivity tips. Ready for approval before posting."

---
*This skill requires LinkedIn API access configured in config/linkedin_config.yaml*
