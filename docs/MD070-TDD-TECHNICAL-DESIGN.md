# MD070 - Technical Design Document (TDD)
## Nutrition Intelligence - System Architecture & Implementation

**Document Version:** 1.0.0
**Last Updated:** January 2025
**Authors:** Engineering Team
**Reviewers:** CTO, Senior Architects
**Status:** Draft → Technical Review → Approved
**Classification:** Internal - Confidential

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Database Design](#3-database-design)
4. [API Specifications](#4-api-specifications)
5. [Social Media Integration](#5-social-media-integration)
6. [AI/ML Pipeline](#6-aiml-pipeline)
7. [Security & Privacy](#7-security--privacy)
8. [Scalability & Performance](#8-scalability--performance)
9. [DevOps & Infrastructure](#9-devops--infrastructure)
10. [Monitoring & Observability](#10-monitoring--observability)

---

## 1. Executive Summary

### 1.1 System Overview

**Nutrition Intelligence** is a multi-platform health social network built on modern cloud-native architecture, supporting:

- **100K concurrent users** (Year 1 target)
- **1M+ API requests/day**
- **99.9% uptime SLA**
- **Real-time features** (WebSocket connections)
- **AI/ML workloads** (image recognition, NLP, predictions)
- **Multi-region deployment** (Mexico-first, LATAM expansion)

### 1.2 Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                        │
├─────────────────────────────────────────────────────────────┤
│ • React Native (Expo) - iOS/Android App                     │
│ • React 18 - Web Application                                │
│ • Next.js 14 - SSR/SEO for marketing pages                  │
│ • TailwindCSS + Shadcn/ui - Design System                   │
│ • Zustand - State Management                                │
│ • React Query - Server State & Caching                      │
│ • Socket.IO Client - Real-time Communication                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                         API LAYER                            │
├─────────────────────────────────────────────────────────────┤
│ • FastAPI (Python 3.11+) - Main API Server                  │
│ • Pydantic - Data Validation                                │
│ • SQLAlchemy 2.0 - ORM                                       │
│ • Alembic - Database Migrations                             │
│ • Celery - Async Task Queue                                 │
│ • Socket.IO - WebSocket Server                              │
│ • FastAPI-Users - Authentication                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│ • PostgreSQL 15 - Primary Database                          │
│ • Redis 7 - Caching + Session Store + Pub/Sub               │
│ • Elasticsearch 8 - Full-Text Search                        │
│ • TimescaleDB - Time-Series Data (metrics, vitals)          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                           │
├─────────────────────────────────────────────────────────────┤
│ • MinIO / S3 - Object Storage (images, documents)           │
│ • Cloudinary - Image CDN + Transformations                  │
│ • PostgreSQL JSONB - Semi-structured Data                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                        AI/ML LAYER                           │
├─────────────────────────────────────────────────────────────┤
│ • PyTorch 2.0 - Deep Learning Framework                     │
│ • Hugging Face Transformers - NLP Models                    │
│ • OpenAI GPT-4 API - Advanced NLP                           │
│ • TensorFlow Lite - Mobile Inference                        │
│ • MLflow - Model Registry & Versioning                      │
│ • Ray - Distributed ML Training                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                       │
├─────────────────────────────────────────────────────────────┤
│ • Kubernetes (K8s) - Container Orchestration                │
│ • Docker - Containerization                                 │
│ • AWS / Google Cloud - Cloud Provider                       │
│ • Terraform - Infrastructure as Code                        │
│ • GitHub Actions - CI/CD Pipeline                           │
│ • ArgoCD - GitOps Deployment                                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY LAYER                       │
├─────────────────────────────────────────────────────────────┤
│ • Prometheus - Metrics Collection                           │
│ • Grafana - Metrics Visualization                           │
│ • Loki - Log Aggregation                                    │
│ • Jaeger - Distributed Tracing                              │
│ • Sentry - Error Tracking                                   │
│ • PagerDuty - Incident Management                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. System Architecture

### 2.1 High-Level Architecture Diagram

```
                                   Internet
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │   Cloudflare CDN        │
                        │   (DDoS Protection)     │
                        └─────────────────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │   Web App       │  │   iOS App       │  │  Android App    │
        │  (React/Next)   │  │ (React Native)  │  │ (React Native)  │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │   API Gateway           │
                        │   (Kong / AWS ALB)      │
                        │   Rate Limiting         │
                        │   Authentication        │
                        └─────────────────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │   FastAPI        │  │  WebSocket      │  │   ML Service    │
        │   REST API       │  │  Server         │  │   (AI Models)   │
        │   (Pods x10)     │  │  (Socket.IO)    │  │   (GPU Pods)    │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
        ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
        │  PostgreSQL     │  │     Redis        │  │ Elasticsearch   │
        │  (Primary DB)   │  │  (Cache/Queue)   │  │  (Search)       │
        │  Master-Replica │  │  Cluster (3)     │  │  Cluster (3)    │
        └─────────────────┘  └─────────────────┘  └─────────────────┘
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      │
                                      ▼
                        ┌─────────────────────────┐
                        │   Object Storage        │
                        │   (S3 / MinIO)          │
                        │   + Cloudinary CDN      │
                        └─────────────────────────┘
```

### 2.2 Microservices Architecture

We use a **modular monolith** initially (simpler to develop/deploy) with clear boundaries for future microservices extraction.

```python
# app/ directory structure
app/
├── __init__.py
├── main.py                     # FastAPI app entry point
│
├── api/                        # API layer (controllers)
│   ├── v1/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── patients.py
│   │   ├── nutritionists.py
│   │   ├── posts.py            # Social feed
│   │   ├── groups.py
│   │   ├── challenges.py
│   │   ├── recipes.py
│   │   ├── meals.py
│   │   ├── measurements.py
│   │   └── ai.py               # AI endpoints
│
├── core/                       # Core business logic
│   ├── config.py
│   ├── security.py
│   ├── dependencies.py
│   └── exceptions.py
│
├── models/                     # SQLAlchemy ORM models
│   ├── user.py
│   ├── patient.py
│   ├── nutritionist.py
│   ├── post.py
│   ├── comment.py
│   ├── group.py
│   ├── challenge.py
│   ├── recipe.py
│   ├── meal_log.py
│   ├── measurement.py
│   ├── clinical_record.py
│   └── __init__.py
│
├── schemas/                    # Pydantic schemas (DTOs)
│   ├── user.py
│   ├── post.py
│   ├── recipe.py
│   └── ...
│
├── services/                   # Business logic services
│   ├── auth_service.py
│   ├── user_service.py
│   ├── feed_service.py         # Feed algorithm
│   ├── gamification_service.py
│   ├── notification_service.py
│   ├── ai/
│   │   ├── food_recognition.py
│   │   ├── label_scanner.py
│   │   ├── diet_generator.py
│   │   └── predictions.py
│   └── social/
│       ├── instagram.py
│       ├── tiktok.py
│       ├── facebook.py
│       └── twitter.py
│
├── repositories/               # Data access layer
│   ├── user_repo.py
│   ├── post_repo.py
│   └── ...
│
├── tasks/                      # Celery async tasks
│   ├── email_tasks.py
│   ├── notification_tasks.py
│   ├── ai_tasks.py
│   └── social_sharing_tasks.py
│
├── utils/                      # Utilities
│   ├── storage.py              # S3/MinIO wrapper
│   ├── image.py                # Image processing
│   ├── encryption.py
│   └── validators.py
│
└── tests/                      # Pytest tests
    ├── unit/
    ├── integration/
    └── e2e/
```

### 2.3 Request Flow Example: "Create Post"

```
User taps "Share Progress Photo" on mobile app
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. MOBILE APP (React Native)                                │
│    • User selects photo from gallery                        │
│    • Writes caption: "¡Perdí 5kg este mes! 🎉"             │
│    • Taps "Publicar"                                        │
└─────────────────────────────────────────────────────────────┘
              │
              │ POST /api/v1/posts
              │ Headers: Authorization: Bearer <JWT>
              │ Body (multipart/form-data):
              │   - photo: [binary]
              │   - caption: "¡Perdí 5kg este mes! 🎉"
              │   - type: "progress"
              │   - visibility: "public"
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. API GATEWAY (Kong)                                       │
│    • Rate limiting check (100 req/min per user)             │
│    • JWT validation                                         │
│    • Request logging                                        │
│    ✅ Forward to FastAPI                                   │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. FASTAPI - POST /api/v1/posts                             │
│    def create_post(                                         │
│        file: UploadFile,                                    │
│        data: PostCreate,                                    │
│        current_user: User = Depends(get_current_user)       │
│    ):                                                       │
│        # 3.1 Validate request                               │
│        validate_image(file)  # Check size, format           │
│                                                             │
│        # 3.2 Upload image to storage (async)                │
│        image_url = await storage_service.upload(            │
│            file, folder="posts", user_id=current_user.id    │
│        )                                                    │
│                                                             │
│        # 3.3 Create post in database                        │
│        post = post_service.create_post(                     │
│            author_id=current_user.id,                       │
│            type="progress",                                 │
│            caption=data.caption,                            │
│            media_urls=[image_url],                          │
│            visibility="public"                              │
│        )                                                    │
│                                                             │
│        # 3.4 Trigger async tasks                            │
│        tasks.process_new_post.delay(post.id)                │
│                                                             │
│        return PostResponse(post)                            │
└─────────────────────────────────────────────────────────────┘
              │
              ├──────────────────┬──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
      ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
      │ 4. DATABASE │    │ 5. CELERY   │    │ 6. REDIS    │
      │             │    │    TASKS    │    │             │
      │ INSERT INTO │    │             │    │ Cache       │
      │ posts       │    │ • AI check  │    │ invalidate  │
      │ VALUES(...) │    │   content   │    │ user feed   │
      └─────────────┘    │ • Notify    │    └─────────────┘
                         │   followers │
                         │ • Update    │
                         │   trending  │
                         └─────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. WEBSOCKET NOTIFICATION                                   │
│    • Broadcast to followers via Socket.IO                   │
│    • "Nueva publicación de @username"                       │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. MOBILE APP - Real-time Update                            │
│    • Followers see notification bell light up               │
│    • Feed refreshes with new post at top                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Database Design

### 3.1 Database Schema Overview

We use **PostgreSQL 15** with the following extensions:
- `uuid-ossp` - UUID generation
- `pg_trgm` - Trigram matching for fuzzy search
- `pgcrypto` - Encryption functions
- `timescaledb` - Time-series data (for metrics, measurements)

**Schema Organization:**
```sql
-- Schemas for logical separation
CREATE SCHEMA auth;          -- Authentication & users
CREATE SCHEMA social;        -- Posts, comments, groups, challenges
CREATE SCHEMA clinical;      -- Medical records, measurements
CREATE SCHEMA nutrition;     -- Foods, recipes, meal logs
CREATE SCHEMA gamification;  -- XP, badges, levels
CREATE SCHEMA integrations;  -- External services (Instagram, WhatsApp)
CREATE SCHEMA analytics;     -- Metrics, events, tracking
```

### 3.2 Core Tables - Authentication & Users

```sql
-- ============================================================================
-- USERS TABLE (Central entity)
-- ============================================================================
CREATE TABLE auth.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Basic Info
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,

    phone VARCHAR(20) UNIQUE,
    phone_verified BOOLEAN DEFAULT FALSE,

    username VARCHAR(50) UNIQUE NOT NULL,

    -- Password (hashed with bcrypt)
    hashed_password VARCHAR(255) NOT NULL,

    -- OAuth
    google_id VARCHAR(255) UNIQUE,
    facebook_id VARCHAR(255) UNIQUE,
    apple_id VARCHAR(255) UNIQUE,

    -- Profile
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(255) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,

    date_of_birth DATE,
    gender VARCHAR(20), -- 'male', 'female', 'other', 'prefer_not_to_say'

    photo_url VARCHAR(500),
    bio TEXT,

    -- Location
    country VARCHAR(2) DEFAULT 'MX', -- ISO code
    state VARCHAR(100),
    city VARCHAR(100),

    -- User Type & Roles
    user_type VARCHAR(20) NOT NULL, -- 'patient', 'nutritionist', 'admin'
    roles JSONB DEFAULT '[]'::jsonb, -- ['patient', 'nutritionist'] for dual roles

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_banned BOOLEAN DEFAULT FALSE,
    banned_reason TEXT,
    banned_at TIMESTAMP,

    -- Security
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,

    -- Soft Delete
    deleted_at TIMESTAMP,

    -- Indexes
    CONSTRAINT email_lowercase CHECK (email = LOWER(email)),
    CONSTRAINT username_lowercase CHECK (username = LOWER(username))
);

CREATE INDEX idx_users_email ON auth.users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_username ON auth.users(username) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_user_type ON auth.users(user_type) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_state ON auth.users(state) WHERE deleted_at IS NULL;


-- ============================================================================
-- REFRESH TOKENS (JWT refresh token rotation)
-- ============================================================================
CREATE TABLE auth.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    token VARCHAR(500) UNIQUE NOT NULL,
    device_info JSONB, -- {device_type, os, browser, ip}

    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    -- Token rotation (when refreshed, old token is revoked)
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMP,
    replaced_by_token VARCHAR(500)
);

CREATE INDEX idx_refresh_tokens_user ON auth.refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON auth.refresh_tokens(token) WHERE NOT revoked;


-- ============================================================================
-- PATIENTS TABLE
-- ============================================================================
CREATE TABLE auth.patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Assignment
    nutritionist_id UUID REFERENCES auth.nutritionists(user_id) ON DELETE SET NULL,
    assigned_at TIMESTAMP,

    -- Goals
    primary_goal VARCHAR(50), -- 'weight_loss', 'muscle_gain', 'maintenance', 'health_condition'
    target_weight_kg DECIMAL(5,2),
    target_date DATE,

    -- Health Conditions
    health_conditions JSONB DEFAULT '[]'::jsonb,
    -- [{"name": "diabetes_type_2", "diagnosed_at": "2023-01-15", "controlled": true}]

    -- Allergies & Restrictions
    allergies JSONB DEFAULT '[]'::jsonb, -- ["peanuts", "shellfish"]
    food_restrictions JSONB DEFAULT '[]'::jsonb, -- ["gluten", "lactose"]
    dietary_preference VARCHAR(50), -- 'omnivore', 'vegetarian', 'vegan'

    -- Insurance
    has_insurance BOOLEAN DEFAULT FALSE,
    insurance_type VARCHAR(50),
    insurance_number VARCHAR(100),

    -- Status
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'graduated', 'dropped'

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_patients_nutritionist ON auth.patients(nutritionist_id);
CREATE INDEX idx_patients_status ON auth.patients(status);


-- ============================================================================
-- NUTRITIONISTS TABLE
-- ============================================================================
CREATE TABLE auth.nutritionists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Professional Info
    professional_license VARCHAR(100) UNIQUE NOT NULL, -- Cédula profesional
    license_verified BOOLEAN DEFAULT FALSE,
    license_verified_at TIMESTAMP,
    license_verified_by UUID REFERENCES auth.users(id),

    specializations JSONB DEFAULT '[]'::jsonb,
    -- ["sports_nutrition", "diabetes", "pediatric"]

    years_experience INTEGER,

    -- Education
    education JSONB DEFAULT '[]'::jsonb,
    -- [{"degree": "Licenciatura en Nutrición", "institution": "UNAM", "year": 2015}]

    certifications JSONB DEFAULT '[]'::jsonb,

    -- Practice Info
    clinic_name VARCHAR(255),
    clinic_address TEXT,
    clinic_phone VARCHAR(20),

    consultation_fee_mxn INTEGER, -- Per session fee
    accepts_insurance BOOLEAN DEFAULT FALSE,

    -- Availability
    working_hours JSONB,
    -- {"monday": {"start": "09:00", "end": "18:00"}, ...}

    -- Stats (denormalized for performance)
    active_patients_count INTEGER DEFAULT 0,
    total_patients_count INTEGER DEFAULT 0,
    avg_rating DECIMAL(3,2) DEFAULT 5.0,
    total_reviews INTEGER DEFAULT 0,

    -- Status
    verification_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'verified', 'rejected'
    is_accepting_patients BOOLEAN DEFAULT TRUE,

    -- Gamification (professional reputation)
    reputation_points INTEGER DEFAULT 0,
    professional_level VARCHAR(20) DEFAULT 'junior',

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_nutritionists_verified ON auth.nutritionists(license_verified);
CREATE INDEX idx_nutritionists_accepting ON auth.nutritionists(is_accepting_patients);
CREATE INDEX idx_nutritionists_rating ON auth.nutritionists(avg_rating DESC);
```

### 3.3 Social Network Tables

```sql
-- ============================================================================
-- POSTS TABLE (Main feed content)
-- ============================================================================
CREATE TABLE social.posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    author_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Content
    type VARCHAR(20) NOT NULL,
    -- 'text', 'photo', 'progress', 'recipe', 'question', 'achievement'

    title VARCHAR(255),
    body TEXT NOT NULL,

    media_urls JSONB DEFAULT '[]'::jsonb, -- Array of image/video URLs

    -- Type-specific data (polymorphic)
    progress_data JSONB,
    -- {
    --   "weight_before_kg": 80.5,
    --   "weight_after_kg": 75.2,
    --   "weight_lost_kg": 5.3,
    --   "time_period_days": 30,
    --   "photo_before_url": "...",
    --   "photo_after_url": "..."
    -- }

    recipe_data JSONB,
    -- {"recipe_id": "uuid", "servings": 4}

    achievement_data JSONB,
    -- {"badge_id": "uuid", "badge_name": "30_day_streak"}

    -- Visibility & Privacy
    visibility VARCHAR(20) DEFAULT 'public',
    -- 'public', 'followers', 'group', 'family_circle', 'nutritionist_only'

    group_id UUID REFERENCES social.groups(id) ON DELETE CASCADE,
    family_circle_id UUID REFERENCES social.family_circles(id) ON DELETE CASCADE,

    -- Engagement Metrics (denormalized for performance)
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,
    saves_count INTEGER DEFAULT 0,

    -- Reactions Breakdown
    reaction_heart INTEGER DEFAULT 0,   -- ❤️
    reaction_clap INTEGER DEFAULT 0,    -- 👏
    reaction_fire INTEGER DEFAULT 0,    -- 🔥
    reaction_strong INTEGER DEFAULT 0,  -- 💪
    reaction_celebrate INTEGER DEFAULT 0, -- 🎉

    -- Virality & Ranking
    virality_score DECIMAL(10,2) DEFAULT 0,
    -- Calculated: (likes + comments*3 + shares*5) / hours_since_post

    is_trending BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    featured_at TIMESTAMP,
    featured_by UUID REFERENCES auth.users(id),

    -- Moderation
    is_flagged BOOLEAN DEFAULT FALSE,
    flag_count INTEGER DEFAULT 0,
    flag_reasons JSONB DEFAULT '[]'::jsonb,

    moderation_status VARCHAR(20) DEFAULT 'approved',
    -- 'pending', 'approved', 'rejected', 'removed'

    moderated_at TIMESTAMP,
    moderated_by UUID REFERENCES auth.users(id),
    moderation_notes TEXT,

    -- Search & Discovery
    tags JSONB DEFAULT '[]'::jsonb, -- ["diabetes", "recetas", "motivacion"]
    mentioned_users UUID[], -- Array of user IDs mentioned with @

    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('spanish', COALESCE(title, '')), 'A') ||
        setweight(to_tsvector('spanish', COALESCE(body, '')), 'B')
    ) STORED,

    -- Location (optional)
    state VARCHAR(100),
    city VARCHAR(100),

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP,

    -- Soft Delete
    deleted_at TIMESTAMP
);

CREATE INDEX idx_posts_author ON social.posts(author_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_type ON social.posts(type) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_visibility ON social.posts(visibility) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_group ON social.posts(group_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_trending ON social.posts(is_trending, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_created_at ON social.posts(created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_virality ON social.posts(virality_score DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_posts_search ON social.posts USING GIN(search_vector);
CREATE INDEX idx_posts_tags ON social.posts USING GIN(tags);


-- ============================================================================
-- COMMENTS TABLE
-- ============================================================================
CREATE TABLE social.comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    post_id UUID NOT NULL REFERENCES social.posts(id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Nested comments (max 3 levels)
    parent_comment_id UUID REFERENCES social.comments(id) ON DELETE CASCADE,
    depth_level INTEGER DEFAULT 0, -- 0=top-level, 1=reply, 2=reply-to-reply
    CONSTRAINT max_depth_level CHECK (depth_level <= 2),

    -- Content
    content TEXT NOT NULL,

    -- Engagement
    likes_count INTEGER DEFAULT 0,

    -- Moderation
    is_flagged BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP
);

CREATE INDEX idx_comments_post ON social.comments(post_id) WHERE NOT is_deleted;
CREATE INDEX idx_comments_author ON social.comments(author_id);
CREATE INDEX idx_comments_parent ON social.comments(parent_comment_id);
CREATE INDEX idx_comments_created_at ON social.comments(post_id, created_at ASC);


-- ============================================================================
-- REACTIONS TABLE (Likes, Hearts, etc.)
-- ============================================================================
CREATE TABLE social.reactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    post_id UUID NOT NULL REFERENCES social.posts(id) ON DELETE CASCADE,

    reaction_type VARCHAR(20) NOT NULL,
    -- 'heart', 'clap', 'fire', 'strong', 'celebrate'

    created_at TIMESTAMP DEFAULT NOW(),

    -- Unique constraint: user can only react once per post
    UNIQUE(user_id, post_id)
);

CREATE INDEX idx_reactions_post ON social.reactions(post_id);
CREATE INDEX idx_reactions_user ON social.reactions(user_id);


-- ============================================================================
-- GROUPS TABLE
-- ============================================================================
CREATE TABLE social.groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(255) NOT NULL,
    description TEXT,
    cover_image_url VARCHAR(500),
    icon_url VARCHAR(500),

    -- Group Type
    type VARCHAR(20) DEFAULT 'open',
    -- 'open' - anyone can join
    -- 'closed' - request to join
    -- 'private' - invite only
    -- 'nutritionist_only'
    -- 'patient_only'

    category VARCHAR(50),
    -- 'goal_based', 'condition_based', 'location_based', 'nutritionist_practice', 'other'

    -- Creator & Admins
    created_by UUID NOT NULL REFERENCES auth.users(id) ON DELETE SET NULL,
    admins UUID[] DEFAULT ARRAY[]::UUID[], -- Array of admin user IDs
    moderators UUID[] DEFAULT ARRAY[]::UUID[],

    -- Membership
    member_count INTEGER DEFAULT 0,
    post_count INTEGER DEFAULT 0,

    -- Rules
    rules JSONB DEFAULT '[]'::jsonb,
    -- [{"title": "Respeto mutuo", "description": "..."}, ...]

    -- Posting Permissions
    who_can_post VARCHAR(20) DEFAULT 'everyone',
    -- 'everyone', 'admins_only', 'approved_members'

    require_post_approval BOOLEAN DEFAULT FALSE,

    -- Joining
    requires_approval BOOLEAN DEFAULT FALSE,
    join_questions JSONB, -- [{"question": "...", "required": true}, ...]

    -- Activity Metrics
    activity_level VARCHAR(20),
    -- 'very_active', 'active', 'moderate', 'low'
    -- Calculated based on posts/day

    last_post_at TIMESTAMP,

    -- Discovery
    tags JSONB DEFAULT '[]'::jsonb,
    state VARCHAR(100), -- For location-based groups
    is_featured BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_groups_type ON social.groups(type) WHERE deleted_at IS NULL;
CREATE INDEX idx_groups_category ON social.groups(category) WHERE deleted_at IS NULL;
CREATE INDEX idx_groups_featured ON social.groups(is_featured) WHERE deleted_at IS NULL;
CREATE INDEX idx_groups_tags ON social.groups USING GIN(tags);


-- ============================================================================
-- GROUP MEMBERS TABLE
-- ============================================================================
CREATE TABLE social.group_members (
    group_id UUID NOT NULL REFERENCES social.groups(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    role VARCHAR(20) DEFAULT 'member',
    -- 'admin', 'moderator', 'member', 'pending'

    -- Engagement tracking
    posts_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    last_active_at TIMESTAMP,

    -- Notifications
    notification_preference VARCHAR(20) DEFAULT 'all',
    -- 'all', 'mentions_only', 'none'

    -- Join metadata
    joined_at TIMESTAMP DEFAULT NOW(),
    invited_by UUID REFERENCES auth.users(id),
    join_answers JSONB, -- Answers to join questions

    PRIMARY KEY (group_id, user_id)
);

CREATE INDEX idx_group_members_user ON social.group_members(user_id);
CREATE INDEX idx_group_members_role ON social.group_members(group_id, role);


-- ============================================================================
-- CHALLENGES TABLE
-- ============================================================================
CREATE TABLE social.challenges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title VARCHAR(255) NOT NULL,
    description TEXT,
    banner_image_url VARCHAR(500),

    -- Challenge Type
    type VARCHAR(20) NOT NULL, -- 'individual', 'team', 'community'
    category VARCHAR(50), -- 'weight_loss', 'steps', 'water', 'meals', 'exercise'

    -- Scope
    scope VARCHAR(50) DEFAULT 'national',
    -- 'national', 'state', 'city', 'group', 'nutritionist_patients'

    state VARCHAR(100),
    group_id UUID REFERENCES social.groups(id),
    nutritionist_id UUID REFERENCES auth.nutritionists(user_id),

    -- Timeline
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INTEGER GENERATED ALWAYS AS (end_date - start_date) STORED,

    status VARCHAR(20) DEFAULT 'upcoming',
    -- 'upcoming', 'active', 'completed', 'cancelled'

    -- Goal
    goal_type VARCHAR(20), -- 'cumulative', 'daily', 'weekly', 'threshold'
    goal_metric VARCHAR(50), -- 'steps', 'kg_lost', 'water_glasses', 'meals_logged'
    goal_value DECIMAL(10,2),
    goal_unit VARCHAR(20),

    -- Participation
    participant_count INTEGER DEFAULT 0,
    max_participants INTEGER, -- NULL = unlimited

    requires_approval BOOLEAN DEFAULT FALSE,

    -- Rewards
    rewards JSONB,
    -- [
    --   {"rank": 1, "reward_type": "badge", "reward_value": "first_place"},
    --   {"rank": null, "reward_type": "xp", "reward_value": "100"}
    -- ]

    -- Team Challenges
    team_size INTEGER,
    teams JSONB,

    -- Rules
    rules JSONB DEFAULT '[]'::jsonb,

    -- Visibility
    is_featured BOOLEAN DEFAULT FALSE,
    is_sponsored BOOLEAN DEFAULT FALSE,
    sponsor_name VARCHAR(255),
    sponsor_logo_url VARCHAR(500),

    -- Creator
    created_by UUID NOT NULL REFERENCES auth.users(id),
    created_by_type VARCHAR(20), -- 'admin', 'nutritionist', 'patient', 'system'

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_challenges_status ON social.challenges(status, start_date);
CREATE INDEX idx_challenges_scope ON social.challenges(scope, state);
CREATE INDEX idx_challenges_featured ON social.challenges(is_featured);


-- ============================================================================
-- CHALLENGE PARTICIPANTS TABLE
-- ============================================================================
CREATE TABLE social.challenge_participants (
    challenge_id UUID NOT NULL REFERENCES social.challenges(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    team_id UUID, -- If team challenge

    -- Progress
    current_value DECIMAL(10,2) DEFAULT 0,
    total_value DECIMAL(10,2) DEFAULT 0,
    completion_percentage DECIMAL(5,2) DEFAULT 0,

    -- Daily check-ins
    daily_progress JSONB DEFAULT '[]'::jsonb,
    -- [{"date": "2025-01-15", "value": 5000, "checked_in": true}, ...]

    -- Ranking
    rank INTEGER,
    previous_rank INTEGER,

    -- Status
    status VARCHAR(20) DEFAULT 'active',
    -- 'active', 'completed', 'dropped', 'failed'

    -- Rewards
    rewards_earned JSONB DEFAULT '[]'::jsonb, -- Badge IDs
    xp_earned INTEGER DEFAULT 0,

    -- Timestamps
    joined_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,

    PRIMARY KEY (challenge_id, user_id)
);

CREATE INDEX idx_challenge_participants_rank ON social.challenge_participants(challenge_id, rank);
CREATE INDEX idx_challenge_participants_user ON social.challenge_participants(user_id);


-- ============================================================================
-- RECIPES TABLE
-- ============================================================================
CREATE TABLE social.recipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Media
    main_photo_url VARCHAR(500),
    gallery_photos JSONB DEFAULT '[]'::jsonb,
    video_url VARCHAR(500),

    -- Author
    author_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    author_type VARCHAR(20), -- 'patient', 'nutritionist', 'admin'

    is_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES auth.nutritionists(user_id),
    verified_at TIMESTAMP,

    -- Categories
    meal_type VARCHAR(20), -- 'desayuno', 'colacion', 'comida', 'cena', 'postre', 'bebida'
    cuisine_type VARCHAR(20), -- 'mexicana', 'internacional', 'fusion'

    dietary_tags JSONB DEFAULT '[]'::jsonb,
    -- ["vegetarian", "gluten_free", "low_carb", "diabetic_friendly"]

    -- Difficulty & Time
    difficulty VARCHAR(20), -- 'facil', 'media', 'dificil'
    prep_time_min INTEGER,
    cook_time_min INTEGER,
    total_time_min INTEGER GENERATED ALWAYS AS (prep_time_min + cook_time_min) STORED,
    servings INTEGER,

    -- Cost
    cost_estimate_mxn INTEGER,
    cost_level VARCHAR(20), -- 'economico', 'moderado', 'caro'

    -- Cultural
    is_traditional_mexican BOOLEAN DEFAULT FALSE,
    region_origin VARCHAR(100),
    history_story TEXT,

    -- Ingredients
    ingredients JSONB NOT NULL,
    -- [
    --   {
    --     "name": "Tortilla de maíz",
    --     "quantity": 4,
    --     "unit": "piezas",
    --     "notes": "de preferencia hechas a mano",
    --     "is_optional": false,
    --     "substitutions": ["tortilla de harina integral"]
    --   }
    -- ]

    -- Instructions
    instructions JSONB NOT NULL,
    -- [
    --   {
    --     "step_number": 1,
    --     "instruction": "Calentar el comal a fuego medio",
    --     "photo_url": null,
    --     "duration_min": 2
    --   }
    -- ]

    -- Nutrition per serving
    nutrition_per_serving JSONB,
    -- {
    --   "calories": 350,
    --   "protein_g": 25,
    --   "carbs_g": 40,
    --   "fat_g": 8,
    --   "fiber_g": 6,
    --   "sugar_g": 5,
    --   "sodium_mg": 450,
    --   "equivalents": "2 cereales, 1 carne muy bajo aporte, 1 verdura"
    -- }

    -- Tips
    chef_tips JSONB DEFAULT '[]'::jsonb,
    storage_instructions TEXT,
    reheating_instructions TEXT,

    -- Engagement
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    saves_count INTEGER DEFAULT 0,
    tried_count INTEGER DEFAULT 0,

    rating_average DECIMAL(3,2) DEFAULT 5.0,
    rating_count INTEGER DEFAULT 0,

    -- Collections
    is_featured BOOLEAN DEFAULT FALSE,
    is_trending BOOLEAN DEFAULT FALSE,
    is_seasonal BOOLEAN DEFAULT FALSE,
    season VARCHAR(20),

    -- Moderation
    is_published BOOLEAN DEFAULT FALSE,
    moderation_status VARCHAR(20) DEFAULT 'pending',
    moderation_notes TEXT,

    -- Search
    tags JSONB DEFAULT '[]'::jsonb,
    search_keywords JSONB DEFAULT '[]'::jsonb,

    search_vector tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('spanish', COALESCE(title, '')), 'A') ||
        setweight(to_tsvector('spanish', COALESCE(description, '')), 'B')
    ) STORED,

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_recipes_author ON social.recipes(author_id);
CREATE INDEX idx_recipes_verified ON social.recipes(is_verified);
CREATE INDEX idx_recipes_meal_type ON social.recipes(meal_type);
CREATE INDEX idx_recipes_rating ON social.recipes(rating_average DESC);
CREATE INDEX idx_recipes_search ON social.recipes USING GIN(search_vector);
CREATE INDEX idx_recipes_tags ON social.recipes USING GIN(tags);


-- ============================================================================
-- FAMILY CIRCLES TABLE (Unique feature)
-- ============================================================================
CREATE TABLE social.family_circles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name VARCHAR(255) NOT NULL,
    description TEXT,
    cover_photo_url VARCHAR(500),

    -- Owner (patient who created it)
    owner_id UUID NOT NULL REFERENCES auth.patients(id) ON DELETE CASCADE,

    -- Nutritionist is auto-included
    nutritionist_id UUID NOT NULL REFERENCES auth.nutritionists(user_id),

    -- Privacy Settings
    share_progress_automatically BOOLEAN DEFAULT TRUE,
    share_achievements BOOLEAN DEFAULT TRUE,
    share_meal_logs BOOLEAN DEFAULT FALSE,

    -- Family Challenges
    family_challenges JSONB DEFAULT '[]'::jsonb,

    -- Shared Goals
    family_goals JSONB DEFAULT '[]'::jsonb,

    -- Shared Recipes
    family_recipes UUID[], -- Array of recipe IDs

    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_family_circles_owner ON social.family_circles(owner_id);
CREATE INDEX idx_family_circles_nutritionist ON social.family_circles(nutritionist_id);


-- ============================================================================
-- FAMILY CIRCLE MEMBERS TABLE
-- ============================================================================
CREATE TABLE social.family_circle_members (
    circle_id UUID NOT NULL REFERENCES social.family_circles(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    role VARCHAR(20) DEFAULT 'family_member',
    -- 'owner', 'family_member', 'nutritionist', 'support_friend'

    relationship VARCHAR(50), -- 'esposo', 'mamá', 'hijo', 'mejor amiga'

    -- Permissions
    can_view_progress BOOLEAN DEFAULT TRUE,
    can_view_meal_log BOOLEAN DEFAULT TRUE,
    can_post BOOLEAN DEFAULT TRUE,
    can_comment BOOLEAN DEFAULT TRUE,
    can_give_encouragement BOOLEAN DEFAULT TRUE,

    -- Activity
    joined_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP,

    PRIMARY KEY (circle_id, user_id)
);

CREATE INDEX idx_family_circle_members_user ON social.family_circle_members(user_id);
```

---

## 4. API Specifications

### 4.1 API Design Principles

**RESTful Design:**
- Resource-based URLs (`/api/v1/users/{id}`)
- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Stateless requests (JWT in Authorization header)
- HATEOAS links where appropriate

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

**Error Format:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El email no es válido",
    "details": [
      {"field": "email", "issue": "invalid_format"}
    ]
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### 4.2 Authentication Endpoints

```python
# ============================================================================
# POST /api/v1/auth/register
# ============================================================================
"""
Register new user (self-registration for patients/nutritionists)
"""
Request:
{
  "email": "carlos@example.com",
  "password": "SecurePass123!",
  "first_name": "Carlos",
  "last_name": "Hernández",
  "user_type": "patient",
  "phone": "+52 555 123 4567",
  "date_of_birth": "1985-05-15",
  "gender": "male",
  "state": "CDMX",
  "city": "México"
}

Response (201 Created):
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "email": "carlos@example.com",
      "username": "carlos_hernandez",
      "first_name": "Carlos",
      "last_name": "Hernández",
      "user_type": "patient",
      "email_verified": false
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}


# ============================================================================
# POST /api/v1/auth/login
# ============================================================================
Request:
{
  "email": "carlos@example.com",
  "password": "SecurePass123!"
}

Response (200 OK):
{
  "success": true,
  "data": {
    "user": { ... },
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}


# ============================================================================
# POST /api/v1/auth/refresh
# ============================================================================
Request:
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response (200 OK):
{
  "success": true,
  "data": {
    "access_token": "new_token_here",
    "refresh_token": "new_refresh_token_here",
    "expires_in": 3600
  }
}


# ============================================================================
# POST /api/v1/auth/password/forgot
# ============================================================================
Request:
{
  "email": "carlos@example.com"
}

Response (200 OK):
{
  "success": true,
  "message": "Si el email existe, recibirás instrucciones para restablecer tu contraseña"
}


# ============================================================================
# POST /api/v1/auth/password/reset
# ============================================================================
Request:
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!"
}

Response (200 OK):
{
  "success": true,
  "message": "Contraseña restablecida exitosamente"
}


# ============================================================================
# POST /api/v1/auth/oauth/google
# ============================================================================
Request:
{
  "id_token": "google_oauth_id_token",
  "provider": "google"
}

Response (200 OK):
{
  "success": true,
  "data": {
    "user": { ... },
    "access_token": "...",
    "refresh_token": "...",
    "is_new_user": false
  }
}
```

### 4.3 Social Feed Endpoints

```python
# ============================================================================
# GET /api/v1/feed
# ============================================================================
"""
Get personalized feed for current user (ranked by algorithm)
"""
Query Parameters:
- page: int = 1
- limit: int = 20
- type: str = null  # Filter by post type

Response (200 OK):
{
  "success": true,
  "data": {
    "posts": [
      {
        "id": "uuid",
        "author": {
          "id": "uuid",
          "username": "maria_gomez",
          "full_name": "María Gómez",
          "photo_url": "...",
          "user_type": "patient"
        },
        "type": "progress",
        "body": "¡Perdí 5kg este mes! 🎉",
        "media_urls": ["https://cdn.example.com/post1.jpg"],
        "progress_data": {
          "weight_before_kg": 80.5,
          "weight_after_kg": 75.2,
          "weight_lost_kg": 5.3,
          "time_period_days": 30
        },
        "likes_count": 156,
        "comments_count": 23,
        "shares_count": 8,
        "reactions": {
          "heart": 89,
          "clap": 45,
          "fire": 22
        },
        "has_liked": false,
        "has_saved": false,
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 15,
      "total_items": 300,
      "has_next": true
    }
  }
}


# ============================================================================
# POST /api/v1/posts
# ============================================================================
"""
Create new post (multipart/form-data)
"""
Request (Form Data):
- type: "progress"
- body: "¡Perdí 5kg este mes! 🎉"
- visibility: "public"
- files: [File, File]  # Photos/videos
- progress_data: {"weight_before_kg": 80.5, "weight_after_kg": 75.2}

Response (201 Created):
{
  "success": true,
  "data": {
    "post": { ... }
  }
}


# ============================================================================
# GET /api/v1/posts/{post_id}
# ============================================================================
Response (200 OK):
{
  "success": true,
  "data": {
    "post": { ... },
    "comments": [ ... ]
  }
}


# ============================================================================
# POST /api/v1/posts/{post_id}/reactions
# ============================================================================
Request:
{
  "reaction_type": "heart"  # heart, clap, fire, strong, celebrate
}

Response (201 Created):
{
  "success": true,
  "data": {
    "reaction": {
      "id": "uuid",
      "reaction_type": "heart",
      "created_at": "2025-01-15T10:30:00Z"
    }
  }
}


# ============================================================================
# DELETE /api/v1/posts/{post_id}/reactions
# ============================================================================
Response (204 No Content)


# ============================================================================
# POST /api/v1/posts/{post_id}/comments
# ============================================================================
Request:
{
  "content": "¡Felicidades! 🎉",
  "parent_comment_id": null  # For nested replies
}

Response (201 Created):
{
  "success": true,
  "data": {
    "comment": {
      "id": "uuid",
      "author": { ... },
      "content": "¡Felicidades! 🎉",
      "likes_count": 0,
      "created_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

### 4.4 Patient Management Endpoints

```python
# ============================================================================
# POST /api/v1/nutritionist/patients
# ============================================================================
"""
Nutritionist adds new patient (auto-creates user account)
"""
Request:
{
  "email": "paciente@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "+52 555 987 6543",
  "date_of_birth": "1990-03-20",
  "gender": "male",
  "primary_goal": "weight_loss",
  "target_weight_kg": 75.0,
  "health_conditions": ["diabetes_type_2"],
  "allergies": ["peanuts"],
  "send_welcome_email": true
}

Response (201 Created):
{
  "success": true,
  "data": {
    "patient": {
      "id": "uuid",
      "user_id": "uuid",
      "email": "paciente@example.com",
      "full_name": "Juan Pérez",
      "nutritionist_id": "uuid",
      "status": "active",
      "user_created": true,
      "welcome_email_sent": true,
      "temporary_password_sent": true
    }
  },
  "message": "Paciente creado exitosamente. Se ha enviado un email con instrucciones de acceso."
}


# ============================================================================
# GET /api/v1/nutritionist/patients
# ============================================================================
"""
Get all patients for current nutritionist
"""
Query Parameters:
- status: str = "active"  # active, inactive, all
- search: str = null
- page: int = 1
- limit: int = 20

Response (200 OK):
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": "uuid",
        "full_name": "Juan Pérez",
        "email": "paciente@example.com",
        "photo_url": "...",
        "primary_goal": "weight_loss",
        "status": "active",
        "assigned_at": "2024-12-01T09:00:00Z",
        "last_appointment": "2025-01-10T14:00:00Z",
        "next_appointment": "2025-01-24T14:00:00Z",
        "adherence_rate": 85.5,
        "current_weight_kg": 78.2,
        "target_weight_kg": 75.0,
        "progress_percentage": 45.2
      }
    ],
    "pagination": { ... }
  }
}


# ============================================================================
# GET /api/v1/nutritionist/patients/{patient_id}
# ============================================================================
"""
Get detailed patient information (including clinical record)
"""
Response (200 OK):
{
  "success": true,
  "data": {
    "patient": {
      "id": "uuid",
      "basic_info": { ... },
      "current_metrics": { ... },
      "progress_history": [ ... ],
      "active_meal_plan": { ... },
      "appointments": [ ... ],
      "clinical_notes": [ ... ]
    }
  }
}
```

### 4.5 Recipe Endpoints

```python
# ============================================================================
# GET /api/v1/recipes
# ============================================================================
"""
Search and filter recipes
"""
Query Parameters:
- search: str = null
- meal_type: str = null  # desayuno, colacion, comida, cena
- dietary_tags: str[] = null  # vegetarian, gluten_free, etc.
- max_prep_time_min: int = null
- difficulty: str = null
- is_verified: bool = null
- sort_by: str = "rating"  # rating, created_at, tried_count
- page: int = 1
- limit: int = 20

Response (200 OK):
{
  "success": true,
  "data": {
    "recipes": [
      {
        "id": "uuid",
        "title": "Tacos de Pollo con Nopales",
        "description": "Tacos saludables con pollo y nopales",
        "main_photo_url": "...",
        "author": {
          "id": "uuid",
          "username": "nutriologa_maria",
          "full_name": "Dra. María López",
          "user_type": "nutritionist"
        },
        "is_verified": true,
        "meal_type": "comida",
        "dietary_tags": ["high_protein", "low_carb"],
        "difficulty": "facil",
        "total_time_min": 30,
        "servings": 4,
        "nutrition_per_serving": {
          "calories": 350,
          "protein_g": 25,
          "carbs_g": 40,
          "fat_g": 8
        },
        "rating_average": 4.8,
        "rating_count": 127,
        "tried_count": 89,
        "created_at": "2025-01-10T08:00:00Z"
      }
    ],
    "pagination": { ... }
  }
}


# ============================================================================
# POST /api/v1/recipes
# ============================================================================
"""
Create new recipe (multipart/form-data)
"""
Request:
{
  "title": "Tacos de Pollo con Nopales",
  "description": "...",
  "meal_type": "comida",
  "dietary_tags": ["high_protein"],
  "difficulty": "facil",
  "prep_time_min": 15,
  "cook_time_min": 15,
  "servings": 4,
  "ingredients": [...],
  "instructions": [...],
  "nutrition_per_serving": {...},
  "files": [File]  # Photos
}

Response (201 Created):
{
  "success": true,
  "data": {
    "recipe": { ... },
    "moderation_status": "pending"
  },
  "message": "Receta creada. En revisión para publicación."
}
```

### 4.6 Challenge Endpoints

```python
# ============================================================================
# GET /api/v1/challenges
# ============================================================================
"""
Get available challenges
"""
Query Parameters:
- status: str = "active"  # upcoming, active, completed
- scope: str = null  # national, state, group
- category: str = null  # weight_loss, steps, water
- page: int = 1
- limit: int = 20

Response (200 OK):
{
  "success": true,
  "data": {
    "challenges": [
      {
        "id": "uuid",
        "title": "Reto Nacional: 10,000 Pasos Diarios",
        "description": "Camina 10,000 pasos cada día durante 30 días",
        "banner_image_url": "...",
        "type": "individual",
        "category": "steps",
        "scope": "national",
        "start_date": "2025-02-01",
        "end_date": "2025-03-02",
        "duration_days": 30,
        "status": "upcoming",
        "goal_metric": "steps",
        "goal_value": 10000,
        "goal_type": "daily",
        "participant_count": 1245,
        "max_participants": null,
        "rewards": [
          {
            "rank": 1,
            "reward_type": "badge",
            "reward_value": "campeón_nacional"
          }
        ],
        "is_featured": true,
        "created_by": {
          "id": "uuid",
          "full_name": "Nutrition Intelligence",
          "created_by_type": "system"
        }
      }
    ],
    "pagination": { ... }
  }
}


# ============================================================================
# POST /api/v1/challenges/{challenge_id}/join
# ============================================================================
Request:
{
  "team_id": null  # For team challenges
}

Response (201 Created):
{
  "success": true,
  "data": {
    "participation": {
      "challenge_id": "uuid",
      "user_id": "uuid",
      "status": "active",
      "current_value": 0,
      "completion_percentage": 0,
      "joined_at": "2025-01-15T10:30:00Z"
    }
  },
  "message": "Te has unido al reto exitosamente. ¡Mucha suerte!"
}


# ============================================================================
# POST /api/v1/challenges/{challenge_id}/progress
# ============================================================================
"""
Update challenge progress (daily check-in)
"""
Request:
{
  "date": "2025-01-15",
  "value": 12500  # Steps for the day
}

Response (200 OK):
{
  "success": true,
  "data": {
    "progress": {
      "date": "2025-01-15",
      "value": 12500,
      "goal_achieved": true,
      "total_value": 12500,
      "days_completed": 1,
      "completion_percentage": 3.33,
      "current_rank": 523
    },
    "achievements": [
      {
        "type": "milestone",
        "title": "Primer día completado",
        "xp_earned": 10
      }
    ]
  }
}


# ============================================================================
# GET /api/v1/challenges/{challenge_id}/leaderboard
# ============================================================================
Query Parameters:
- page: int = 1
- limit: int = 50

Response (200 OK):
{
  "success": true,
  "data": {
    "leaderboard": [
      {
        "rank": 1,
        "user": {
          "id": "uuid",
          "username": "carlos_runner",
          "full_name": "Carlos Hernández",
          "photo_url": "...",
          "state": "CDMX"
        },
        "total_value": 385000,
        "days_completed": 30,
        "completion_percentage": 100,
        "average_daily_value": 12833
      }
    ],
    "current_user_position": {
      "rank": 523,
      "total_value": 12500,
      "days_completed": 1
    }
  }
}
```

### 4.7 AI-Powered Endpoints

```python
# ============================================================================
# POST /api/v1/ai/recognize-food
# ============================================================================
"""
AI food recognition from photo (Google Gemini Vision API)
"""
Request (multipart/form-data):
- image: File
- meal_type: "comida"

Response (200 OK):
{
  "success": true,
  "data": {
    "recognized_foods": [
      {
        "name": "Tacos de pollo",
        "confidence": 0.92,
        "quantity": "3 piezas",
        "estimated_nutrition": {
          "calories": 450,
          "protein_g": 30,
          "carbs_g": 45,
          "fat_g": 12
        },
        "equivalents": "2 cereales, 2 carne bajo aporte",
        "alternative_matches": [
          {"name": "Tacos de res", "confidence": 0.65}
        ]
      }
    ],
    "suggestions": [
      "Considera agregar más verduras para balancear el plato"
    ],
    "processing_time_ms": 1250
  }
}


# ============================================================================
# POST /api/v1/ai/scan-label
# ============================================================================
"""
Scan nutrition label (NOM-051) using OCR + Gemini
"""
Request (multipart/form-data):
- image: File

Response (200 OK):
{
  "success": true,
  "data": {
    "product_name": "Cereal Integral Fitness",
    "brand": "Nestlé",
    "serving_size": "30g",
    "servings_per_container": 12,
    "nutrition_per_serving": {
      "calories": 110,
      "protein_g": 2,
      "carbs_g": 24,
      "sugar_g": 8,
      "fat_g": 1,
      "saturated_fat_g": 0.5,
      "fiber_g": 3,
      "sodium_mg": 150
    },
    "nom_051_warnings": [
      "EXCESO AZÚCARES",
      "EXCESO SODIO"
    ],
    "health_score": 6.5,  # Out of 10
    "recommendation": "Moderado. Contiene exceso de azúcares. Considera opciones sin azúcar añadida.",
    "better_alternatives": [
      {
        "product_name": "Avena natural",
        "health_score": 9.2
      }
    ]
  }
}


# ============================================================================
# POST /api/v1/ai/generate-meal-plan
# ============================================================================
"""
AI-generated personalized meal plan (Gemini + nutritional database)
"""
Request:
{
  "patient_id": "uuid",
  "duration_days": 7,
  "calories_target": 1800,
  "dietary_preferences": ["vegetarian"],
  "exclude_foods": ["brócoli"],
  "budget_level": "moderado"
}

Response (200 OK):
{
  "success": true,
  "data": {
    "meal_plan": {
      "id": "uuid",
      "days": [
        {
          "day": 1,
          "date": "2025-01-16",
          "meals": [
            {
              "meal_type": "desayuno",
              "time": "08:00",
              "recipe_id": "uuid",
              "recipe_name": "Avena con Frutos Rojos",
              "portions": 1,
              "nutrition": {...},
              "equivalents": "2 cereales, 1 fruta"
            }
          ],
          "daily_totals": {
            "calories": 1820,
            "protein_g": 90,
            "carbs_g": 220,
            "fat_g": 50
          }
        }
      ],
      "weekly_summary": {...},
      "shopping_list": [...],
      "estimated_cost_mxn": 850
    }
  }
}


# ============================================================================
# POST /api/v1/ai/chat
# ============================================================================
"""
Chatbot nutritionist assistant (Google Gemini)
"""
Request:
{
  "message": "¿Puedo comer plátano si tengo diabetes?",
  "conversation_id": "uuid"  # For context
}

Response (200 OK):
{
  "success": true,
  "data": {
    "response": "Sí, las personas con diabetes pueden comer plátano con moderación. Un plátano mediano contiene aproximadamente 27g de carbohidratos y tiene un índice glucémico medio...",
    "conversation_id": "uuid",
    "sources": [
      "American Diabetes Association Guidelines",
      "NOM-043-SSA2-2012"
    ],
    "related_questions": [
      "¿Cuál es la porción recomendada de plátano?",
      "¿Qué frutas son mejores para la diabetes?"
    ]
  }
}
```

### 4.8 WebSocket Events

```python
# ============================================================================
# WebSocket Connection: /ws
# ============================================================================
"""
Real-time updates via Socket.IO
"""

# Client connects
socket.connect("wss://api.nutritionintelligence.mx/ws", {
  "auth": {"token": "jwt_token_here"}
})


# Server Events (Server → Client)
# ============================================================================

# 1. New Notification
{
  "event": "notification:new",
  "data": {
    "id": "uuid",
    "type": "new_follower",
    "title": "Nuevo seguidor",
    "body": "@maria_gomez comenzó a seguirte",
    "action_url": "/profile/maria_gomez",
    "created_at": "2025-01-15T10:30:00Z"
  }
}

# 2. New Comment on User's Post
{
  "event": "post:new_comment",
  "data": {
    "post_id": "uuid",
    "comment": { ... }
  }
}

# 3. New Reaction on User's Post
{
  "event": "post:new_reaction",
  "data": {
    "post_id": "uuid",
    "reaction_type": "heart",
    "user": { ... }
  }
}

# 4. Challenge Update
{
  "event": "challenge:rank_change",
  "data": {
    "challenge_id": "uuid",
    "old_rank": 525,
    "new_rank": 503,
    "rank_change": 22
  }
}

# 5. Family Circle Activity
{
  "event": "family_circle:new_post",
  "data": {
    "circle_id": "uuid",
    "post": { ... }
  }
}

# 6. Nutritionist Message
{
  "event": "message:new",
  "data": {
    "from": {
      "id": "uuid",
      "full_name": "Dra. Sara Gallegos",
      "user_type": "nutritionist"
    },
    "message": "Hola Juan, vi que ya terminaste tu semana 1. ¡Felicidades!",
    "created_at": "2025-01-15T10:30:00Z"
  }
}


# Client Events (Client → Server)
# ============================================================================

# 1. User is typing
socket.emit("typing:start", {
  "conversation_id": "uuid"
})

# 2. Mark notification as read
socket.emit("notification:read", {
  "notification_id": "uuid"
})

# 3. Join challenge room (for live leaderboard updates)
socket.emit("challenge:join_room", {
  "challenge_id": "uuid"
})
```

---

## 5. Social Media Integration

### 5.1 Overview

Nutrition Intelligence integrates with major social media platforms to enable viral content sharing and community growth. This creates a virtuous cycle:

```
User achieves milestone → Shares to Instagram/TikTok → Friends see success
    → Friends join app → More community engagement → More motivation
```

**Supported Platforms:**
- Instagram (photos, stories, reels)
- TikTok (short videos)
- Facebook (posts, groups integration)
- X/Twitter (text updates, threads)

### 5.2 Instagram Integration

#### 5.2.1 Instagram APIs Used

**Instagram Basic Display API:**
- User authentication via OAuth 2.0
- Access to user's profile info
- Read user's media (photos/videos)

**Instagram Graph API (Business/Creator accounts):**
- Publish photos to feed
- Publish stories
- Publish reels
- Insights and analytics

#### 5.2.2 Database Schema

```sql
-- ============================================================================
-- INSTAGRAM CONNECTIONS TABLE
-- ============================================================================
CREATE TABLE integrations.instagram_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Instagram Account Info
    instagram_user_id VARCHAR(255) UNIQUE NOT NULL,
    instagram_username VARCHAR(255) NOT NULL,
    instagram_display_name VARCHAR(255),
    instagram_profile_picture_url VARCHAR(500),

    account_type VARCHAR(20), -- 'personal', 'business', 'creator'

    -- OAuth Tokens
    access_token TEXT NOT NULL,
    token_type VARCHAR(50) DEFAULT 'Bearer',
    expires_at TIMESTAMP,

    -- Long-lived token (60 days)
    refresh_token TEXT,

    -- Permissions granted
    scopes JSONB DEFAULT '[]'::jsonb,
    -- ["user_profile", "user_media", "instagram_content_publish"]

    -- Settings
    auto_share_progress BOOLEAN DEFAULT FALSE,
    auto_share_recipes BOOLEAN DEFAULT FALSE,
    auto_share_achievements BOOLEAN DEFAULT TRUE,

    share_to_feed BOOLEAN DEFAULT TRUE,
    share_to_stories BOOLEAN DEFAULT FALSE,

    -- Hashtags
    default_hashtags JSONB DEFAULT '["#NutritionIntelligence", "#VidaSaludable", "#México"]'::jsonb,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,

    -- Timestamps
    connected_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    disconnected_at TIMESTAMP
);

CREATE INDEX idx_instagram_connections_user ON integrations.instagram_connections(user_id);
CREATE INDEX idx_instagram_connections_instagram_user ON integrations.instagram_connections(instagram_user_id);


-- ============================================================================
-- INSTAGRAM POSTS TABLE (shared content tracking)
-- ============================================================================
CREATE TABLE integrations.instagram_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    connection_id UUID NOT NULL REFERENCES integrations.instagram_connections(id) ON DELETE CASCADE,

    -- Source post in our app
    source_post_id UUID REFERENCES social.posts(id) ON DELETE SET NULL,
    source_recipe_id UUID REFERENCES social.recipes(id) ON DELETE SET NULL,

    -- Instagram post info
    instagram_media_id VARCHAR(255) UNIQUE NOT NULL,
    instagram_permalink VARCHAR(500),
    instagram_shortcode VARCHAR(50),

    media_type VARCHAR(20), -- 'IMAGE', 'VIDEO', 'CAROUSEL_ALBUM', 'STORY', 'REEL'

    -- Content
    caption TEXT,
    media_url VARCHAR(500),
    thumbnail_url VARCHAR(500),

    -- Engagement (synced periodically)
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'published',
    -- 'publishing', 'published', 'failed', 'deleted'

    error_message TEXT,

    -- Timestamps
    published_at TIMESTAMP DEFAULT NOW(),
    last_synced_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_instagram_posts_user ON integrations.instagram_posts(user_id);
CREATE INDEX idx_instagram_posts_source_post ON integrations.instagram_posts(source_post_id);
CREATE INDEX idx_instagram_posts_instagram_media ON integrations.instagram_posts(instagram_media_id);
```

#### 5.2.3 Implementation

```python
# app/services/social/instagram.py

from typing import Optional, Dict, Any
import httpx
from app.core.config import settings
from app.models.user import User
from app.models.instagram_connection import InstagramConnection
import logging

logger = logging.getLogger(__name__)


class InstagramService:
    """
    Service for Instagram integration using Instagram Graph API
    """

    BASE_URL = "https://graph.instagram.com"
    GRAPH_API_VERSION = "v18.0"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)


    async def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate Instagram OAuth authorization URL
        """
        params = {
            "client_id": settings.INSTAGRAM_APP_ID,
            "redirect_uri": redirect_uri,
            "scope": "user_profile,user_media,instagram_content_publish",
            "response_type": "code",
            "state": state
        }

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"https://api.instagram.com/oauth/authorize?{query_string}"


    async def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        """
        response = await self.client.post(
            "https://api.instagram.com/oauth/access_token",
            data={
                "client_id": settings.INSTAGRAM_APP_ID,
                "client_secret": settings.INSTAGRAM_APP_SECRET,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "code": code
            }
        )
        response.raise_for_status()
        return response.json()


    async def get_long_lived_token(self, short_lived_token: str) -> Dict[str, Any]:
        """
        Exchange short-lived token (1 hour) for long-lived token (60 days)
        """
        response = await self.client.get(
            f"{self.BASE_URL}/access_token",
            params={
                "grant_type": "ig_exchange_token",
                "client_secret": settings.INSTAGRAM_APP_SECRET,
                "access_token": short_lived_token
            }
        )
        response.raise_for_status()
        return response.json()


    async def refresh_token(self, access_token: str) -> Dict[str, Any]:
        """
        Refresh long-lived token (extends for another 60 days)
        """
        response = await self.client.get(
            f"{self.BASE_URL}/refresh_access_token",
            params={
                "grant_type": "ig_refresh_token",
                "access_token": access_token
            }
        )
        response.raise_for_status()
        return response.json()


    async def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        """
        Get Instagram user profile info
        """
        response = await self.client.get(
            f"{self.BASE_URL}/me",
            params={
                "fields": "id,username,account_type,media_count",
                "access_token": access_token
            }
        )
        response.raise_for_status()
        return response.json()


    async def publish_photo(
        self,
        connection: InstagramConnection,
        image_url: str,
        caption: str,
        hashtags: list[str] = None
    ) -> Dict[str, Any]:
        """
        Publish photo to Instagram feed (Business/Creator accounts only)

        Two-step process:
        1. Create media container
        2. Publish media container
        """
        try:
            # Step 1: Create container
            full_caption = self._build_caption(caption, hashtags or connection.default_hashtags)

            container_response = await self.client.post(
                f"{self.BASE_URL}/{connection.instagram_user_id}/media",
                params={
                    "image_url": image_url,
                    "caption": full_caption,
                    "access_token": connection.access_token
                }
            )
            container_response.raise_for_status()
            container_data = container_response.json()
            creation_id = container_data["id"]

            # Step 2: Publish container
            publish_response = await self.client.post(
                f"{self.BASE_URL}/{connection.instagram_user_id}/media_publish",
                params={
                    "creation_id": creation_id,
                    "access_token": connection.access_token
                }
            )
            publish_response.raise_for_status()
            publish_data = publish_response.json()

            logger.info(f"Published to Instagram: {publish_data['id']}")

            return {
                "instagram_media_id": publish_data["id"],
                "status": "published"
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"Instagram API error: {e.response.text}")
            raise


    async def publish_story(
        self,
        connection: InstagramConnection,
        image_url: str,
        sticker_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Publish photo to Instagram Stories
        """
        params = {
            "image_url": image_url,
            "media_type": "STORIES",
            "access_token": connection.access_token
        }

        response = await self.client.post(
            f"{self.BASE_URL}/{connection.instagram_user_id}/media",
            params=params
        )
        response.raise_for_status()

        # Publish
        container_id = response.json()["id"]
        publish_response = await self.client.post(
            f"{self.BASE_URL}/{connection.instagram_user_id}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": connection.access_token
            }
        )
        publish_response.raise_for_status()

        return publish_response.json()


    async def get_media_insights(
        self,
        connection: InstagramConnection,
        media_id: str
    ) -> Dict[str, Any]:
        """
        Get engagement metrics for published media
        """
        response = await self.client.get(
            f"{self.BASE_URL}/{media_id}",
            params={
                "fields": "like_count,comments_count,timestamp,media_url,permalink",
                "access_token": connection.access_token
            }
        )
        response.raise_for_status()
        return response.json()


    def _build_caption(self, caption: str, hashtags: list[str]) -> str:
        """
        Build caption with hashtags
        """
        hashtag_str = " ".join(f"#{tag}" for tag in hashtags if not tag.startswith("#"))
        return f"{caption}\n\n{hashtag_str}"


# Celery task for async publishing
@celery_app.task(name="share_to_instagram")
def share_to_instagram_task(user_id: str, post_id: str):
    """
    Background task to share post to Instagram
    """
    instagram_service = InstagramService()

    # Get user's Instagram connection
    connection = InstagramConnection.get_by_user_id(user_id)

    if not connection or not connection.is_active:
        logger.warning(f"No active Instagram connection for user {user_id}")
        return

    # Get post details
    post = Post.get_by_id(post_id)

    # Publish to Instagram
    result = await instagram_service.publish_photo(
        connection=connection,
        image_url=post.media_urls[0],
        caption=post.body,
        hashtags=connection.default_hashtags
    )

    # Save record
    InstagramPost.create({
        "user_id": user_id,
        "connection_id": connection.id,
        "source_post_id": post_id,
        "instagram_media_id": result["instagram_media_id"],
        "status": "published"
    })
```

#### 5.2.4 API Endpoints

```python
# ============================================================================
# POST /api/v1/integrations/instagram/connect
# ============================================================================
"""
Initiate Instagram OAuth flow
"""
Request:
{
  "redirect_uri": "https://app.nutritionintelligence.mx/settings/integrations/instagram/callback"
}

Response (200 OK):
{
  "success": true,
  "data": {
    "authorization_url": "https://api.instagram.com/oauth/authorize?client_id=...",
    "state": "random_state_token"
  }
}


# ============================================================================
# GET /api/v1/integrations/instagram/callback
# ============================================================================
"""
OAuth callback (handles code exchange)
"""
Query Parameters:
- code: str
- state: str

Response (302 Redirect to app with success message)


# ============================================================================
# GET /api/v1/integrations/instagram/status
# ============================================================================
"""
Get current Instagram connection status
"""
Response (200 OK):
{
  "success": true,
  "data": {
    "connected": true,
    "connection": {
      "instagram_username": "carlos_saludable",
      "account_type": "personal",
      "connected_at": "2025-01-10T09:00:00Z",
      "auto_share_progress": true,
      "auto_share_achievements": true
    }
  }
}


# ============================================================================
# POST /api/v1/integrations/instagram/share
# ============================================================================
"""
Manually share a post to Instagram
"""
Request:
{
  "post_id": "uuid",
  "share_to_feed": true,
  "share_to_stories": false,
  "custom_caption": "Optional custom caption override",
  "hashtags": ["#México", "#Salud"]
}

Response (202 Accepted):
{
  "success": true,
  "message": "Tu publicación se está compartiendo en Instagram",
  "data": {
    "job_id": "uuid",
    "estimated_time_seconds": 5
  }
}


# ============================================================================
# DELETE /api/v1/integrations/instagram/disconnect
# ============================================================================
Response (200 OK):
{
  "success": true,
  "message": "Instagram desconectado exitosamente"
}
```

### 5.3 TikTok Integration

#### 5.3.1 TikTok APIs Used

**TikTok Login Kit:**
- User authentication via OAuth 2.0
- Access to user profile

**TikTok Content Posting API:**
- Upload videos directly to TikTok
- Schedule posts
- Add captions, hashtags, privacy settings

#### 5.3.2 Database Schema

```sql
-- ============================================================================
-- TIKTOK CONNECTIONS TABLE
-- ============================================================================
CREATE TABLE integrations.tiktok_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- TikTok Account Info
    tiktok_open_id VARCHAR(255) UNIQUE NOT NULL,
    tiktok_username VARCHAR(255) NOT NULL,
    tiktok_display_name VARCHAR(255),
    tiktok_avatar_url VARCHAR(500),

    -- OAuth Tokens
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at TIMESTAMP,

    -- Permissions
    scopes JSONB DEFAULT '[]'::jsonb,
    -- ["user.info.basic", "video.upload", "video.publish"]

    -- Settings
    auto_share_recipes BOOLEAN DEFAULT TRUE,
    auto_share_transformations BOOLEAN DEFAULT TRUE,

    -- Video Settings
    default_privacy VARCHAR(20) DEFAULT 'PUBLIC_TO_EVERYONE',
    -- 'PUBLIC_TO_EVERYONE', 'MUTUAL_FOLLOW_FRIENDS', 'SELF_ONLY'

    allow_comments BOOLEAN DEFAULT TRUE,
    allow_duet BOOLEAN DEFAULT TRUE,
    allow_stitch BOOLEAN DEFAULT TRUE,

    default_hashtags JSONB DEFAULT '["#NutritionIntelligence", "#Nutrición", "#México"]'::jsonb,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,

    -- Timestamps
    connected_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    disconnected_at TIMESTAMP
);

CREATE INDEX idx_tiktok_connections_user ON integrations.tiktok_connections(user_id);


-- ============================================================================
-- TIKTOK VIDEOS TABLE
-- ============================================================================
CREATE TABLE integrations.tiktok_videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    connection_id UUID NOT NULL REFERENCES integrations.tiktok_connections(id) ON DELETE CASCADE,

    -- Source
    source_recipe_id UUID REFERENCES social.recipes(id) ON DELETE SET NULL,
    source_post_id UUID REFERENCES social.posts(id) ON DELETE SET NULL,

    -- TikTok video info
    tiktok_video_id VARCHAR(255) UNIQUE,
    tiktok_share_url VARCHAR(500),

    -- Content
    caption TEXT,
    video_url VARCHAR(500),
    cover_image_url VARCHAR(500),

    duration_seconds INTEGER,

    -- Engagement (synced periodically)
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'uploading',
    -- 'uploading', 'processing', 'published', 'failed', 'deleted'

    publish_status VARCHAR(50), -- TikTok's status
    error_message TEXT,

    -- Timestamps
    uploaded_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP,
    last_synced_at TIMESTAMP
);

CREATE INDEX idx_tiktok_videos_user ON integrations.tiktok_videos(user_id);
CREATE INDEX idx_tiktok_videos_source_recipe ON integrations.tiktok_videos(source_recipe_id);
```

#### 5.3.3 Implementation

```python
# app/services/social/tiktok.py

from typing import Optional, Dict, Any
import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TikTokService:
    """
    Service for TikTok integration using TikTok Content Posting API
    """

    BASE_URL = "https://open.tiktokapis.com"
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)  # Video uploads need more time


    async def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate TikTok OAuth authorization URL
        """
        params = {
            "client_key": settings.TIKTOK_CLIENT_KEY,
            "redirect_uri": redirect_uri,
            "scope": "user.info.basic,video.upload,video.publish",
            "response_type": "code",
            "state": state
        }

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query_string}"


    async def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        """
        response = await self.client.post(
            f"{self.BASE_URL}/v2/oauth/token/",
            json={
                "client_key": settings.TIKTOK_CLIENT_KEY,
                "client_secret": settings.TIKTOK_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
        )
        response.raise_for_status()
        return response.json()["data"]


    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token
        """
        response = await self.client.post(
            f"{self.BASE_URL}/v2/oauth/token/",
            json={
                "client_key": settings.TIKTOK_CLIENT_KEY,
                "client_secret": settings.TIKTOK_CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
        )
        response.raise_for_status()
        return response.json()["data"]


    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Get TikTok user profile info
        """
        response = await self.client.get(
            f"{self.BASE_URL}/v2/user/info/",
            params={"fields": "open_id,union_id,avatar_url,display_name"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        response.raise_for_status()
        return response.json()["data"]["user"]


    async def upload_video(
        self,
        connection: TikTokConnection,
        video_url: str,
        caption: str,
        hashtags: list[str] = None,
        privacy_level: str = "PUBLIC_TO_EVERYONE"
    ) -> Dict[str, Any]:
        """
        Upload and publish video to TikTok

        Process:
        1. Initialize upload
        2. Upload video chunks
        3. Publish video
        """
        try:
            # Build caption with hashtags
            full_caption = self._build_caption(caption, hashtags or connection.default_hashtags)

            # Step 1: Initialize upload
            init_response = await self.client.post(
                f"{self.BASE_URL}/v2/post/publish/video/init/",
                json={
                    "post_info": {
                        "title": full_caption,
                        "privacy_level": privacy_level,
                        "disable_comment": not connection.allow_comments,
                        "disable_duet": not connection.allow_duet,
                        "disable_stitch": not connection.allow_stitch,
                        "video_cover_timestamp_ms": 1000  # Cover at 1 second
                    },
                    "source_info": {
                        "source": "PULL_FROM_URL",
                        "video_url": video_url
                    }
                },
                headers={"Authorization": f"Bearer {connection.access_token}"}
            )
            init_response.raise_for_status()
            init_data = init_response.json()["data"]

            publish_id = init_data["publish_id"]

            logger.info(f"TikTok video upload initiated: {publish_id}")

            # Return publish_id for status polling
            return {
                "publish_id": publish_id,
                "status": "uploading"
            }

        except httpx.HTTPStatusError as e:
            logger.error(f"TikTok API error: {e.response.text}")
            raise


    async def get_publish_status(
        self,
        connection: TikTokConnection,
        publish_id: str
    ) -> Dict[str, Any]:
        """
        Check video publish status
        """
        response = await self.client.post(
            f"{self.BASE_URL}/v2/post/publish/status/fetch/",
            json={"publish_id": publish_id},
            headers={"Authorization": f"Bearer {connection.access_token}"}
        )
        response.raise_for_status()
        return response.json()["data"]


    def _build_caption(self, caption: str, hashtags: list[str]) -> str:
        """
        Build caption with hashtags (max 150 chars for TikTok)
        """
        hashtag_str = " ".join(f"#{tag}" for tag in hashtags if not tag.startswith("#"))
        full_caption = f"{caption} {hashtag_str}"

        # TikTok caption limit
        if len(full_caption) > 150:
            # Truncate caption, keep hashtags
            max_caption_len = 150 - len(hashtag_str) - 1
            caption = caption[:max_caption_len]
            full_caption = f"{caption} {hashtag_str}"

        return full_caption


# Celery task
@celery_app.task(name="share_to_tiktok")
async def share_to_tiktok_task(user_id: str, recipe_id: str):
    """
    Background task to share recipe video to TikTok
    """
    tiktok_service = TikTokService()

    connection = TikTokConnection.get_by_user_id(user_id)
    recipe = Recipe.get_by_id(recipe_id)

    if not recipe.video_url:
        logger.warning(f"Recipe {recipe_id} has no video")
        return

    # Upload video
    result = await tiktok_service.upload_video(
        connection=connection,
        video_url=recipe.video_url,
        caption=recipe.title,
        hashtags=connection.default_hashtags
    )

    # Save record
    TikTokVideo.create({
        "user_id": user_id,
        "connection_id": connection.id,
        "source_recipe_id": recipe_id,
        "publish_id": result["publish_id"],
        "status": "uploading"
    })
```

### 5.4 Facebook Integration

#### 5.4.1 Facebook APIs Used

**Facebook Login:**
- User authentication
- Profile access

**Facebook Graph API:**
- Post to user's timeline
- Post to Facebook Pages
- Post to Facebook Groups
- Insights and analytics

#### 5.4.2 Database Schema

```sql
-- ============================================================================
-- FACEBOOK CONNECTIONS TABLE
-- ============================================================================
CREATE TABLE integrations.facebook_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Facebook Account Info
    facebook_user_id VARCHAR(255) UNIQUE NOT NULL,
    facebook_name VARCHAR(255) NOT NULL,
    facebook_email VARCHAR(255),
    facebook_picture_url VARCHAR(500),

    -- OAuth Tokens
    access_token TEXT NOT NULL,
    token_type VARCHAR(50) DEFAULT 'Bearer',
    expires_at TIMESTAMP,

    -- Long-lived token
    long_lived_token TEXT,

    -- Permissions
    scopes JSONB DEFAULT '[]'::jsonb,
    -- ["public_profile", "email", "publish_to_groups", "pages_manage_posts"]

    -- Connected Pages
    pages JSONB DEFAULT '[]'::jsonb,
    -- [{"id": "123", "name": "Mi Página de Nutrición", "access_token": "..."}]

    -- Settings
    auto_share_progress BOOLEAN DEFAULT TRUE,
    auto_share_recipes BOOLEAN DEFAULT FALSE,
    auto_share_achievements BOOLEAN DEFAULT TRUE,

    share_to_timeline BOOLEAN DEFAULT TRUE,
    share_to_page_id VARCHAR(255), -- If user wants to share to their page

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,

    -- Timestamps
    connected_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    disconnected_at TIMESTAMP
);

CREATE INDEX idx_facebook_connections_user ON integrations.facebook_connections(user_id);


-- ============================================================================
-- FACEBOOK POSTS TABLE
-- ============================================================================
CREATE TABLE integrations.facebook_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    connection_id UUID NOT NULL REFERENCES integrations.facebook_connections(id) ON DELETE CASCADE,

    -- Source
    source_post_id UUID REFERENCES social.posts(id) ON DELETE SET NULL,
    source_recipe_id UUID REFERENCES social.recipes(id) ON DELETE SET NULL,

    -- Facebook post info
    facebook_post_id VARCHAR(255) UNIQUE NOT NULL,
    facebook_permalink VARCHAR(500),

    -- Where it was posted
    posted_to VARCHAR(20), -- 'timeline', 'page', 'group'
    page_id VARCHAR(255),
    group_id VARCHAR(255),

    -- Content
    message TEXT,
    link VARCHAR(500),
    picture VARCHAR(500),

    -- Engagement (synced periodically)
    reactions_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    shares_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'published',
    error_message TEXT,

    -- Timestamps
    published_at TIMESTAMP DEFAULT NOW(),
    last_synced_at TIMESTAMP
);

CREATE INDEX idx_facebook_posts_user ON integrations.facebook_posts(user_id);
CREATE INDEX idx_facebook_posts_source_post ON integrations.facebook_posts(source_post_id);
```

#### 5.4.3 Implementation

```python
# app/services/social/facebook.py

class FacebookService:
    """
    Service for Facebook integration using Facebook Graph API
    """

    BASE_URL = "https://graph.facebook.com"
    API_VERSION = "v18.0"

    async def publish_post(
        self,
        connection: FacebookConnection,
        message: str,
        image_url: Optional[str] = None,
        link: Optional[str] = None,
        target: str = "timeline"  # or "page"
    ) -> Dict[str, Any]:
        """
        Publish post to Facebook timeline or page
        """
        endpoint = f"{connection.facebook_user_id}/feed"
        access_token = connection.access_token

        if target == "page" and connection.share_to_page_id:
            # Post to page instead
            page = next(
                (p for p in connection.pages if p["id"] == connection.share_to_page_id),
                None
            )
            if page:
                endpoint = f"{page['id']}/feed"
                access_token = page["access_token"]

        payload = {
            "message": message,
            "access_token": access_token
        }

        if image_url:
            payload["picture"] = image_url

        if link:
            payload["link"] = link

        response = await self.client.post(
            f"{self.BASE_URL}/{self.API_VERSION}/{endpoint}",
            data=payload
        )
        response.raise_for_status()

        return response.json()  # {"id": "user_id_post_id"}
```

### 5.5 X (Twitter) Integration

#### 5.5.1 X APIs Used

**X API v2:**
- OAuth 2.0 with PKCE
- Post tweets (text + media)
- Create threads
- Upload media

#### 5.5.2 Database Schema

```sql
-- ============================================================================
-- TWITTER CONNECTIONS TABLE
-- ============================================================================
CREATE TABLE integrations.twitter_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Twitter/X Account Info
    twitter_user_id VARCHAR(255) UNIQUE NOT NULL,
    twitter_username VARCHAR(255) NOT NULL,
    twitter_name VARCHAR(255),
    twitter_profile_image_url VARCHAR(500),

    -- OAuth 2.0 Tokens
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMP,

    -- Permissions
    scopes JSONB DEFAULT '["tweet.read", "tweet.write", "users.read"]'::jsonb,

    -- Settings
    auto_share_milestones BOOLEAN DEFAULT TRUE,
    auto_share_achievements BOOLEAN DEFAULT TRUE,

    default_hashtags JSONB DEFAULT '["#MéxicoSaludable", "#Nutrición"]'::jsonb,

    -- Threading
    create_threads BOOLEAN DEFAULT FALSE, -- For longer updates

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP,

    -- Timestamps
    connected_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    disconnected_at TIMESTAMP
);

CREATE INDEX idx_twitter_connections_user ON integrations.twitter_connections(user_id);


-- ============================================================================
-- TWITTER TWEETS TABLE
-- ============================================================================
CREATE TABLE integrations.twitter_tweets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    connection_id UUID NOT NULL REFERENCES integrations.twitter_connections(id) ON DELETE CASCADE,

    -- Source
    source_post_id UUID REFERENCES social.posts(id) ON DELETE SET NULL,

    -- Twitter tweet info
    twitter_tweet_id VARCHAR(255) UNIQUE NOT NULL,
    twitter_url VARCHAR(500),

    -- Content
    text TEXT NOT NULL,
    media_keys JSONB, -- Array of media keys if photos attached

    -- Thread
    is_thread BOOLEAN DEFAULT FALSE,
    thread_tweets JSONB, -- Array of tweet IDs if it's a thread

    -- Engagement (synced periodically)
    retweet_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    quote_count INTEGER DEFAULT 0,
    impression_count INTEGER DEFAULT 0,

    -- Status
    status VARCHAR(20) DEFAULT 'published',
    error_message TEXT,

    -- Timestamps
    published_at TIMESTAMP DEFAULT NOW(),
    last_synced_at TIMESTAMP
);

CREATE INDEX idx_twitter_tweets_user ON integrations.twitter_tweets(user_id);
```

#### 5.5.3 Implementation

```python
# app/services/social/twitter.py

class TwitterService:
    """
    Service for X (Twitter) integration using Twitter API v2
    """

    BASE_URL = "https://api.twitter.com/2"

    async def create_tweet(
        self,
        connection: TwitterConnection,
        text: str,
        media_ids: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a tweet (X post)
        """
        payload = {"text": text}

        if media_ids:
            payload["media"] = {"media_ids": media_ids}

        response = await self.client.post(
            f"{self.BASE_URL}/tweets",
            json=payload,
            headers={"Authorization": f"Bearer {connection.access_token}"}
        )
        response.raise_for_status()

        return response.json()["data"]  # {"id": "...", "text": "..."}


    async def upload_media(
        self,
        connection: TwitterConnection,
        media_url: str
    ) -> str:
        """
        Upload media to Twitter (returns media_id)
        """
        # Download media first
        media_response = await self.client.get(media_url)
        media_bytes = media_response.content

        # Upload to Twitter
        upload_response = await self.client.post(
            "https://upload.twitter.com/1.1/media/upload.json",
            files={"media": media_bytes},
            headers={"Authorization": f"Bearer {connection.access_token}"}
        )
        upload_response.raise_for_status()

        return upload_response.json()["media_id_string"]
```

### 5.6 Cross-Platform Sharing Strategy

#### 5.6.1 Auto-Share Rules

```python
# app/services/social/cross_platform_service.py

class CrossPlatformSharingService:
    """
    Orchestrates sharing across multiple platforms based on content type
    """

    SHARING_RULES = {
        "progress": {
            "instagram": {"feed": True, "stories": True},
            "facebook": {"timeline": True},
            "twitter": {"tweet": True},
            "tiktok": False  # No auto-share for progress (no video)
        },
        "recipe": {
            "instagram": {"feed": True, "stories": False},
            "facebook": {"timeline": True, "page": True},
            "twitter": {"tweet": True},
            "tiktok": {"video": True}  # If recipe has video
        },
        "achievement": {
            "instagram": {"feed": False, "stories": True},
            "facebook": {"timeline": True},
            "twitter": {"tweet": True},
            "tiktok": False
        },
        "transformation": {
            "instagram": {"feed": True, "stories": True, "reels": True},
            "facebook": {"timeline": True, "page": True},
            "twitter": {"tweet": True},
            "tiktok": {"video": True}
        }
    }


    async def auto_share_post(self, post: Post, user: User):
        """
        Automatically share post to connected platforms based on user settings
        """
        # Get user's active connections
        connections = await self.get_active_connections(user.id)

        # Get sharing rules for this post type
        rules = self.SHARING_RULES.get(post.type, {})

        # Queue sharing tasks
        tasks = []

        for platform, platform_rules in rules.items():
            if platform not in connections:
                continue

            connection = connections[platform]

            if not self.should_auto_share(connection, post.type):
                continue

            # Queue async task
            if platform == "instagram":
                if platform_rules.get("feed"):
                    tasks.append(share_to_instagram_task.delay(user.id, post.id))
                if platform_rules.get("stories"):
                    tasks.append(share_to_instagram_stories_task.delay(user.id, post.id))

            elif platform == "facebook":
                tasks.append(share_to_facebook_task.delay(user.id, post.id))

            elif platform == "twitter":
                tasks.append(share_to_twitter_task.delay(user.id, post.id))

            elif platform == "tiktok" and post.video_url:
                tasks.append(share_to_tiktok_task.delay(user.id, post.id))

        return tasks
```

---

## 6. AI/ML Pipeline with Google Gemini

### 6.1 Overview

Nutrition Intelligence leverages **Google Gemini** as its primary AI engine, integrated with Google Workspace for enhanced capabilities. This provides:

- **Multimodal AI**: Process text, images, and structured data
- **Mexican Food Recognition**: Custom-trained models for local cuisine
- **NOM-051 Label Scanning**: OCR + AI for Mexican nutrition labels
- **Personalized Meal Plans**: AI-generated diet recommendations
- **Chatbot Assistant**: Conversational nutrition guidance
- **Predictive Analytics**: Health trend forecasting

**Why Google Gemini:**
- User has Google Workspace access
- Multimodal capabilities (text + vision)
- Better Spanish language support than GPT-4
- Integration with Google Cloud ecosystem
- Cost-effective for high-volume usage

### 6.2 Google Gemini Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATIONS                             │
│             (React Web, React Native iOS/Android)                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FASTAPI BACKEND                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │               AI SERVICE LAYER                             │    │
│  │                                                            │    │
│  │  • FoodRecognitionService   (Gemini Vision)              │    │
│  │  • LabelScannerService      (Gemini Vision + OCR)        │    │
│  │  • MealPlanGeneratorService (Gemini Pro)                 │    │
│  │  • ChatbotService           (Gemini Pro)                 │    │
│  │  • PredictionService        (Gemini Pro + Custom Models) │    │
│  └────────────────────────────────────────────────────────────┘    │
│                             │                                        │
└─────────────────────────────┼────────────────────────────────────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │   Gemini    │  │   Google    │  │  PostgreSQL │
    │  Pro API    │  │Cloud Vision │  │  (Training  │
    │   (Text)    │  │  API (OCR)  │  │    Data)    │
    └─────────────┘  └─────────────┘  └─────────────┘
             │               │               │
             └───────────────┼───────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Google Cloud   │
                    │    Storage      │
                    │  (Model Cache)  │
                    └─────────────────┘
```

### 6.3 Gemini API Setup

```python
# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Google Gemini Configuration
    GOOGLE_API_KEY: str  # From Google AI Studio
    GEMINI_PRO_MODEL: str = "gemini-1.5-pro-latest"
    GEMINI_VISION_MODEL: str = "gemini-1.5-pro-vision-latest"
    GEMINI_FLASH_MODEL: str = "gemini-1.5-flash-latest"  # For faster responses

    # Google Cloud Project (for Workspace integration)
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_CLOUD_LOCATION: str = "us-central1"

    # Google Workspace
    GOOGLE_WORKSPACE_DOMAIN: str  # e.g., "nutritionintelligence.mx"
    GOOGLE_ADMIN_EMAIL: str

    # Model Configuration
    GEMINI_TEMPERATURE: float = 0.7  # Creativity level
    GEMINI_TOP_P: float = 0.95
    GEMINI_TOP_K: int = 40
    GEMINI_MAX_OUTPUT_TOKENS: int = 2048

    # Rate Limits
    GEMINI_REQUESTS_PER_MINUTE: int = 60
    GEMINI_REQUESTS_PER_DAY: int = 1500

    class Config:
        env_file = ".env"


settings = Settings()
```

### 6.4 Gemini Client Wrapper

```python
# app/services/ai/gemini_client.py

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from typing import Optional, List, Dict, Any
import base64
import asyncio
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)


class GeminiClient:
    """
    Wrapper for Google Gemini API with rate limiting and error handling
    """

    def __init__(self):
        self.pro_model = genai.GenerativeModel(settings.GEMINI_PRO_MODEL)
        self.vision_model = genai.GenerativeModel(settings.GEMINI_VISION_MODEL)
        self.flash_model = genai.GenerativeModel(settings.GEMINI_FLASH_MODEL)

        # Safety settings (allow health/medical content)
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }

        # Generation config
        self.generation_config = genai.types.GenerationConfig(
            temperature=settings.GEMINI_TEMPERATURE,
            top_p=settings.GEMINI_TOP_P,
            top_k=settings.GEMINI_TOP_K,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
        )


    async def generate_text(
        self,
        prompt: str,
        model: str = "pro",  # "pro", "vision", "flash"
        system_instruction: Optional[str] = None,
        max_retries: int = 3
    ) -> str:
        """
        Generate text using Gemini Pro
        """
        model_instance = self._get_model(model)

        if system_instruction:
            # Prepend system instruction to prompt
            full_prompt = f"{system_instruction}\n\n{prompt}"
        else:
            full_prompt = prompt

        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    model_instance.generate_content,
                    full_prompt,
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings
                )

                # Check if response was blocked
                if not response.candidates:
                    logger.warning("Gemini response blocked by safety filters")
                    return "Lo siento, no puedo generar una respuesta para eso."

                return response.text

            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff


    async def generate_text_with_image(
        self,
        prompt: str,
        image_data: bytes,
        mime_type: str = "image/jpeg"
    ) -> str:
        """
        Generate text from text + image using Gemini Vision
        """
        try:
            # Prepare image part
            image_part = {
                "mime_type": mime_type,
                "data": image_data
            }

            response = await asyncio.to_thread(
                self.vision_model.generate_content,
                [prompt, image_part],
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            return response.text

        except Exception as e:
            logger.error(f"Gemini Vision API error: {e}")
            raise


    async def analyze_image(
        self,
        image_data: bytes,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze image and return structured output

        Args:
            image_data: Image bytes
            task: "food_recognition", "label_scan", "progress_photo"
            context: Additional context (e.g., user preferences, allergies)
        """
        prompts = {
            "food_recognition": """
                Analiza esta foto de comida y proporciona la siguiente información en formato JSON:
                {
                  "foods": [
                    {
                      "name": "Nombre del alimento en español",
                      "quantity": "Cantidad estimada (ej: 3 piezas, 1 taza)",
                      "confidence": 0.95,
                      "is_mexican_food": true,
                      "estimated_calories": 450,
                      "macros": {
                        "protein_g": 25,
                        "carbs_g": 45,
                        "fat_g": 12,
                        "fiber_g": 5
                      }
                    }
                  ],
                  "meal_type": "comida",
                  "presentation_quality": "home_cooked",
                  "suggestions": ["Agrega más verduras", "Reduce el aceite"]
                }

                Enfócate especialmente en comida mexicana tradicional como tacos, tamales, mole, pozole, etc.
                Sé preciso con las porciones típicas mexicanas.
            """,

            "label_scan": """
                Extrae la información nutricional de esta etiqueta (NOM-051 México).
                Devuelve JSON con:
                {
                  "product_name": "",
                  "brand": "",
                  "serving_size": "",
                  "servings_per_container": 0,
                  "nutrition_per_serving": {
                    "calories": 0,
                    "protein_g": 0,
                    "carbs_g": 0,
                    "sugar_g": 0,
                    "fat_g": 0,
                    "saturated_fat_g": 0,
                    "trans_fat_g": 0,
                    "fiber_g": 0,
                    "sodium_mg": 0
                  },
                  "nom_051_warnings": ["EXCESO CALORÍAS", "EXCESO AZÚCARES"],
                  "ingredients_list": [],
                  "allergens": []
                }
            """,

            "progress_photo": """
                Analiza esta foto de progreso físico y estima:
                {
                  "photo_type": "before" o "after" o "comparison",
                  "visible_changes": ["pérdida de grasa abdominal", "mayor definición muscular"],
                  "body_composition_estimate": {
                    "body_fat_percentage_range": "25-30%",
                    "muscle_tone": "moderado"
                  },
                  "motivation_message": "Mensaje motivacional en español",
                  "recommendations": ["Continúa con cardio", "Aumenta proteína"]
                }
            """
        }

        prompt = prompts.get(task, prompts["food_recognition"])

        # Add context if provided
        if context:
            prompt = f"Contexto del usuario: {context}\n\n{prompt}"

        response_text = await self.generate_text_with_image(prompt, image_data)

        # Parse JSON from response
        import json
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse Gemini JSON response: {response_text}")
            return {"error": "Failed to parse response", "raw_text": response_text}


    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Multi-turn conversation with Gemini

        Args:
            messages: List of {"role": "user"|"model", "content": "..."}
            system_instruction: System prompt for behavior
        """
        chat = self.pro_model.start_chat(history=[])

        # Add system instruction as first message if provided
        if system_instruction:
            chat.send_message(system_instruction)

        # Send conversation history
        for msg in messages[:-1]:  # All except last
            if msg["role"] == "user":
                chat.send_message(msg["content"])

        # Send final user message and get response
        response = await asyncio.to_thread(
            chat.send_message,
            messages[-1]["content"],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

        return response.text


    def _get_model(self, model_type: str):
        """Get model instance by type"""
        models = {
            "pro": self.pro_model,
            "vision": self.vision_model,
            "flash": self.flash_model
        }
        return models.get(model_type, self.pro_model)


# Singleton instance
gemini_client = GeminiClient()
```

### 6.5 Food Recognition Service

```python
# app/services/ai/food_recognition.py

from app.services.ai.gemini_client import gemini_client
from app.models.user import User
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class FoodRecognitionService:
    """
    AI-powered food recognition optimized for Mexican cuisine
    """

    # Mexican food database (top 100 most common foods)
    MEXICAN_FOODS_DB = {
        "tacos": {"base_calories_per_unit": 150, "typical_macros": {"protein": 8, "carbs": 18, "fat": 6}},
        "tamales": {"base_calories_per_unit": 280, "typical_macros": {"protein": 8, "carbs": 35, "fat": 12}},
        "pozole": {"base_calories_per_portion": 320, "typical_macros": {"protein": 18, "carbs": 40, "fat": 10}},
        "mole": {"base_calories_per_portion": 380, "typical_macros": {"protein": 22, "carbs": 25, "fat": 20}},
        # ... (full database)
    }


    async def recognize_food(
        self,
        image_data: bytes,
        user: User,
        meal_type: str = "comida"
    ) -> Dict[str, Any]:
        """
        Recognize food from image using Gemini Vision

        Returns:
            {
              "recognized_foods": [...],
              "total_nutrition": {...},
              "equivalents": "3 cereales, 2 carne, 1 grasa",
              "suggestions": [...],
              "confidence_score": 0.92
            }
        """
        try:
            # Build user context
            user_context = {
                "dietary_restrictions": user.patient.food_restrictions if hasattr(user, 'patient') else [],
                "allergies": user.patient.allergies if hasattr(user, 'patient') else [],
                "goal": user.patient.primary_goal if hasattr(user, 'patient') else None
            }

            # Call Gemini Vision
            gemini_result = await gemini_client.analyze_image(
                image_data=image_data,
                task="food_recognition",
                context=user_context
            )

            # Enhance with local database
            enhanced_foods = []
            for food in gemini_result.get("foods", []):
                food_name = food["name"].lower()

                # Check if it's in our Mexican foods database
                if food_name in self.MEXICAN_FOODS_DB:
                    db_info = self.MEXICAN_FOODS_DB[food_name]
                    food["is_verified"] = True
                    food["database_match"] = True
                    # Use database values if Gemini's estimation is off
                    if abs(food["estimated_calories"] - db_info["base_calories_per_unit"]) > 100:
                        food["estimated_calories"] = db_info["base_calories_per_unit"]
                        food["macros"] = db_info["typical_macros"]

                enhanced_foods.append(food)

            # Calculate total nutrition
            total_nutrition = self._calculate_total_nutrition(enhanced_foods)

            # Calculate Mexican equivalents
            equivalents = self._calculate_equivalents(total_nutrition)

            # Generate suggestions based on user goal
            suggestions = self._generate_suggestions(enhanced_foods, user)

            return {
                "recognized_foods": enhanced_foods,
                "total_nutrition": total_nutrition,
                "equivalents": equivalents,
                "suggestions": suggestions,
                "confidence_score": self._calculate_confidence(enhanced_foods),
                "processing_time_ms": 0  # Add timing
            }

        except Exception as e:
            logger.error(f"Food recognition error: {e}")
            raise


    def _calculate_total_nutrition(self, foods: List[Dict]) -> Dict[str, float]:
        """Sum nutrition from all foods"""
        totals = {
            "calories": 0,
            "protein_g": 0,
            "carbs_g": 0,
            "fat_g": 0,
            "fiber_g": 0
        }

        for food in foods:
            totals["calories"] += food.get("estimated_calories", 0)
            macros = food.get("macros", {})
            totals["protein_g"] += macros.get("protein_g", 0)
            totals["carbs_g"] += macros.get("carbs_g", 0)
            totals["fat_g"] += macros.get("fat_g", 0)
            totals["fiber_g"] += macros.get("fiber_g", 0)

        return totals


    def _calculate_equivalents(self, nutrition: Dict[str, float]) -> str:
        """
        Convert nutrition to Mexican food equivalents system

        Mexican equivalents:
        - 1 Cereal = 15g carbs, 2g protein, 70 cal
        - 1 Carne bajo aporte = 7g protein, 3g fat, 55 cal
        - 1 Grasa = 5g fat, 45 cal
        - 1 Verdura = 4g carbs, 2g protein, 25 cal
        - 1 Fruta = 15g carbs, 60 cal
        """
        cereales = round(nutrition["carbs_g"] / 15)
        carne = round(nutrition["protein_g"] / 7)
        grasa = round(nutrition["fat_g"] / 5)

        parts = []
        if cereales > 0:
            parts.append(f"{cereales} {'cereal' if cereales == 1 else 'cereales'}")
        if carne > 0:
            parts.append(f"{carne} carne")
        if grasa > 0:
            parts.append(f"{grasa} {'grasa' if grasa == 1 else 'grasas'}")

        return ", ".join(parts) if parts else "0 equivalentes"


    def _generate_suggestions(self, foods: List[Dict], user: User) -> List[str]:
        """Generate personalized suggestions based on user goal"""
        suggestions = []

        total_protein = sum(f.get("macros", {}).get("protein_g", 0) for f in foods)
        total_carbs = sum(f.get("macros", {}).get("carbs_g", 0) for f in foods)
        total_fat = sum(f.get("macros", {}).get("fat_g", 0) for f in foods)

        # Check if user has goal
        if hasattr(user, 'patient') and user.patient:
            goal = user.patient.primary_goal

            if goal == "weight_loss":
                if total_carbs > 50:
                    suggestions.append("Considera reducir cereales para acelerar pérdida de peso")
                if total_protein < 20:
                    suggestions.append("Agrega más proteína para mantener masa muscular")

            elif goal == "muscle_gain":
                if total_protein < 30:
                    suggestions.append("Aumenta proteína a 30-40g por comida para ganar músculo")

            # Check for missing veggies
            has_vegetables = any("verdura" in f["name"].lower() or "vegetal" in f["name"].lower() for f in foods)
            if not has_vegetables:
                suggestions.append("Agrega verduras para fibra y micronutrientes")

        return suggestions


    def _calculate_confidence(self, foods: List[Dict]) -> float:
        """Calculate overall confidence score"""
        if not foods:
            return 0.0

        confidences = [f.get("confidence", 0.5) for f in foods]
        return sum(confidences) / len(confidences)
```

### 6.6 NOM-051 Label Scanner Service

```python
# app/services/ai/label_scanner.py

from app.services.ai.gemini_client import gemini_client
from google.cloud import vision
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class LabelScannerService:
    """
    Scan Mexican nutrition labels (NOM-051) using Gemini Vision + Cloud Vision OCR
    """

    def __init__(self):
        # Google Cloud Vision for OCR (more accurate text extraction)
        self.vision_client = vision.ImageAnnotatorClient()

        # NOM-051 warning thresholds
        self.NOM_051_THRESHOLDS = {
            "calories": {"per_100g": 275, "per_100ml": 70},
            "sugar": {"per_100g": 10, "per_100ml": 5},
            "saturated_fat": {"per_100g": 4, "per_100ml": 2},
            "trans_fat": {"any": 0.5},
            "sodium": {"per_100g": 300, "per_100ml": 300}
        }


    async def scan_label(self, image_data: bytes) -> Dict[str, Any]:
        """
        Scan nutrition label and extract structured data

        Process:
        1. Use Cloud Vision OCR for text extraction (high accuracy)
        2. Use Gemini Vision for structure parsing + understanding
        3. Apply NOM-051 validation rules
        4. Generate health score and recommendations
        """
        try:
            # Step 1: OCR with Cloud Vision
            ocr_text = await self._extract_text_with_ocr(image_data)

            # Step 2: Parse with Gemini Vision
            gemini_result = await gemini_client.analyze_image(
                image_data=image_data,
                task="label_scan",
                context={"ocr_text": ocr_text}  # Provide OCR text to Gemini for better accuracy
            )

            # Step 3: Validate and apply NOM-051 rules
            warnings = self._check_nom_051_warnings(gemini_result.get("nutrition_per_serving", {}))
            gemini_result["nom_051_warnings"] = warnings

            # Step 4: Calculate health score
            health_score = self._calculate_health_score(
                gemini_result.get("nutrition_per_serving", {}),
                warnings
            )
            gemini_result["health_score"] = health_score

            # Step 5: Generate recommendation using Gemini
            recommendation = await self._generate_recommendation(gemini_result)
            gemini_result["recommendation"] = recommendation

            # Step 6: Find better alternatives
            alternatives = await self._find_alternatives(gemini_result)
            gemini_result["better_alternatives"] = alternatives

            return gemini_result

        except Exception as e:
            logger.error(f"Label scan error: {e}")
            raise


    async def _extract_text_with_ocr(self, image_data: bytes) -> str:
        """Extract text from image using Google Cloud Vision OCR"""
        image = vision.Image(content=image_data)
        response = self.vision_client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            return texts[0].description  # Full text
        return ""


    def _check_nom_051_warnings(self, nutrition: Dict[str, float]) -> List[str]:
        """
        Check NOM-051 warning seal requirements

        Mexican law requires warning seals for:
        - EXCESO CALORÍAS
        - EXCESO AZÚCARES
        - EXCESO GRASAS SATURADAS
        - EXCESO GRASAS TRANS
        - EXCESO SODIO
        """
        warnings = []

        # Assume per 100g for solid foods (adjust if per_100ml)
        thresholds = self.NOM_051_THRESHOLDS

        if nutrition.get("calories", 0) >= thresholds["calories"]["per_100g"]:
            warnings.append("EXCESO CALORÍAS")

        if nutrition.get("sugar_g", 0) >= thresholds["sugar"]["per_100g"]:
            warnings.append("EXCESO AZÚCARES")

        if nutrition.get("saturated_fat_g", 0) >= thresholds["saturated_fat"]["per_100g"]:
            warnings.append("EXCESO GRASAS SATURADAS")

        if nutrition.get("trans_fat_g", 0) >= thresholds["trans_fat"]["any"]:
            warnings.append("EXCESO GRASAS TRANS")

        if nutrition.get("sodium_mg", 0) >= thresholds["sodium"]["per_100g"]:
            warnings.append("EXCESO SODIO")

        return warnings


    def _calculate_health_score(self, nutrition: Dict[str, float], warnings: List[str]) -> float:
        """
        Calculate health score from 0-10

        Scoring:
        - Start with 10
        - Deduct 2 points per NOM-051 warning
        - Add points for fiber, protein
        - Consider ingredient quality
        """
        score = 10.0

        # Penalties
        score -= len(warnings) * 2

        # Bonuses
        if nutrition.get("fiber_g", 0) >= 3:
            score += 1
        if nutrition.get("protein_g", 0) >= 5:
            score += 1

        # Clamp to 0-10
        return max(0, min(10, score))


    async def _generate_recommendation(self, label_data: Dict[str, Any]) -> str:
        """Generate personalized recommendation using Gemini"""
        prompt = f"""
        Basándote en esta información nutricional:

        Producto: {label_data.get('product_name')}
        Calorías: {label_data.get('nutrition_per_serving', {}).get('calories')} kcal
        Azúcar: {label_data.get('nutrition_per_serving', {}).get('sugar_g')} g
        Sodio: {label_data.get('nutrition_per_serving', {}).get('sodium_mg')} mg
        Advertencias NOM-051: {', '.join(label_data.get('nom_051_warnings', []))}

        Genera una recomendación breve (2-3 oraciones) en español para un mexicano promedio.
        Sé directo, amigable y práctico.
        """

        return await gemini_client.generate_text(prompt, model="flash")


    async def _find_alternatives(self, label_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find healthier alternatives using database + Gemini"""
        # TODO: Implement product database search
        # For now, use Gemini to suggest generic alternatives

        prompt = f"""
        El producto "{label_data.get('product_name')}" tiene estos problemas:
        {', '.join(label_data.get('nom_051_warnings', []))}

        Sugiere 2-3 alternativas más saludables (productos reales en México).
        Formato JSON:
        [{{"product_name": "...", "why_better": "...", "estimated_health_score": 8.5}}]
        """

        response = await gemini_client.generate_text(prompt, model="flash")

        # Parse JSON
        import json
        try:
            return json.loads(response)
        except:
            return []
```

### 6.7 Meal Plan Generator Service

```python
# app/services/ai/meal_plan_generator.py

from app.services.ai.gemini_client import gemini_client
from app.models.patient import Patient
from app.repositories.recipe_repo import RecipeRepository
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class MealPlanGeneratorService:
    """
    AI-powered personalized meal plan generator
    """

    def __init__(self):
        self.recipe_repo = RecipeRepository()


    async def generate_meal_plan(
        self,
        patient: Patient,
        duration_days: int = 7,
        calories_target: int = None,
        dietary_preferences: List[str] = None,
        exclude_foods: List[str] = None,
        budget_level: str = "moderado"
    ) -> Dict[str, Any]:
        """
        Generate personalized meal plan using Gemini + recipe database

        Process:
        1. Calculate nutritional requirements
        2. Get available recipes from database
        3. Use Gemini to create optimal combinations
        4. Generate shopping list
        5. Estimate cost
        """
        try:
            # Step 1: Calculate requirements
            requirements = self._calculate_requirements(patient, calories_target)

            # Step 2: Get recipes matching criteria
            available_recipes = await self.recipe_repo.search_recipes(
                dietary_tags=dietary_preferences,
                exclude_ingredients=exclude_foods,
                is_published=True
            )

            # Step 3: Build context for Gemini
            context = {
                "patient_info": {
                    "age": patient.age,
                    "gender": patient.gender,
                    "goal": patient.primary_goal,
                    "activity_level": patient.activity_level,
                    "health_conditions": patient.health_conditions,
                    "allergies": patient.allergies,
                    "restrictions": patient.food_restrictions
                },
                "requirements": requirements,
                "available_recipes": [
                    {
                        "id": r.id,
                        "title": r.title,
                        "meal_type": r.meal_type,
                        "calories": r.nutrition_per_serving.get("calories"),
                        "macros": r.nutrition_per_serving
                    }
                    for r in available_recipes[:50]  # Limit to 50 best matches
                ],
                "budget_level": budget_level,
                "duration_days": duration_days
            }

            # Step 4: Ask Gemini to create meal plan
            prompt = f"""
            Crea un plan de comidas de {duration_days} días para un paciente mexicano con:

            **Objetivo:** {patient.primary_goal}
            **Calorías diarias:** {requirements['calories']} kcal
            **Macros objetivo:** {requirements['macros']['protein']}g proteína, {requirements['macros']['carbs']}g carbohidratos, {requirements['macros']['fat']}g grasas
            **Restricciones:** {', '.join(patient.food_restrictions) if patient.food_restrictions else 'Ninguna'}
            **Alergias:** {', '.join(patient.allergies) if patient.allergies else 'Ninguna'}
            **Presupuesto:** {budget_level}

            **Recetas disponibles:**
            {self._format_recipes_for_prompt(available_recipes[:30])}

            Genera un plan variado, balanceado y culturalmente apropiado para México.
            Incluye 5 comidas al día: desayuno, colación AM, comida, colación PM, cena.

            Devuelve JSON con esta estructura:
            {{
              "days": [
                {{
                  "day": 1,
                  "meals": [
                    {{
                      "meal_type": "desayuno",
                      "recipe_id": "uuid",
                      "recipe_name": "...",
                      "portions": 1.0,
                      "time": "08:00"
                    }}
                  ],
                  "daily_totals": {{
                    "calories": 1800,
                    "protein_g": 90,
                    "carbs_g": 200,
                    "fat_g": 60
                  }}
                }}
              ],
              "shopping_list": [
                {{"item": "Tortillas de maíz", "quantity": "2 paquetes", "estimated_cost_mxn": 40}}
              ],
              "preparation_tips": ["...", "..."],
              "estimated_total_cost_mxn": 850
            }}
            """

            response_text = await gemini_client.generate_text(
                prompt,
                model="pro",
                system_instruction="Eres un nutriólogo mexicano experto en crear planes de alimentación personalizados y culturalmente apropiados."
            )

            # Parse JSON response
            import json
            meal_plan = json.loads(self._extract_json(response_text))

            # Add metadata
            meal_plan["patient_id"] = patient.id
            meal_plan["created_at"] = "2025-01-15T10:30:00Z"  # Use actual timestamp
            meal_plan["requirements"] = requirements

            return meal_plan

        except Exception as e:
            logger.error(f"Meal plan generation error: {e}")
            raise


    def _calculate_requirements(self, patient: Patient, calories_override: int = None) -> Dict[str, Any]:
        """Calculate nutritional requirements using Harris-Benedict + activity factor"""
        # Simplified calculation (use actual formulas in production)
        if calories_override:
            calories = calories_override
        else:
            # Estimate based on goal
            base_calories = 2000 if patient.gender == "male" else 1600

            if patient.primary_goal == "weight_loss":
                calories = base_calories - 500
            elif patient.primary_goal == "muscle_gain":
                calories = base_calories + 300
            else:
                calories = base_calories

        # Macro distribution
        if patient.primary_goal == "muscle_gain":
            protein_ratio = 0.30
            carbs_ratio = 0.45
            fat_ratio = 0.25
        else:
            protein_ratio = 0.25
            carbs_ratio = 0.45
            fat_ratio = 0.30

        return {
            "calories": calories,
            "macros": {
                "protein": round((calories * protein_ratio) / 4),  # 4 cal/g
                "carbs": round((calories * carbs_ratio) / 4),
                "fat": round((calories * fat_ratio) / 9)  # 9 cal/g
            }
        }


    def _format_recipes_for_prompt(self, recipes: List) -> str:
        """Format recipes for Gemini prompt"""
        formatted = []
        for r in recipes:
            formatted.append(
                f"- {r.title} (ID: {r.id}, {r.meal_type}, {r.nutrition_per_serving.get('calories')} kcal)"
            )
        return "\n".join(formatted)


    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown code blocks"""
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text
```

### 6.8 Chatbot Service

```python
# app/services/ai/chatbot_service.py

from app.services.ai.gemini_client import gemini_client
from app.models.user import User
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ChatbotService:
    """
    AI nutritionist chatbot using Gemini Pro
    """

    SYSTEM_INSTRUCTION = """
    Eres un asistente virtual de nutrición experto, trabajando para Nutrition Intelligence en México.

    Tu rol:
    - Responder preguntas sobre nutrición de manera clara y amigable
    - Usar lenguaje apropiado para mexicanos
    - Basar tus respuestas en evidencia científica
    - Mencionar la cultura alimentaria mexicana cuando sea relevante
    - Ser empático y motivador
    - NUNCA dar diagnósticos médicos - siempre recomendar consultar con un profesional
    - Promover la comida tradicional mexicana saludable

    Temas que puedes abordar:
    - Información nutricional de alimentos
    - Consejos para objetivos (pérdida de peso, ganancia muscular, salud)
    - Explicación de macronutrientes y micronutrientes
    - Interpretación de etiquetas nutricionales
    - Recetas saludables mexicanas
    - Sistema de equivalentes

    Temas que DEBES evitar:
    - Diagnósticos médicos
    - Prescripción de suplementos sin supervisión
    - Consejos para condiciones médicas graves sin profesional
    - Dietas extremas o peligrosas
    """

    async def chat(
        self,
        user: User,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and return AI response

        Args:
            user: Current user
            message: User's message
            conversation_history: Previous messages in format [{"role": "user"|"model", "content": "..."}]

        Returns:
            {
              "response": "...",
              "sources": [...],
              "related_questions": [...],
              "conversation_id": "uuid"
            }
        """
        try:
            # Build user context
            user_context = ""
            if hasattr(user, 'patient') and user.patient:
                user_context = f"""
                Contexto del usuario:
                - Objetivo: {user.patient.primary_goal}
                - Condiciones de salud: {', '.join(user.patient.health_conditions) if user.patient.health_conditions else 'Ninguna'}
                - Alergias: {', '.join(user.patient.allergies) if user.patient.allergies else 'Ninguna'}
                - Restricciones: {', '.join(user.patient.food_restrictions) if user.patient.food_restrictions else 'Ninguna'}

                Usa esta información para personalizar tu respuesta.
                """

            # Prepare messages
            messages = conversation_history or []
            messages.append({
                "role": "user",
                "content": f"{user_context}\n\n{message}" if user_context else message
            })

            # Get Gemini response
            response_text = await gemini_client.chat(
                messages=messages,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            # Generate related questions
            related_questions = await self._generate_related_questions(message, response_text)

            return {
                "response": response_text,
                "sources": self._extract_sources(response_text),
                "related_questions": related_questions,
                "conversation_id": "uuid"  # Generate proper UUID
            }

        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return {
                "response": "Lo siento, tuve un problema procesando tu pregunta. ¿Podrías intentar reformularla?",
                "sources": [],
                "related_questions": [],
                "conversation_id": None
            }


    async def _generate_related_questions(self, original_question: str, answer: str) -> List[str]:
        """Generate 3 related follow-up questions"""
        prompt = f"""
        Pregunta original: {original_question}
        Respuesta dada: {answer}

        Genera 3 preguntas relacionadas que el usuario podría querer hacer a continuación.
        Devuelve solo las preguntas, una por línea, sin numeración.
        """

        response = await gemini_client.generate_text(prompt, model="flash")
        questions = [q.strip() for q in response.split('\n') if q.strip()]
        return questions[:3]


    def _extract_sources(self, response: str) -> List[str]:
        """Extract cited sources from response"""
        # Simple implementation - look for common source patterns
        sources = []
        if "NOM-043" in response or "NOM-051" in response:
            sources.append("Normas Oficiales Mexicanas (NOM)")
        if "OMS" in response or "WHO" in response:
            sources.append("Organización Mundial de la Salud")
        return sources


# Singleton
chatbot_service = ChatbotService()
```

### 6.9 Google Workspace Integration

```python
# app/services/google_workspace.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class GoogleWorkspaceService:
    """
    Integration with Google Workspace for enhanced features
    """

    def __init__(self):
        # Service account credentials
        self.credentials = service_account.Credentials.from_service_account_file(
            'google-workspace-credentials.json',
            scopes=[
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/gmail.send'
            ]
        )

        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.calendar_service = build('calendar', 'v3', credentials=self.credentials)
        self.gmail_service = build('gmail', 'v1', credentials=self.credentials)


    async def create_shared_meal_plan_doc(
        self,
        patient_name: str,
        meal_plan: Dict[str, Any],
        nutritionist_email: str
    ) -> str:
        """
        Create a Google Doc with meal plan and share with nutritionist & patient

        Returns: Document URL
        """
        # Create document
        doc = self.drive_service.files().create(
            body={
                'name': f'Plan de Alimentación - {patient_name}',
                'mimeType': 'application/vnd.google-apps.document'
            }
        ).execute()

        doc_id = doc['id']

        # TODO: Populate document with meal plan content using Docs API

        # Share with nutritionist
        self.drive_service.permissions().create(
            fileId=doc_id,
            body={
                'type': 'user',
                'role': 'writer',
                'emailAddress': nutritionist_email
            }
        ).execute()

        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

        logger.info(f"Created shared meal plan doc: {doc_url}")

        return doc_url


    async def schedule_appointment(
        self,
        patient_email: str,
        nutritionist_email: str,
        start_time: str,
        duration_minutes: int = 60,
        title: str = "Consulta Nutricional"
    ) -> str:
        """
        Create Google Calendar event for appointment

        Returns: Event ID
        """
        event = {
            'summary': title,
            'description': 'Consulta nutricional agendada a través de Nutrition Intelligence',
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Mexico_City',
            },
            'end': {
                'dateTime': start_time,  # Add duration
                'timeZone': 'America/Mexico_City',
            },
            'attendees': [
                {'email': patient_email},
                {'email': nutritionist_email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 60},  # 1 hour before
                ],
            },
        }

        event = self.calendar_service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'
        ).execute()

        logger.info(f"Created calendar event: {event.get('id')}")

        return event.get('id')
```

---

## 7. Security & Privacy

### 7.1 Authentication & Authorization

#### 7.1.1 JWT Token Strategy

```python
# app/core/security.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional, Dict, Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create JWT refresh token (longer expiration)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)
```

#### 7.1.2 Role-Based Access Control (RBAC)

```python
# app/core/permissions.py

from enum import Enum
from typing import List

class Permission(str, Enum):
    # User management
    CREATE_USERS = "create_users"
    VIEW_USERS = "view_users"
    EDIT_USERS = "edit_users"
    DELETE_USERS = "delete_users"

    # Patient management
    CREATE_PATIENTS = "create_patients"
    VIEW_PATIENTS = "view_patients"
    EDIT_PATIENTS = "edit_patients"
    ASSIGN_PATIENTS = "assign_patients"

    # Clinical records
    VIEW_CLINICAL_RECORD = "view_clinical_record"
    EDIT_CLINICAL_RECORD = "edit_clinical_record"

    # Meal plans
    CREATE_MEAL_PLANS = "create_meal_plans"
    ASSIGN_MEAL_PLANS = "assign_meal_plans"

    # Social features
    CREATE_POSTS = "create_posts"
    MODERATE_POSTS = "moderate_posts"

    # Admin features
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_SYSTEM = "manage_system"


ROLE_PERMISSIONS = {
    "admin": [
        Permission.CREATE_USERS,
        Permission.VIEW_USERS,
        Permission.EDIT_USERS,
        Permission.DELETE_USERS,
        Permission.VIEW_ANALYTICS,
        Permission.MANAGE_SYSTEM,
        Permission.MODERATE_POSTS,
    ],
    "nutritionist": [
        Permission.CREATE_PATIENTS,
        Permission.VIEW_PATIENTS,
        Permission.EDIT_PATIENTS,
        Permission.ASSIGN_PATIENTS,
        Permission.VIEW_CLINICAL_RECORD,
        Permission.EDIT_CLINICAL_RECORD,
        Permission.CREATE_MEAL_PLANS,
        Permission.ASSIGN_MEAL_PLANS,
        Permission.CREATE_POSTS,
    ],
    "patient": [
        Permission.CREATE_POSTS,
        Permission.VIEW_CLINICAL_RECORD,  # Own record only
    ]
}


def has_permission(user_roles: List[str], required_permission: Permission) -> bool:
    """Check if user has required permission"""
    for role in user_roles:
        if required_permission in ROLE_PERMISSIONS.get(role, []):
            return True
    return False
```

### 7.2 Data Encryption

#### 7.2.1 Encryption at Rest

```sql
-- PostgreSQL encryption for sensitive fields

-- Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Example: Encrypt patient health data
CREATE TABLE clinical.encrypted_records (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL,

    -- Encrypted fields
    medical_history_encrypted BYTEA,
    medications_encrypted BYTEA,
    lab_results_encrypted BYTEA,

    -- Encryption metadata
    encryption_key_version INTEGER DEFAULT 1,
    encrypted_at TIMESTAMP DEFAULT NOW()
);

-- Insert with encryption
INSERT INTO clinical.encrypted_records (patient_id, medical_history_encrypted)
VALUES (
    'uuid',
    pgp_sym_encrypt('Sensitive medical history...', 'encryption_key_from_env')
);

-- Query with decryption
SELECT
    id,
    patient_id,
    pgp_sym_decrypt(medical_history_encrypted, 'encryption_key_from_env') as medical_history
FROM clinical.encrypted_records
WHERE patient_id = 'uuid';
```

#### 7.2.2 Encryption in Transit

```nginx
# nginx SSL configuration

server {
    listen 443 ssl http2;
    server_name api.nutritionintelligence.mx;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/nutritionintelligence.mx/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/nutritionintelligence.mx/privkey.pem;

    # Strong SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;

    # HSTS (force HTTPS)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name api.nutritionintelligence.mx;
    return 301 https://$server_name$request_uri;
}
```

### 7.3 Data Privacy & Compliance

#### 7.3.1 Mexican Data Protection Law (LFPDPPP)

**Compliance Requirements:**
- Obtain explicit consent for personal data collection
- Provide privacy notice (Aviso de Privacidad)
- Allow users to access, rectify, cancel, and oppose data usage (ARCO rights)
- Implement security measures for sensitive data
- Report data breaches within 72 hours

**Implementation:**

```python
# app/models/user_consent.py

class UserConsent(Base):
    """Track user consent for data processing"""
    __tablename__ = "user_consents"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))

    # Consent types
    data_processing = Column(Boolean, default=False)
    marketing_communications = Column(Boolean, default=False)
    data_sharing_partners = Column(Boolean, default=False)

    # Privacy notice
    privacy_notice_version = Column(String(10))
    privacy_notice_accepted_at = Column(DateTime)

    # IP address for legal records
    ip_address = Column(String(45))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

#### 7.3.2 GDPR Compliance (for European users)

```python
# app/api/v1/privacy.py

@router.post("/privacy/export-data")
async def export_user_data(current_user: User = Depends(get_current_user)):
    """
    GDPR Article 20: Right to data portability
    Export all user data in machine-readable format (JSON)
    """
    user_data = {
        "profile": current_user.to_dict(),
        "posts": [p.to_dict() for p in current_user.posts],
        "comments": [c.to_dict() for c in current_user.comments],
        "measurements": [m.to_dict() for m in current_user.measurements],
        "meal_logs": [l.to_dict() for l in current_user.meal_logs],
        "clinical_records": [r.to_dict() for r in current_user.clinical_records],
    }

    return JSONResponse(content=user_data)


@router.delete("/privacy/delete-account")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    confirmation: str = Body(...)
):
    """
    GDPR Article 17: Right to erasure (right to be forgotten)
    Permanently delete user account and associated data
    """
    if confirmation != "DELETE_MY_ACCOUNT":
        raise HTTPException(400, "Confirmation required")

    # Soft delete (mark as deleted, anonymize data)
    current_user.deleted_at = datetime.utcnow()
    current_user.email = f"deleted_{current_user.id}@deleted.local"
    current_user.first_name = "Deleted"
    current_user.last_name = "User"

    db.commit()

    return {"message": "Account deleted successfully"}
```

### 7.4 Security Best Practices

#### 7.4.1 Input Validation

```python
# app/schemas/user.py

from pydantic import BaseModel, EmailStr, constr, validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    first_name: constr(min_length=1, max_length=100)
    last_name: constr(min_length=1, max_length=100)
    phone: Optional[constr(regex=r'^\+52\d{10}$')]  # Mexican phone format

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain special character')
        return v
```

#### 7.4.2 Rate Limiting

```python
# app/middleware/rate_limit.py

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply to FastAPI app
app.state.limiter = limiter

# Rate limit decorators
@app.post("/api/v1/auth/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request, credentials: LoginCredentials):
    pass


@app.post("/api/v1/posts")
@limiter.limit("20/hour")  # Max 20 posts per hour
async def create_post(request: Request, post: PostCreate):
    pass
```

#### 7.4.3 SQL Injection Prevention

```python
# Always use parameterized queries with SQLAlchemy

# ❌ VULNERABLE (Never do this)
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ SAFE (Always do this)
query = select(User).where(User.email == email)
```

#### 7.4.4 XSS Prevention

```python
# Sanitize user input before storing/displaying

from bleach import clean

ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

def sanitize_html(content: str) -> str:
    """Remove dangerous HTML tags and attributes"""
    return clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
```

---

## 8. Scalability & Performance

### 8.1 Caching Strategy

#### 8.1.1 Redis Cache Layers

```python
# app/services/cache.py

import redis
import json
from typing import Any, Optional
from functools import wraps

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


def cache(ttl: int = 300):
    """
    Decorator for caching function results

    Args:
        ttl: Time to live in seconds (default 5 minutes)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator


# Usage example
@cache(ttl=3600)  # Cache for 1 hour
async def get_trending_posts():
    """Get trending posts (expensive query)"""
    return db.query(Post).filter(Post.is_trending == True).all()
```

#### 8.1.2 Cache Invalidation

```python
# Invalidate cache when data changes

async def create_post(post_data: PostCreate, user: User):
    """Create new post and invalidate feed cache"""
    # Create post
    post = Post(**post_data.dict(), author_id=user.id)
    db.add(post)
    db.commit()

    # Invalidate relevant caches
    redis_client.delete(f"user_feed:{user.id}")
    redis_client.delete(f"trending_posts")

    # Invalidate followers' feeds
    followers = get_followers(user.id)
    for follower in followers:
        redis_client.delete(f"user_feed:{follower.id}")

    return post
```

### 8.2 Database Optimization

#### 8.2.1 Query Optimization

```python
# Use eager loading to avoid N+1 queries

# ❌ BAD (N+1 query problem)
posts = db.query(Post).all()
for post in posts:
    print(post.author.name)  # Each iteration hits database


# ✅ GOOD (Single query with join)
from sqlalchemy.orm import joinedload

posts = db.query(Post).options(
    joinedload(Post.author),
    joinedload(Post.comments)
).all()
```

#### 8.2.2 Database Indexes

```sql
-- Create indexes for frequently queried columns

-- Posts feed queries
CREATE INDEX idx_posts_created_at_trending ON social.posts(created_at DESC, is_trending)
WHERE deleted_at IS NULL;

-- User lookups
CREATE INDEX idx_users_email_active ON auth.users(email)
WHERE deleted_at IS NULL AND is_active = TRUE;

-- Challenge leaderboards
CREATE INDEX idx_challenge_participants_rank ON social.challenge_participants(challenge_id, rank);

-- Partial index for active connections
CREATE INDEX idx_instagram_active ON integrations.instagram_connections(user_id)
WHERE is_active = TRUE;
```

#### 8.2.3 Database Partitioning

```sql
-- Partition posts table by created_at for better performance

CREATE TABLE social.posts_partitioned (
    id UUID,
    created_at TIMESTAMP NOT NULL,
    -- ... other columns
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE social.posts_2025_01 PARTITION OF social.posts_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE social.posts_2025_02 PARTITION OF social.posts_partitioned
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

### 8.3 Load Balancing

```yaml
# kubernetes/api-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 5  # Run 5 instances
  selector:
    matchLabels:
      app: nutrition-api
  template:
    metadata:
      labels:
        app: nutrition-api
    spec:
      containers:
      - name: api
        image: nutritionintelligence/api:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: LoadBalancer
  selector:
    app: nutrition-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### 8.4 CDN for Static Assets

```python
# app/core/config.py

class Settings(BaseSettings):
    # CDN Configuration
    CDN_URL: str = "https://cdn.nutritionintelligence.mx"
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str


# app/services/storage.py

import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_image(file: UploadFile, folder: str = "posts") -> str:
    """
    Upload image to Cloudinary CDN
    Returns: CDN URL
    """
    result = cloudinary.uploader.upload(
        file.file,
        folder=folder,
        transformation=[
            {'width': 1200, 'height': 1200, 'crop': 'limit'},
            {'quality': 'auto:good'},
            {'fetch_format': 'auto'}  # Automatic format (WebP for supported browsers)
        ]
    )

    return result['secure_url']
```

---

## 9. DevOps & Infrastructure

### 9.1 Infrastructure Overview (Google Cloud Platform)

```
┌─────────────────────────────────────────────────────────────┐
│                     GOOGLE CLOUD PLATFORM                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Cloud Load Balancing (HTTPS)               │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                     │
│       ┌───────────────┼───────────────┐                    │
│       │               │               │                    │
│       ▼               ▼               ▼                    │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐               │
│  │  GKE    │    │  GKE    │    │  GKE    │               │
│  │ Cluster │    │ Cluster │    │ Cluster │               │
│  │ (us-c1) │    │ (us-e1) │    │ (eu-w1) │               │
│  └─────────┘    └─────────┘    └─────────┘               │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           Cloud SQL (PostgreSQL 15)                  │ │
│  │           Master + Read Replicas                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           Cloud Memorystore (Redis)                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           Cloud Storage (Object Storage)             │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           Cloud CDN (Cloudflare)                     │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=app tests/

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: gcr.io
          username: _json_key
          password: ${{ secrets.GCP_SA_KEY }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: gcr.io/nutrition-intelligence/api:${{ github.sha }},gcr.io/nutrition-intelligence/api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1

      - name: Get GKE credentials
        run: |
          gcloud container clusters get-credentials nutrition-cluster \
            --zone us-central1-a \
            --project nutrition-intelligence

      - name: Deploy to GKE
        run: |
          kubectl set image deployment/api-deployment \
            api=gcr.io/nutrition-intelligence/api:${{ github.sha }}

          kubectl rollout status deployment/api-deployment

      - name: Run database migrations
        run: |
          kubectl exec -it $(kubectl get pod -l app=api -o jsonpath="{.items[0].metadata.name}") \
            -- alembic upgrade head
```

### 9.3 Docker Configuration

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml (for local development)

version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/nutrition_db
      - REDIS_URL=redis://redis:6379/0
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --reload --host 0.0.0.0

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=nutrition_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery_worker:
    build: .
    command: celery -A app.tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
      - postgres
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/nutrition_db
      - REDIS_URL=redis://redis:6379/0

volumes:
  postgres_data:
```

---

## 10. Monitoring & Observability

### 10.1 Prometheus Metrics

```python
# app/middleware/metrics.py

from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

active_users = Gauge(
    'active_users_total',
    'Number of active users'
)

gemini_api_calls = Counter(
    'gemini_api_calls_total',
    'Total Gemini API calls',
    ['model', 'status']
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response


# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### 10.2 Logging Strategy

```python
# app/core/logging.py

import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easy parsing"""

    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

# Set JSON formatter
for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

### 10.3 Error Tracking (Sentry)

```python
# app/main.py

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastAPIIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.1,
    integrations=[
        FastAPIIntegration(),
        SqlalchemyIntegration(),
    ],
)


# Custom error tracking
def track_error(error: Exception, context: dict = None):
    """Track error with additional context"""
    with sentry_sdk.push_scope() as scope:
        if context:
            for key, value in context.items():
                scope.set_extra(key, value)

        sentry_sdk.capture_exception(error)
```

### 10.4 Grafana Dashboards

```yaml
# grafana/dashboards/api-dashboard.json

{
  "dashboard": {
    "title": "Nutrition Intelligence - API Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{endpoint}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx errors"
          }
        ]
      },
      {
        "title": "Active Users",
        "targets": [
          {
            "expr": "active_users_total"
          }
        ]
      },
      {
        "title": "Database Connections",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends"
          }
        ]
      },
      {
        "title": "Gemini API Calls",
        "targets": [
          {
            "expr": "rate(gemini_api_calls_total[5m])",
            "legendFormat": "{{model}}"
          }
        ]
      }
    ]
  }
}
```

### 10.5 Alerting Rules

```yaml
# prometheus/alerts.yml

groups:
  - name: api_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      # High response time
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "P95 response time is {{ $value }}s"

      # Database connection issues
      - alert: DatabaseConnectionHigh
        expr: pg_stat_database_numbackends > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High number of database connections"
          description: "{{ $value }} active connections"

      # Low active users (potential outage)
      - alert: LowActiveUsers
        expr: active_users_total < 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Unusually low active users"
          description: "Only {{ $value }} active users"
```

---

## 11. Conclusion

This Technical Design Document provides a comprehensive blueprint for building **Nutrition Intelligence**, a world-class nutrition platform optimized for the Mexican market.

### Key Highlights:

✅ **Modern Tech Stack**: FastAPI, React Native, PostgreSQL, Google Gemini AI
✅ **Mexican-First**: NOM-051 compliance, local food database, cultural adaptation
✅ **Social Impact**: 100% free, backed by Consejo Nacional de Nutriólogos
✅ **Scalable Architecture**: Microservices-ready, cloud-native on Google Cloud Platform
✅ **AI-Powered**: Food recognition, label scanning, meal plan generation with Gemini
✅ **Viral Features**: Social media integration, family circles, challenges
✅ **Enterprise-Grade**: Security, monitoring, CI/CD, compliance

### Next Steps:

1. **Phase 1** (Weeks 1-4): Core infrastructure, authentication, basic CRUD
2. **Phase 2** (Weeks 5-8): Social features, AI integration, mobile apps
3. **Phase 3** (Weeks 9-12): Clinical records, meal planning, gamification
4. **Phase 4** (Weeks 13-16): Social media integration, advanced features
5. **Phase 5** (Weeks 17-20): Testing, optimization, launch preparation

**Estimated Timeline**: 20 weeks to MVP
**Team Size**: 2 backend + 2 frontend + 1 DevOps + 1 QA

---

**Document Status**: ✅ **COMPLETE**
**Version**: 1.0.0
**Last Updated**: January 2025
**Next Review**: February 2025

---