# n8n Workflow Examples

Real-world examples of workflows you can generate with natural language prompts using the Grok-powered n8n Workflow Builder.

## 📧 Email & Communication

### Daily News Digest
**Prompt**: "Send me an email every morning at 8 AM with top stories from Hacker News"

**Generated Workflow**:
- Schedule Trigger (cron: 0 8 * * *)
- HTTP Request (Hacker News API)
- Function Node (format HTML email)
- Send Email Node

### Slack Alert on Error
**Prompt**: "Monitor my application logs and send Slack alerts when errors occur"

**Generated Workflow**:
- Webhook Trigger (receive log events)
- IF Node (check for error level)
- Slack Node (send notification to #alerts)

### Gmail to Google Sheets
**Prompt**: "When I receive an email with 'invoice' in the subject, extract the data and add it to my Google Sheets"

**Generated Workflow**:
- Gmail Trigger (on new email)
- IF Node (subject contains 'invoice')
- Extract from File (get PDF data)
- Google Sheets (append row)
- Gmail (mark as processed)

## 📊 Data Processing

### API Data Sync
**Prompt**: "Fetch data from my REST API every hour and sync it to PostgreSQL database"

**Generated Workflow**:
- Schedule Trigger (every hour)
- HTTP Request (GET /api/data)
- Function Node (transform data)
- PostgreSQL Node (upsert rows)
- Error Handler (log failures)

### CSV File Processing
**Prompt**: "Watch an FTP folder for new CSV files, process them, and insert data into my database"

**Generated Workflow**:
- FTP Trigger (watch folder)
- Read Binary Files
- Spreadsheet File (parse CSV)
- Function Node (validate & transform)
- PostgreSQL (batch insert)
- FTP (move file to processed/)

### Data Aggregation
**Prompt**: "Aggregate data from 3 different APIs, combine them, and generate a daily report"

**Generated Workflow**:
- Schedule Trigger (daily at midnight)
- HTTP Request 1 (API A)
- HTTP Request 2 (API B)
- HTTP Request 3 (API C)
- Function Node (merge data)
- Google Sheets (update dashboard)
- Email (send report)

## 🔗 Integrations

### Stripe to Salesforce
**Prompt**: "When a new customer subscribes on Stripe, create a lead in Salesforce and send welcome email"

**Generated Workflow**:
- Stripe Trigger (new subscription)
- Salesforce (create lead)
- SendGrid (send welcome email)
- Slack (notify sales team)

### GitHub to Jira
**Prompt**: "When a GitHub issue is created with label 'bug', automatically create a Jira ticket"

**Generated Workflow**:
- GitHub Trigger (issue created)
- IF Node (label = 'bug')
- Jira (create issue)
- GitHub (add comment with Jira link)

### Form Submission Handler
**Prompt**: "Create a webhook that accepts form submissions, validates them, saves to database, and sends confirmation"

**Generated Workflow**:
- Webhook Trigger (POST endpoint)
- Function Node (validate fields)
- PostgreSQL (insert record)
- SendGrid (send confirmation)
- Respond to Webhook (success message)

## 🤖 Automation & Monitoring

### Website Uptime Monitor
**Prompt**: "Check if my website is up every 5 minutes, alert me if it's down"

**Generated Workflow**:
- Schedule Trigger (*/5 * * * *)
- HTTP Request (HEAD request to website)
- IF Node (status code != 200)
- Twilio (send SMS alert)
- PagerDuty (create incident)

### Backup Automation
**Prompt**: "Backup my PostgreSQL database daily and upload to AWS S3"

**Generated Workflow**:
- Schedule Trigger (daily at 2 AM)
- Execute Command (pg_dump)
- AWS S3 (upload file)
- Slack (notify completion)

### Content Publishing
**Prompt**: "When I publish a new blog post on WordPress, share it on Twitter, LinkedIn, and Facebook"

**Generated Workflow**:
- WordPress Trigger (new post)
- Twitter (create tweet with link)
- LinkedIn (create post)
- Facebook (create post)
- Analytics (track shares)

## 💼 Business Workflows

### Lead Qualification
**Prompt**: "Qualify incoming leads based on company size and industry, route to appropriate sales rep"

**Generated Workflow**:
- Webhook Trigger (lead form submission)
- Clearbit Enrichment (get company data)
- IF Node (check company size > 100)
- IF Node (check industry)
- Salesforce (assign to rep)
- Slack (notify rep)
- Email (send to lead)

### Invoice Processing
**Prompt**: "Extract invoice data from email attachments, match with PO numbers, and update accounting system"

**Generated Workflow**:
- Gmail Trigger (new email with attachment)
- IF Node (has PDF attachment)
- Extract from PDF (get invoice data)
- PostgreSQL (lookup PO number)
- QuickBooks (create bill)
- Gmail (send confirmation)

### Customer Onboarding
**Prompt**: "Automate new customer onboarding: create accounts, send welcome materials, schedule kickoff"

**Generated Workflow**:
- Stripe Trigger (new subscription)
- Create User Account (API call)
- SendGrid (welcome email sequence)
- Google Calendar (schedule kickoff)
- Asana (create onboarding tasks)
- Slack (notify success team)

## 🔄 ETL & Data Pipelines

### Real-time Analytics
**Prompt**: "Stream events from Kafka, transform them, and write to ClickHouse for analytics"

**Generated Workflow**:
- Kafka Trigger (consume events)
- Function Node (parse & enrich)
- IF Node (filter relevant events)
- ClickHouse (batch insert)
- Prometheus (update metrics)

### Data Warehouse Sync
**Prompt**: "Sync data from multiple sources to Snowflake data warehouse nightly"

**Generated Workflow**:
- Schedule Trigger (daily at 3 AM)
- HTTP Request (SaaS API)
- PostgreSQL (read updates)
- Google Sheets (fetch data)
- Function Node (transform & merge)
- Snowflake (upsert data)
- Slack (send summary)

## 🛠️ DevOps

### CI/CD Webhook Handler
**Prompt**: "Handle GitHub webhooks for CI/CD: run tests, build Docker image, deploy to Kubernetes"

**Generated Workflow**:
- Webhook Trigger (GitHub push)
- IF Node (branch = main)
- Execute Command (run tests)
- Docker (build image)
- Docker Registry (push image)
- Kubernetes (update deployment)
- Slack (notify team)

### Infrastructure Monitoring
**Prompt**: "Monitor AWS EC2 instances, alert if CPU > 80% or disk > 90%"

**Generated Workflow**:
- Schedule Trigger (every minute)
- AWS CloudWatch (get metrics)
- Function Node (check thresholds)
- IF Node (alert conditions)
- PagerDuty (create alert)
- Slack (notify #ops)

## 📱 Social Media

### Social Media Scheduler
**Prompt**: "Schedule and publish content to Twitter, LinkedIn, and Instagram simultaneously"

**Generated Workflow**:
- Schedule Trigger (from calendar)
- Google Sheets (read content calendar)
- Function Node (format for each platform)
- Twitter (post tweet)
- LinkedIn (create post)
- Instagram (via API)
- Airtable (mark as published)

### Social Listening
**Prompt**: "Monitor Twitter for mentions of my brand, analyze sentiment, and route to support if negative"

**Generated Workflow**:
- Twitter Trigger (search mentions)
- OpenAI (sentiment analysis)
- IF Node (sentiment < 0.3)
- Zendesk (create ticket)
- Slack (alert support team)

## 🎓 Advanced Examples

### Multi-Step Approval Workflow
**Prompt**: "Create expense approval workflow: submit → manager review → finance approval → reimburse"

**Generated Workflow**:
- Webhook Trigger (expense submission)
- Slack (send to manager for approval)
- Wait for Webhook (manager response)
- IF Node (approved)
- Slack (send to finance)
- Wait for Webhook (finance approval)
- QuickBooks (create reimbursement)
- Email (notify employee)

### AI-Powered Content Moderation
**Prompt**: "Moderate user-generated content using AI, flag inappropriate items, and notify moderators"

**Generated Workflow**:
- Webhook Trigger (new content)
- OpenAI (analyze content)
- IF Node (inappropriate detected)
- PostgreSQL (flag content)
- Slack (notify moderators)
- Respond to Webhook (status)

### Dynamic Workflow Orchestration
**Prompt**: "Process different types of documents based on their type: invoices, receipts, contracts"

**Generated Workflow**:
- Webhook Trigger (document upload)
- OpenAI (classify document type)
- Switch Node (route by type)
  - Case 1: Invoice → Extract → QuickBooks
  - Case 2: Receipt → OCR → Expense system
  - Case 3: Contract → DocuSign → Legal system
- PostgreSQL (log processing)
- Respond to Webhook (result)

## 💡 Pro Tips

### 1. Be Specific with Timing
- ✅ "Every weekday at 9 AM EST"
- ✅ "Every hour between 8 AM and 6 PM"
- ❌ "Regularly"

### 2. Specify Data Formats
- ✅ "Parse JSON response and extract 'email' field"
- ✅ "Convert CSV to JSON objects"
- ❌ "Process the data"

### 3. Include Error Handling
- ✅ "If API call fails, retry 3 times then alert me"
- ✅ "On error, log to file and send Slack notification"
- ❌ Just describing happy path

### 4. Mention Credentials Needed
- ✅ "Use my Gmail account to send emails"
- ✅ "Connect to PostgreSQL database 'production'"
- This helps Grok configure authentication correctly

### 5. Define Success Criteria
- ✅ "Send confirmation when all steps complete successfully"
- ✅ "Update status field to 'processed' when done"

## 🔧 Iterative Refinement

After generating a workflow, you can refine it through chat:

```
Initial: "Send daily email with weather"

Refinements:
- "Add temperature threshold - only send if below 50°F"
- "Include 7-day forecast in addition to today"
- "Add error handling to retry if weather API is down"
- "Change time from 8 AM to 7 AM"
```

## 📚 Learning Resources

- **n8n Node Library**: https://n8n.io/integrations
- **Workflow Templates**: https://n8n.io/workflows
- **Community Forum**: https://community.n8n.io

## 🎯 Next Steps

1. Try these examples in your workflow builder
2. Modify them for your specific needs
3. Combine multiple patterns
4. Share your creations with the community!

Happy automating! 🚀
