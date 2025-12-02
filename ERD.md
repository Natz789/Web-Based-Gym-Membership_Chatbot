# Entity Relationship Diagram (ERD)
## Gym Membership Chatbot System

This document describes the database schema for the Gym Membership Chatbot application.

---

## Entities and Relationships

### Core Entities

#### 1. **User** (users)
Custom user model with role-based access control
- **PK**: id
- username (unique)
- email
- password
- first_name
- last_name
- role (admin/staff/member)
- mobile_no
- address
- birthdate
- age (calculated)
- profile_image
- kiosk_pin (unique, 6-digit)
- is_staff
- is_superuser
- is_active
- created_at
- updated_at

**Relationships:**
- One-to-Many with UserMembership (as member)
- One-to-Many with Payment (as payer)
- One-to-Many with WalkInPayment (as processor)
- One-to-Many with AuditLog (as actor)
- One-to-Many with Attendance (as attendee)
- One-to-Many with LoginActivity (as user)
- One-to-Many with Conversation (as conversation owner)
- One-to-Many with HeroSection (as creator)
- One-to-Many with GymGallery (as uploader)
- One-to-Many with MembershipPlan (as archiver)
- One-to-Many with FlexibleAccess (as archiver)
- One-to-Many with UserMembership (as canceller)
- One-to-Many with Payment (as approver)

---

#### 2. **MembershipPlan** (membership_plans)
Permanent membership plans (monthly, yearly, etc.)
- **PK**: id
- name
- duration_days
- price
- description
- is_active
- is_archived
- archived_at
- **FK**: archived_by → User.id
- created_at
- updated_at

**Relationships:**
- One-to-Many with UserMembership
- Many-to-One with User (archived_by)

---

#### 3. **FlexibleAccess** (flexible_access)
Walk-in passes (1-day, 3-day, weekly, etc.)
- **PK**: id
- name
- duration_days
- price
- description
- is_active
- is_archived
- archived_at
- **FK**: archived_by → User.id
- created_at
- updated_at

**Relationships:**
- One-to-Many with WalkInPayment
- Many-to-One with User (archived_by)

---

#### 4. **UserMembership** (user_memberships)
Tracks member subscriptions to plans
- **PK**: id
- **FK**: user → User.id
- **FK**: plan → MembershipPlan.id
- start_date
- end_date (calculated)
- status (pending/active/expired/cancelled)
- cancelled_at
- **FK**: cancelled_by → User.id
- cancellation_reason
- created_at
- updated_at

**Relationships:**
- Many-to-One with User
- Many-to-One with MembershipPlan
- One-to-Many with Payment
- Many-to-One with User (cancelled_by)

---

#### 5. **Payment** (payments)
Payment records for registered members
- **PK**: id
- **FK**: user → User.id
- **FK**: membership → UserMembership.id
- amount
- method (cash/gcash)
- payment_date
- reference_no (unique, auto-generated)
- notes
- status (pending/confirmed/rejected)
- **FK**: approved_by → User.id
- approved_at
- rejection_reason
- created_at
- updated_at

**Relationships:**
- Many-to-One with User
- Many-to-One with UserMembership
- Many-to-One with User (approved_by)

---

#### 6. **WalkInPayment** (walk_in_payments)
Payment records for walk-in clients (no account required)
- **PK**: id
- **FK**: pass_type → FlexibleAccess.id
- customer_name
- mobile_no
- amount
- method (cash/gcash)
- payment_date
- reference_no (unique, auto-generated)
- notes
- **FK**: processed_by → User.id
- created_at
- updated_at

**Relationships:**
- Many-to-One with FlexibleAccess
- Many-to-One with User (processed_by)

---

### Analytics & Monitoring

#### 7. **Analytics** (analytics)
Daily/weekly aggregated data for dashboard
- **PK**: id
- date (unique)
- total_members
- total_passes
- total_sales
- age_group
- created_at

**Relationships:**
- None (aggregate data)

---

#### 8. **AuditLog** (audit_logs)
Audit trail for all system activities
- **PK**: id
- **FK**: user → User.id (nullable)
- action (40+ action types)
- severity (info/warning/error/critical)
- description
- ip_address
- user_agent
- model_name
- object_id
- object_repr
- extra_data (JSON)
- timestamp (indexed)

**Relationships:**
- Many-to-One with User

**Indexes:**
- timestamp DESC
- user + timestamp DESC
- action + timestamp DESC

---

#### 9. **Attendance** (attendance)
Track member check-ins and check-outs
- **PK**: id
- **FK**: user → User.id
- check_in
- check_out
- duration_minutes (calculated)
- notes

**Relationships:**
- Many-to-One with User

**Indexes:**
- check_in DESC
- user + check_in DESC

---

#### 10. **LoginActivity** (login_activities)
Track user login activity for security
- **PK**: id
- **FK**: user → User.id
- login_time
- ip_address
- user_agent
- success
- failure_reason

**Relationships:**
- Many-to-One with User

**Indexes:**
- user + login_time DESC

---

### Chatbot System

