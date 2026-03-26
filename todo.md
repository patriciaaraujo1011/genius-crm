# Genius CRM - Full Platform Plan v3

## Vision
A unified, scalable CRM platform for personal development brand (Cool Girl Rehab™), expandable to other industries via white-labeling. Goal: Replace Kajabi, Go High Level, Skool, and Stan.

---

## Phase 1: Foundation ✅
- Django project setup with virtual environment
- Contact model with tags & UTM tracking
- Basic opt-in page with email validation
- 5-tag auto-tagging system
- GitHub setup

---

## Phase 2: Funnel System + Payments

### 2.0 Funnel Templates
- [x] Sales page template created (`sales_template_1.html`) ✅
- [x] **Order page template** (`order_template_1.html`) ✅
  - Include countdown timer (under hero, scrolling)
  - Order form with contact fields
  - Order bumps section
  - Product summary sidebar
- [x] **Upsell page template** (`upsell_template_1.html`) ✅
  - Urgency bar
  - Congratulation hero
  - Value stack
  - Final CTA
- [x] **Thank you page template** (`thank_you_template_1.html`) ✅
  - Confirmation badge
  - Order summary
  - Access instructions
  - Next steps timeline
- [ ] Update funnel views to use correct templates
- [ ] ⚠️ DECISION NEEDED: How to manage custom copy/images/videos per funnel page?
  - Option A: Upload full HTML/asset package per page
  - Option B: Admin fields for each element + media uploads
  - Option C: Combination of both

### 2.1 Countdown Timer ✅
- Add `offer_end_date` to Funnel model
- Create reusable JavaScript countdown component
- Display on order page & upsell page
- Per-funnel end date setting

### 2.2 Stripe Integration ✅
- Add Stripe SDK + API keys
- Create Stripe customer on checkout
- Basic Checkout Session (one-time payment)
- Webhook handler for payment confirmation
- Stripe handles abandoned cart recovery automatically

### 2.3 Order Bumps ✅
- Add order bump model to Funnel
- Multiple product options on order page
- Bump price & description display
- Add bump items to Stripe checkout

### 2.4 One-Click Upsell ✅
- Upsell page with countdown timer
- Stripe Payment Intent for upsell (basic)
- "Accept" → process upsell
- "Decline" → continue to thank you

### 2.5 Full Funnel Flow ✅
- Sales page → Order page → Upsell page → Thank you page
- URL routing for each funnel
- Session tracking through funnel
- Template swapping (upload different templates)

---

## Phase 3: Email Marketing (Enhanced)

### 3.1 Models (Enhanced)
- **EmailSequence**: name, trigger, segments, send_window_start, send_window_end, exit_conditions
- **EmailSequenceStep**: sequence, order, subject, content, delay_type, delay_hours, condition_type, condition_action
- **CampaignMetric**: track opens, clicks, bounces per step
- **EmailLog**: per-contact delivery tracking (sent, opened, clicked, bounced)

### 3.2 Triggers
- Opt-in (new contact with tag)
- Tag added/removed
- Purchase
- Manual add

### 3.3 Conditions
- If opened → send next step
- If not opened → send alternative
- If clicked → branch logic
- Exit on: purchase, unsubscribe, bounce

### 3.4 Send Windows
- Set business hours (e.g., Mon-Fri 8am-5pm)
- Queue emails outside hours for next available window

### 3.5 Email Templates
- Brand-styled HTML email templates (welcome, nurture, promotional)
- Template library in admin
- Preview in browser

### 3.6 Broadcasts (Enhanced)
- Segment selection by tag
- Schedule for future date/time
- A/B subject line testing

### 3.7 Analytics
- Open rate, click rate per email
- Per-contact tracking (sent, opened, clicked)
- Revenue attribution per email

### 3.8 SMTP + Queue (Parked - Go-Live)
- Configure SMTP backend
- Background task queue (Celery)
- Send tracking

---

## Phase 4: Automation Engine

### 4.1 Triggers
- Opt-in (new contact)
- Tag added/removed
- Purchase (main or upsell)
- Email opened/clicked
- Date-based (birthday, anniversary)
- Custom API trigger

### 4.2 Actions
- Send email
- Add/remove tag
- Add to sequence
- Webhook to external service
- Delay (wait X days/hours)
- Condition (if/else branches)

### 4.3 Visual Automation Builder (Parked)
- Drag-and-drop workflow editor
- Pre-built automation templates
- Duplicate and modify

---

## Phase 5: CRM Features

### 5.1 Contact Management
- Full contact profile view
- Activity timeline
- Notes & tasks per contact
- Contact search & filters

### 5.2 Segmentation
- Tag-based segments
- Filter by behavior (opened, purchased, etc.)
- Saved segments
- Segment size preview

### 5.3 Pipeline & Deals
- `Pipeline` model (already built)
- `Opportunity` model (already built)
- Drag-and-drop kanban board
- Deal value tracking
- Stage conversion rates

### 5.4 Custom Fields
- Add custom fields to Contact
- Field types: text, number, date, dropdown, checkbox
- Use in segmentation and automation

---

## Phase 6: Client Portal

### 6.1 Customer Dashboard
- Order history with receipts
- Active subscriptions/products
- Profile settings (email, password, notifications)
- Downloadable resources

