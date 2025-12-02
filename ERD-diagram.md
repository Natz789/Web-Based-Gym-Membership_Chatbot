# Visual Entity Relationship Diagram
## Gym Membership Chatbot System

This diagram can be rendered using Mermaid visualization tools.

---

## ERD Diagram (Mermaid)

```mermaid
erDiagram
    User ||--o{ UserMembership : "owns"
    User ||--o{ Payment : "makes"
    User ||--o{ WalkInPayment : "processes"
    User ||--o{ AuditLog : "performs"
    User ||--o{ Attendance : "records"
    User ||--o{ LoginActivity : "logs"
    User ||--o{ Conversation : "has"
    User ||--o{ HeroSection : "creates"
    User ||--o{ GymGallery : "uploads"
    User ||--o{ MembershipPlan : "archives"
    User ||--o{ FlexibleAccess : "archives"
    User ||--o{ UserMembership : "cancels"
    User ||--o{ Payment : "approves"

    MembershipPlan ||--o{ UserMembership : "provides"
    FlexibleAccess ||--o{ WalkInPayment : "used_in"
    UserMembership ||--o{ Payment : "paid_by"
    Conversation ||--o{ ConversationMessage : "contains"

    User {
        int id PK
        string username UK
        string email
        string password
        string first_name
        string last_name
        string role "admin/staff/member"
        string mobile_no
        text address
        date birthdate
        int age "calculated"
        image profile_image
        string kiosk_pin UK "6-digit"
        boolean is_staff
        boolean is_superuser
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    MembershipPlan {
        int id PK
        string name
        int duration_days
        decimal price
        text description
        boolean is_active
        boolean is_archived
        datetime archived_at
        int archived_by FK
        datetime created_at
        datetime updated_at
    }

    FlexibleAccess {
        int id PK
        string name
        int duration_days
        decimal price
        text description
        boolean is_active
        boolean is_archived
        datetime archived_at
        int archived_by FK
        datetime created_at
        datetime updated_at
    }

    UserMembership {
        int id PK
        int user FK
        int plan FK
        date start_date
        date end_date "calculated"
        string status "pending/active/expired/cancelled"
        datetime cancelled_at
        int cancelled_by FK
        text cancellation_reason
        datetime created_at
        datetime updated_at
    }

    Payment {
        int id PK
        int user FK
        int membership FK
        decimal amount
        string method "cash/gcash"
        datetime payment_date
        string reference_no UK "PAY-YYYYMMDD-XXXXXX"
        text notes
        string status "pending/confirmed/rejected"
        int approved_by FK
        datetime approved_at
        text rejection_reason
        datetime created_at
        datetime updated_at
    }

    WalkInPayment {
        int id PK
        int pass_type FK
        string customer_name
        string mobile_no
        decimal amount
        string method "cash/gcash"
        datetime payment_date
        string reference_no UK "WLK-YYYYMMDD-XXXXXX"
        text notes
        int processed_by FK
        datetime created_at
        datetime updated_at
    }

    Analytics {
        int id PK
        date date UK
        int total_members
        int total_passes
        decimal total_sales
        string age_group
        datetime created_at
    }

    AuditLog {
        int id PK
        int user FK "nullable"
        string action
        string severity "info/warning/error/critical"
        text description
        string ip_address
        text user_agent
        string model_name
        string object_id
        string object_repr
        json extra_data
        datetime timestamp "indexed"
    }

    Attendance {
        int id PK
        int user FK
        datetime check_in
        datetime check_out
        int duration_minutes "calculated"
        text notes
    }

    LoginActivity {
        int id PK
        int user FK
        datetime login_time
        string ip_address
        text user_agent
        boolean success
        string failure_reason
    }

    Conversation {
        int id PK
        int user FK "nullable"
        string conversation_id UK "indexed"
        string title
        string model_used
        string session_key "for anonymous"
        datetime created_at
        datetime updated_at
    }

    ConversationMessage {
        int id PK
        int conversation FK
        string role "user/assistant/system"
        text content
        int tokens_used
        int response_time_ms
        datetime created_at
    }

    HeroSection {
        int id PK
        string title
        string subtitle
        text description
        image background_image
        image mobile_image
        string cta_primary_text
        string cta_primary_link
        string cta_secondary_text
        string cta_secondary_link
        boolean is_active
        int display_order
        decimal overlay_opacity
        int created_by FK
        datetime created_at
        datetime updated_at
    }

    GymGallery {
        int id PK
        string title
        text description
        image image
        string category "equipment/facility/classes/members/events/other"
        boolean is_featured
        boolean is_active
        int display_order
        int uploaded_by FK
        datetime created_at
    }
```