#### 11. **Conversation** (conversations)
Persistent conversation storage for chatbot
- **PK**: id
- **FK**: user → User.id (nullable)
- conversation_id (unique, indexed)
- title
- model_used
- session_key (for anonymous users)
- created_at
- updated_at

**Relationships:**
- Many-to-One with User
- One-to-Many with ConversationMessage

**Indexes:**
- user + updated_at DESC
- conversation_id

---

#### 12. **ConversationMessage** (conversation_messages)
Individual messages in a conversation
- **PK**: id
- **FK**: conversation → Conversation.id
- role (user/assistant/system)
- content
- tokens_used
- response_time_ms
- created_at

**Relationships:**
- Many-to-One with Conversation

**Indexes:**
- conversation + created_at

---

### Content Management

#### 13. **HeroSection** (hero_sections)
Hero section for homepage with images and content
- **PK**: id
- title
- subtitle
- description
- background_image
- mobile_image
- cta_primary_text
- cta_primary_link
- cta_secondary_text
- cta_secondary_link
- is_active
- display_order
- overlay_opacity
- **FK**: created_by → User.id
- created_at
- updated_at

**Relationships:**
- Many-to-One with User (created_by)

---

#### 14. **GymGallery** (gym_gallery)
Gallery of gym photos to showcase facilities
- **PK**: id
- title
- description
- image
- category (equipment/facility/classes/members/events/other)
- is_featured
- is_active
- display_order
- **FK**: uploaded_by → User.id
- created_at

**Relationships:**
- Many-to-One with User (uploaded_by)

---

## Relationship Summary

```
User
├── UserMembership (1:N) - owns memberships
├── Payment (1:N) - makes payments
├── WalkInPayment (1:N) - processes walk-in sales
├── AuditLog (1:N) - activity tracking
├── Attendance (1:N) - check-in/out records
├── LoginActivity (1:N) - login history
├── Conversation (1:N) - chatbot conversations
├── HeroSection (1:N) - creates hero sections
├── GymGallery (1:N) - uploads gallery images
├── MembershipPlan (1:N) - archives plans
├── FlexibleAccess (1:N) - archives passes
├── UserMembership.cancelled_by (1:N) - cancels memberships
└── Payment.approved_by (1:N) - approves payments

MembershipPlan
├── UserMembership (1:N) - subscribed by users
└── User.archived_by (N:1) - archived by admin

FlexibleAccess
├── WalkInPayment (1:N) - purchased by walk-ins
└── User.archived_by (N:1) - archived by admin

UserMembership
├── User (N:1) - belongs to user
├── MembershipPlan (N:1) - uses plan
├── Payment (1:N) - payment records
└── User.cancelled_by (N:1) - cancelled by admin

Payment
├── User (N:1) - paid by user
├── UserMembership (N:1) - for membership
└── User.approved_by (N:1) - approved by staff

WalkInPayment
├── FlexibleAccess (N:1) - uses pass type
└── User.processed_by (N:1) - processed by staff

Conversation
├── User (N:1) - belongs to user
└── ConversationMessage (1:N) - contains messages

ConversationMessage
└── Conversation (N:1) - part of conversation

HeroSection
└── User.created_by (N:1) - created by admin

GymGallery
└── User.uploaded_by (N:1) - uploaded by staff

AuditLog
└── User (N:1) - performed by user

Attendance
└── User (N:1) - attendance of user

LoginActivity
└── User (N:1) - login of user

Analytics
(No relationships - aggregate data only)
```

---

## Key Database Features

### Indexes
- Performance indexes on high-query tables (AuditLog, Attendance, LoginActivity, Conversation)
- Composite indexes for common query patterns (user + timestamp)

### Auto-Generated Fields
- Payment reference numbers: `PAY-YYYYMMDD-XXXXXX`
- Walk-in payment references: `WLK-YYYYMMDD-XXXXXX`
- Kiosk PIN: 6-digit unique PIN for member check-in
- Age calculation from birthdate

### Cascade Rules
- User deletion: CASCADE to memberships, payments, attendance
- Plan/Pass deletion: PROTECT (prevents deletion if in use)
- Soft deletes: Archive flags for plans and passes

### Status Workflows

**UserMembership Status:**
1. pending → Payment awaiting confirmation
2. active → Payment confirmed, membership valid
3. expired → End date reached
4. cancelled → Manually cancelled by admin

**Payment Status:**
1. pending → Awaiting staff confirmation
2. confirmed → Approved by staff, membership activated
3. rejected → Declined by staff, membership cancelled

---

## Business Rules

1. **Role Hierarchy**: Admin > Staff > Member
2. **Membership Validation**: Active membership required for gym access
3. **Payment Approval**: Staff/Admin must confirm payments before activation
4. **Archiving**: Plans can be archived but not deleted (preserves historical data)
5. **Audit Trail**: All critical actions are logged with user, timestamp, and IP
6. **Kiosk Access**: Members with active memberships can check-in using PIN
7. **Walk-in Sales**: No user account required, instant processing
8. **Conversation Tracking**: Full chatbot conversation history for analysis

---

## Generated: 2025-12-02
