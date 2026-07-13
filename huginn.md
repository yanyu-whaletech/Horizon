---
layout: default
title: Huginn Integration
---

# Huginn Integration

[Huginn](https://github.com/huginn/huginn) complements Horizon when you need a
source or delivery integration that Horizon does not provide. Keep Horizon in
charge of news deduplication, AI scoring, enrichment, and summarization; use
Huginn for event collection, deterministic transformations, and downstream
automation.

Huginn requires its own continuously running deployment. It is entirely
optional and is not part of Horizon's recommended GitHub Actions setup. If you
do not have a server, use Huginn as a source of design ideas and run Horizon
solely through `.github/workflows/daily-summary.yml`.

```text
Huginn watchers/transforms
        ↓
Data Output Agent (RSS)
        ↓
Horizon RSS → score → enrich → summarize
        ↓
Horizon webhook
        ↓
Huginn Webhook Agent → actions and deliveries
```

## Feed Huginn events into Horizon

1. In Huginn, connect the desired watcher and transformation agents to a
   [Data Output Agent](https://github.com/huginn/huginn/blob/master/app/models/agents/data_output_agent.rb).
2. Configure the output as RSS. Map at least `title`, `link`, `description`, and
   `pubDate` so Horizon receives normal news-item fields.
3. Give the Data Output Agent a strong, unique secret.
4. Store the full authenticated feed URL in Horizon's `.env` rather than in the
   checked-in JSON configuration:

   ```dotenv
   HUGINN_FEED_URL=https://huginn.example/users/1/web_requests/42/long-random-secret.xml
   ```

5. Add the feed to `data/config.json`:

   ```jsonc
   {
     "sources": {
       "rss": [
         {
           "name": "Huginn bridge",
           "url": "${HUGINN_FEED_URL}",
           "enabled": true,
           "category": "huginn"
         }
       ]
     }
   }
   ```

The feed secret is lightweight authentication and appears in the URL. Do not
publish it in logs, screenshots, generated pages, or version control. Use HTTPS
and rotate the secret if it is exposed.

## Send Horizon results into Huginn

1. Create a Huginn
   [Webhook Agent](https://github.com/huginn/huginn/blob/master/app/models/agents/webhook_agent.rb)
   with a strong secret and `payload_path` set to `.`.
2. Connect it to the Huginn trigger, formatting, buffering, or delivery agents
   you need.
3. Put its URL in Horizon's `.env`:

   ```dotenv
   HORIZON_WEBHOOK_URL=https://huginn.example/users/1/web_requests/84/another-long-secret
   ```

4. Enable Horizon's generic webhook in `data/config.json`:

   ```jsonc
   {
     "webhook": {
       "enabled": true,
       "url_env": "HORIZON_WEBHOOK_URL",
       "delivery": "summary",
       "platform": "generic",
       "layout": "markdown",
       "request_body": {
         "title": "#{message_title}",
         "summary": "#{summary}",
         "important_items": "#{important_items}",
         "all_items": "#{all_items}",
         "date": "#{date}"
       },
       "headers": "Content-Type: application/json"
     }
   }
   ```

Use Horizon's `horizon-webhook` preview/test command before relying on the
route for production notifications.

## Keep GitHub Actions as the schedule owner

When Huginn is available on a separate hosted deployment, let it maintain the
input feeds and route completed summaries while GitHub Actions runs the Horizon
pipeline. Do not ask Huginn to launch Horizon too, or briefings may be duplicated.

Huginn can execute shell commands, but giving an automation service arbitrary
host command access substantially increases risk. A feed/webhook boundary is
usually easier to secure and operate.

## Operational checks

- Confirm the Huginn Data Output Agent is receiving events within its expected
  period.
- Check Horizon run metadata for `source_health.rss`, stage status, and stage
  duration.
- Treat an RSS fetch with `status: succeeded` and `item_count: 0` as a valid
  empty result, not a scraper failure.
- Keep Huginn and Horizon secrets in environment variables and back up their
  state directories separately.