---

## Simplified View - Core Business Logic

```mermaid
graph TB
    subgraph "User Management"
        U[User]
        U --> |role| ROLE[Admin/Staff/Member]
    end

    subgraph "Membership System"
        MP[MembershipPlan]
        UM[UserMembership]
        U --> |subscribes| UM
        MP --> |used by| UM
        UM --> |status| ST[Pending/Active/Expired/Cancelled]
    end

    subgraph "Payment Processing"
        P[Payment - Members]
        WP[WalkInPayment - Walk-ins]
        UM --> |requires| P
        FA[FlexibleAccess] --> |purchased as| WP
        P --> |status| PS[Pending/Confirmed/Rejected]
    end

    subgraph "Attendance & Access"
        AT[Attendance]
        U --> |check-in/out| AT
        UM --> |enables| AT
    end

    subgraph "Chatbot System"
        CV[Conversation]
        CM[ConversationMessage]
        U --> |interacts via| CV
        CV --> |contains| CM
    end

    subgraph "Analytics & Audit"
        AN[Analytics]
        AL[AuditLog]
        LA[LoginActivity]
        U --> |tracked in| AL
        U --> |tracked in| LA
        UM -.aggregated to.-> AN
        WP -.aggregated to.-> AN
    end

    subgraph "Content Management"
        HS[HeroSection]
        GG[GymGallery]
        U --> |manages| HS
        U --> |manages| GG
    end

    style U fill:#4A90E2
    style UM fill:#50C878
    style P fill:#FFD700
    style AT fill:#FF6B6B
    style CV fill:#9B59B6
    style AN fill:#34495E
```

---

## Workflow Diagrams

### Membership Purchase Flow

```mermaid
sequenceDiagram
    participant M as Member
    participant S as System
    participant Staff as Staff/Admin
    participant DB as Database

    M->>S: Browse MembershipPlans
    S->>DB: Query active plans
    DB-->>S: Return plans
    S-->>M: Display plans

    M->>S: Select plan & submit payment
    S->>DB: Create UserMembership (status=pending)
    S->>DB: Create Payment (status=pending)
    DB-->>S: Records created
    S-->>M: Payment reference number

    Staff->>S: Review pending payment
    S->>DB: Query Payment (status=pending)
    DB-->>Staff: Payment details

    alt Payment Approved
        Staff->>S: Confirm payment
        S->>DB: Update Payment (status=confirmed)
        S->>DB: Update UserMembership (status=active)
        S->>DB: Create AuditLog
        DB-->>M: Membership activated
    else Payment Rejected
        Staff->>S: Reject payment
        S->>DB: Update Payment (status=rejected)
        S->>DB: Update UserMembership (status=cancelled)
        S->>DB: Create AuditLog
        DB-->>M: Payment rejected notification
    end
```

### Walk-in Purchase Flow

```mermaid
sequenceDiagram
    participant C as Walk-in Customer
    participant Staff as Staff
    participant S as System
    participant DB as Database

    C->>Staff: Request flexible access pass
    Staff->>S: Browse FlexibleAccess options
    S->>DB: Query active passes
    DB-->>S: Return passes
    S-->>Staff: Display options

    Staff->>S: Process walk-in sale
    S->>DB: Create WalkInPayment
    S->>DB: Create AuditLog (walkin_sale)
    DB-->>S: Payment reference
    S-->>Staff: Receipt with reference
    Staff-->>C: Provide receipt

    Note over S,DB: No UserMembership created<br/>Instant processing
```

### Member Check-in Flow