### 6.2 Services & Products Catalog
- Full catalog visible to all customers
- Purchased = unlocked, immediate access
- Not purchased = visible but locked, with purchase button
- Categories: courses, services, memberships

### 6.3 Subscription Management
- View active subscriptions
- Upgrade/downgrade plans
- Cancel subscription
- Change billing cycle
- Update payment method

---

## Phase 7: Course Content (Learning Management)

### 7.1 Content Types
- Video embeds (YouTube, Vimeo, Wistia, custom)
- Text lessons (rich text editor)
- PDF downloads
- Audio files (podcast-style)

### 7.2 Structure
- Courses → Modules → Lessons
- Immediate access upon purchase
- Progress bar per lesson
- "Continue where you left off" functionality

### 7.3 Quizzes
- Multiple choice questions
- True/false
- Score tracking
- Pass/fail threshold
- Retry capability

---

## Phase 8: Gamification

### 8.1 Points System
- Points for: completing lessons, watching videos, passing quizzes, purchases, daily login, referrals
- Configurable points per action
- Points history

### 8.2 Badges/Achievements
- Unlockable badges (e.g., "First Lesson Complete", "Quiz Master", "5-Day Streak")
- Badge display on profile
- Progress toward badges visible

### 8.3 Leaderboards
- Weekly/monthly/all-time rankings
- Points-based ranking
- Public, visible to all community members

### 8.4 Streaks
- Daily login streak tracking
- Streak preservation (minimum daily activity)
- Streak recovery options
- Streak milestones (7 days, 30 days, etc.)

---

## Phase 9: Analytics & Dashboards

### 9.1 Revenue Dashboard
- Total revenue (daily, weekly, monthly, yearly)
- Revenue by funnel/product
- Revenue by service
- Payment method breakdown (Stripe vs PayPal)
- Refunds and chargebacks tracking

### 9.2 Email Marketing Analytics
- Campaign performance (open rate, click rate)
- List growth (new subscribers, unsubscribes)
- Revenue attributed per email
- Best performing emails
- A/B test results

### 9.3 Ad Attribution
- Meta Ads spend + ROAS
- LinkedIn Ads spend
- Cost per acquisition per funnel
- First/last touch attribution

### 9.4 Funnel Analytics
- Opt-in conversion rate
- Purchase conversion rate (per traffic source)
- Drop-off points in funnel
- A/B test results

### 9.5 Customer Analytics
- Customer lifetime value
- Average order value
- Customer repurchase rate
- Customer segments by value

---

## Phase 10: Social Integration

### 10.1 Meta Integration
- Meta Pixel installation (automatic on funnels)
- Meta Conversions API (server-side tracking)
- Lead form ads integration (auto-import leads)
- Spend data export

### 10.2 LinkedIn Integration
- LinkedIn Insight Tag (tracking)
- Lead gen form import
- Spend data export

### 10.3 Unified Lead Attribution
- Tie leads to source (Meta, LinkedIn, organic, email)
- UTM + Meta/LinkedIn data combined
- First-touch and last-touch attribution

---

## Phase 11: Community Portal (Skool-Style)

### 11.1 Structure
- Discussion forums/categories
- Public + private groups
- Membership tier access (parked)

### 11.2 Member Features
- Posts (text, images, video)
- Comments and replies
- Reactions (like, celebrate, etc.)
- @mentions
- Member directory

### 11.3 Engagement
- Community leaderboard (gamification ties here)
- Admin announcements
- Direct messaging (parked)

---

## Phase 12: Scalability & White-Label

### 12.1 Multi-Tenant
- Organization model
- Separate data per client
- Custom subdomains

### 12.2 White-Label
- Custom branding per org
- Remove Genius CRM branding
- Industry-agnostic configuration

---

## Phased Build Order

| Phase | Focus | Key Deliverables |
|-------|-------|------------------|
| 1 | Foundation | Django setup, contacts, tagging ✅ |
| 2 | Funnels + Payments | Countdown, Stripe, 4-page flow |
| 3 | Email Marketing | Enhanced sequences, templates, analytics |
| 4 | Automation | Triggers, actions, workflows |
| 5 | CRM | Contacts, segments, pipelines |
| 6 | Client Portal | Dashboard, product catalog, subscriptions |
| 7 | Courses | Video, text, PDF, audio, quizzes, progress |
| 8 | Gamification | Points, badges, leaderboards, streaks |
| 9 | Dashboards | Revenue, email, ads, funnel analytics |
| 10 | Social Integration | Meta, LinkedIn tracking + exports |
| 11 | Community | Forums, posts, engagement |
| 12 | White-Label | Multi-tenant, custom branding |

---

## Parked for Later
- SMS campaigns
- Live video in community
- Assignments/certificates
- Membership tiers
- Downsell pages
- Exit intent popups
- Retargeting pixel integration
- Visual automation builder
- Direct messaging in community

---

## Immediate Next Steps (Tonight)
1. Enhance EmailSequence model with GHL-style features
2. Build email sending logic
3. Test full email sequence flow

---

## Notes
- SMTP setup deferred until closer to go-live
- Abandoned cart handled by Stripe's native recovery emails
- Template swapping allows A/B testing different funnel templates
- Platform designed for scalability across industries
