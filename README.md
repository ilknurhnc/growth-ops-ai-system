# Growth Automation & AI Ops Challenge

## Project Overview

This project demonstrates a lightweight AI-powered outbound growth system designed for Konuşarak Öğren.

The goal is to identify HR professionals in Turkey, enrich lead information using AI, generate personalized outreach messages, and manage the outreach process through an automated workflow.

Instead of focusing only on lead collection, the project aims to show an end-to-end growth automation mindset including:

* Lead discovery
* Data enrichment
* AI-powered personalization
* Lead scoring
* CRM organization
* Workflow automation

---

## Problem Statement

Konuşarak Öğren wants to reach Human Resources professionals in Turkey through LinkedIn and email outreach.

The main challenges are:

* Finding relevant decision makers
* Understanding company context
* Personalizing outreach at scale
* Prioritizing high-value leads
* Managing outreach efficiently

This project provides a minimum viable solution for these challenges.

---

## Solution Architecture

Lead Source → Data Cleaning → AI Enrichment → Lead Scoring → Personalized Outreach → CRM

The workflow collects HR professionals, enriches lead data using AI, generates personalized messages, and stores the results in a CRM-ready format.

---

## Tech Stack

* Python
* OpenAI API
* Google Sheets
* n8n
* Apollo.io
* Pandas

---

## Workflow

### Step 1: Lead Collection

HR professionals are collected from Apollo using filters such as:

* HR Manager
* HR Director
* Talent Acquisition Manager
* HR Business Partner
* Learning & Development Manager

Collected fields:

* Full Name
* Company
* Job Title
* LinkedIn URL
* Email (if available)

Target dataset size: 100 leads

### Step 2: Lead Enrichment

Each lead is processed through an AI enrichment workflow.

The AI estimates:

* Company industry
* Company size
* English training need score
* Potential HR challenges
* Outreach angle

This creates additional context for personalized communication.

### Step 3: Lead Scoring

Leads are scored based on:

* Company size
* Decision-making authority
* Estimated English learning demand

This helps prioritize outreach efforts.

### Step 4: Personalized Outreach

AI generates customized LinkedIn messages or cold emails based on:

* Role
* Company context
* Estimated pain points
* Outreach angle

The goal is to avoid generic outreach and improve response rates.

### Step 5: CRM Management

Processed leads are stored inside Google Sheets.

Pipeline stages:

* New
* Contacted
* Replied
* Meeting Scheduled
* Won
* Lost

### Step 6: Automation

An n8n workflow automates:

1. Lead intake
2. AI enrichment
3. Lead scoring
4. Message generation
5. CRM updates

This reduces manual work and improves scalability.

---

## Sample Output

Example Lead:

Name: Ayşe Yılmaz

Company: ABC Teknoloji

Role: HR Manager

AI Output:

Industry: SaaS

Company Size: 50-200

Pain Point:
Scaling recruitment while maintaining employee development.

Outreach Angle:
Improve spoken English skills for international communication and hiring.

Generated Message:

"Merhaba Ayşe Hanım,

ABC Teknoloji'nin büyüyen ekip yapısını inceledim. Uluslararası iletişim ve işe alım süreçlerinde İngilizce gelişiminin önemli bir rol oynayabileceğini düşündüm.

Konuşarak Öğren'in bu konuda sağladığı bazı sonuçları paylaşmak isterim."

---

## Future Improvements

* LinkedIn automation
* Multi-step outreach sequences
* AI reply classification
* Lead intent detection
* CRM integration (HubSpot)
* Inbox automation
* Deliverability monitoring
* Advanced lead scoring
* Agent-based prospect research

---

## Conclusion

This project demonstrates how AI and automation can be combined to build a scalable outbound growth system.

The focus is not only on generating leads but on creating a repeatable workflow that improves personalization, prioritization, and execution efficiency.

## AI Strategy

To keep the prototype lightweight and cost-efficient, a rule-based enrichment engine was implemented instead of using a paid LLM API.

The enrichment layer simulates AI reasoning by analyzing job titles and assigning:

* Estimated English training demand
* Potential HR pain points
* Outreach angles
* Lead qualification signals

This approach allows rapid prototyping while keeping the architecture fully compatible with future LLM integration.

The enrichment module can be replaced with:

* OpenAI GPT
* Claude
* Gemini
* Local LLMs

without changing downstream components such as lead scoring, CRM updates, or outreach generation.

## Lead Qualification Logic

The lead scoring system prioritizes prospects based on three factors:

1. Estimated English learning demand
2. Job title authority
3. Company size

Scoring helps identify the highest-value prospects before outreach.

Example:

* HR Director → Higher priority
* HR Manager → Medium-high priority
* Recruitment Specialist → Medium priority

This allows outreach efforts to focus on leads with the highest potential impact.