```mermaid
sequenceDiagram
    participant M as Member
    participant K as Kiosk
    participant S as System
    participant DB as Database

    M->>K: Enter 6-digit PIN
    K->>S: Verify PIN
    S->>DB: Query User by kiosk_pin
    DB-->>S: User details

    S->>DB: Check active UserMembership
    alt Has Active Membership
        DB-->>S: Membership valid
        S->>DB: Create Attendance (check_in)
        DB-->>S: Check-in recorded
        S-->>K: Success message
        K-->>M: "Welcome! Enjoy your workout"
    else No Active Membership
        DB-->>S: No valid membership
        S-->>K: Error message
        K-->>M: "No active membership found"
    end
```

### Chatbot Conversation Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CB as Chatbot
    participant DB as Database
    participant AI as Ollama AI

    U->>CB: Send message

    CB->>DB: Get or create Conversation
    DB-->>CB: conversation_id

    CB->>DB: Store user message (ConversationMessage)

    CB->>DB: Fetch conversation history
    DB-->>CB: Previous messages

    CB->>AI: Send prompt + history
    AI-->>CB: AI response

    CB->>DB: Store assistant message (ConversationMessage)
    CB->>DB: Update Conversation.updated_at

    CB-->>U: Display response
```

---

## Data Flow Overview

```mermaid
graph LR
    subgraph Input
        REG[New Registration]
        PUR[Purchase Membership]
        WALK[Walk-in Sale]
        CHK[Check-in/out]
        CHAT[Chatbot Query]
    end

    subgraph Processing
        AUTH[Authentication]
        VALID[Validation]
        PROC[Payment Processing]
        AI[AI Processing]
    end

    subgraph Storage
        USR[(User DB)]
        MEM[(Membership DB)]
        PAY[(Payment DB)]
        ATT[(Attendance DB)]
        CONV[(Conversation DB)]
        AUDIT[(Audit Log DB)]
    end

    subgraph Output
        DASH[Dashboard]
        REP[Reports]
        NOTIF[Notifications]
        CHAT_RESP[Chatbot Response]
    end

    REG --> AUTH --> USR
    PUR --> VALID --> MEM
    PUR --> PROC --> PAY
    WALK --> PROC --> PAY
    CHK --> VALID --> ATT
    CHAT --> AI --> CONV

    USR --> AUDIT
    MEM --> AUDIT
    PAY --> AUDIT
    ATT --> AUDIT

    USR --> DASH
    MEM --> DASH
    PAY --> DASH
    ATT --> DASH

    DASH --> REP
    PROC --> NOTIF
    CONV --> CHAT_RESP
```

---

## Key Constraints & Rules

### Database Constraints
- **Unique Constraints**: username, email, kiosk_pin, reference_no, conversation_id
- **Foreign Key Protections**: MembershipPlan and FlexibleAccess use PROTECT (prevent deletion if in use)
- **Cascading Deletes**: User deletion cascades to memberships, payments, attendance
- **Null Constraints**: Most relationships allow NULL for soft references (approved_by, cancelled_by, etc.)

### Business Rules
1. **Only one active membership** per user at a time (enforced at application level)
2. **Payment must be confirmed** before membership activation
3. **Expired memberships automatically updated** by scheduled task
4. **Kiosk access requires** valid kiosk_pin AND active membership
5. **Archived plans** cannot be purchased but remain in records
6. **Audit logs** created for all critical operations (immutable)
7. **Walk-in payments** processed immediately (no approval needed)
8. **Conversation history** preserved for all users (including anonymous)

---

## Index Strategy

### High-Traffic Indexes
1. **AuditLog**: timestamp, user+timestamp, action+timestamp
2. **Attendance**: check_in, user+check_in
3. **LoginActivity**: user+login_time
4. **Conversation**: conversation_id, user+updated_at
5. **ConversationMessage**: conversation+created_at

### Lookup Indexes
- User.username (unique)
- User.kiosk_pin (unique)
- Payment.reference_no (unique)
- WalkInPayment.reference_no (unique)
- Analytics.date (unique)

---

**Generated**: 2025-12-02
**Database**: PostgreSQL/MySQL (Django ORM Compatible)
**Framework**: Django 4.x+
