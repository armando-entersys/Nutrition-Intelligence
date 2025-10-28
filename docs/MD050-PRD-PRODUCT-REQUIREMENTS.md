# MD050 - Product Requirements Document (PRD)
## Nutrition Intelligence - Red Social Familiar Mexicana de Salud

**Document Version:** 1.0.0
**Last Updated:** January 2025
**Owner:** Product Team
**Status:** Draft → Review → Approved
**Classification:** Internal - Confidential

---

## Executive Summary

### 🎯 Vision Statement
Create Mexico's first health-focused social network that leverages the country's strong family values (familismo) to combat obesity and diabetes while preserving cultural food identity.

### 📊 Market Opportunity
- **TAM (Total Addressable Market):** 130M Mexicans
- **SAM (Serviceable Available Market):** 45M smartphone users interested in health
- **SOM (Serviceable Obtainable Market - Year 1):** 100K active users
- **Problem Size:** 75% of Mexican adults are overweight/obese, 12% have diabetes
- **Market Gap:** No existing platform combines professional nutrition + social community + cultural preservation

### 💡 Key Differentiators
1. **Family-Centric Design** - Reflects Mexican "familismo" values
2. **Professional Backing** - Endorsed by Consejo Nacional de Nutriólogos
3. **Cultural Intelligence** - AI trained on Mexican cuisine & traditions
4. **100% Free** - Social impact mission vs. profit maximization
5. **Dual Community** - Separate but connected spaces for patients & nutritionists

---

## 1. Product Overview

### 1.1 What We're Building

**Nutrition Intelligence** is a comprehensive health platform that combines:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│    PROFESSIONAL NUTRITION PRACTICE MANAGEMENT        │
│    (Expediente Clínico Digital + IA)                 │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│    SOCIAL NETWORK "LA FAMILIA SALUDABLE" 🇲🇽         │
│    (Community + Gamification + Viral Features)       │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│    AI-POWERED TOOLS                                  │
│    (Food Recognition + Label Scanner + Predictions)  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 1.2 Core Pillars

#### Pillar 1: Professional Tools (for Nutritionists)
- Complete digital clinical records (NOM-004-SSA3-2012 compliant)
- AI-powered diet generation
- Patient management dashboard
- Appointment scheduling
- Payment tracking
- WhatsApp Business integration

#### Pillar 2: Social Network "La Familia Saludable"
- **Patient Community:** Support groups, challenges, recipe sharing
- **Nutritionist Community:** Professional networking, case studies, CE credits
- **Cross-Community:** Verified content, Q&A, success stories
- **Family Circles:** Private groups for patients + nutritionist + family members

#### Pillar 3: Gamification & Engagement
- Mexican-themed leveling system
- Cultural badges & achievements
- National challenges (state vs. state)
- Streaks & daily rewards
- Community leaderboards

#### Pillar 4: AI & Automation
- Photo food recognition (Mexican cuisine optimized)
- NOM-051 label scanner
- Predictive health analytics
- Auto-generated diet plans
- Chatbot nutritionist assistant
- Early abandonment detection

---

## 2. User Personas

### Persona 1: "Laura" - The Professional Nutritionist

**Demographics:**
- Age: 28-45
- Location: Urban Mexico (CDMX, Guadalajara, Monterrey)
- Education: Licensed nutritionist (Cédula profesional)
- Income: $15K-40K MXN/month
- Tech Savviness: Medium-High

**Goals:**
- Manage 20-50 patients efficiently
- Provide better follow-up than competitors
- Build professional reputation
- Earn stable income
- Stay updated on nutrition science
- Network with peers

**Pain Points:**
- Using multiple disconnected tools (Excel, WhatsApp, paper)
- Patients dropping out after 2-3 sessions
- Spending 30% of time on administrative tasks
- Difficulty tracking patient compliance
- No centralized patient communication
- Manual diet plan creation takes hours

**How Our Product Helps:**
- All-in-one platform replaces 5+ tools
- AI reduces diet creation time from 2h → 20min
- Gamification increases patient retention by 40%
- Real-time patient tracking via app
- Integrated WhatsApp for seamless communication
- Community increases visibility & referrals

**Success Metrics:**
- Time saved per patient: 45 minutes/week
- Patient retention rate: 70% at 6 months (vs. 30% industry avg)
- New patient acquisition: 3-5/month via platform
- Administrative time: -30%

---

### Persona 2: "Carlos" - The Motivated Patient

**Demographics:**
- Age: 30-50
- Location: Urban/suburban Mexico
- Occupation: Office worker
- Income: $8K-25K MXN/month
- Health: Overweight (BMI 28-32), pre-diabetic

**Goals:**
- Lose 10-15kg in 6 months
- Prevent type 2 diabetes
- Learn to eat healthier without giving up Mexican food
- Find support & motivation
- Track progress easily
- Not feel alone in the journey

**Pain Points:**
- Feels isolated in health journey
- Bored with generic diet apps
- Misses traditional Mexican food
- Loses motivation after 2 weeks
- Doesn't understand nutrition labels
- Forgets to log meals
- Expensive nutritionist consultations

**How Our Product Helps:**
- Community of people with same goals
- Mexican recipe database (tacos saludables, mole ligero)
- Gamification makes tracking fun
- Free access to nutritionist guidance
- NOM-051 scanner educates on products
- Daily reminders & streaks keep engaged
- Family can join support circle

**Success Metrics:**
- Weight loss: 0.5-1kg/week
- App opens: 5+ times/day
- Streak: 30+ days
- Community engagement: 10+ interactions/week
- Nutritional knowledge: +60% (quizzes)

---

### Persona 3: "María" - The Community Champion

**Demographics:**
- Age: 35-55
- Location: Semi-urban Mexico
- Occupation: Homemaker / Part-time worker
- Family: 3-4 members
- Role: Primary food preparer

**Goals:**
- Cook healthier for entire family
- Lose weight gained after pregnancies
- Find affordable healthy recipes
- Share her own recipes
- Help others in community
- Feel proud of achievements

**Pain Points:**
- Family resists "diet food"
- Budget constraints ($1500 MXN/week for groceries)
- Doesn't know how to modify traditional recipes
- Feels guilty eating differently than family
- Limited time for meal prep
- Information overload online

**How Our Product Helps:**
- Affordable Mexican recipes with cost breakdown
- Family meal planning (everyone eats same, portions adjusted)
- Recipe modification AI (make mole healthier)
- Community recipe swaps
- Recognition for helping others (badges)
- Voice-to-text logging (while cooking)

**Success Metrics:**
- Recipes shared: 5+/month
- Community karma points: Top 20%
- Family participation: 2+ members using app
- Grocery budget: No increase
- Cooking confidence: +80%

---

### Persona 4: "Dr. Roberto" - The Established Nutritionist

**Demographics:**
- Age: 45-65
- Location: Major city clinic
- Experience: 15+ years
- Patients: 100+ active
- Tech Savviness: Low-Medium

**Goals:**
- Maintain existing patient base
- Delegate routine tasks to assistants
- Establish thought leadership
- Prepare for retirement (passive income)
- Mentor young nutritionists
- Contribute to public health

**Pain Points:**
- Overwhelmed with patient volume
- Using outdated software (Nutrimind desktop)
- No mobile access to patient data
- Difficulty scaling practice
- Young nutritionists taking patients with "modern apps"
- Wants to make bigger impact beyond 1-on-1

**How Our Product Helps:**
- Cloud-based (access anywhere)
- AI handles routine diet adjustments
- Mentorship program with junior nutritionists
- Content creation tools (articles → community)
- Verification badge increases credibility
- Analytics dashboard shows practice health
- Can hire assistant nutritionists on platform

**Success Metrics:**
- Patient capacity: +50% with same hours
- Passive income: Courses, meal plan marketplace
- Influence: 1000+ followers
- Time per patient: -40%
- Practice valuation: +$200K (for sale)

---

## 3. Core Features - Detailed Specifications

### 3.1 SOCIAL NETWORK: "La Familia Saludable" 🇲🇽

#### 3.1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     LA FAMILIA SALUDABLE                     │
│                  (Mexican Health Family Network)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┬──────────────┐
                              │                 │              │
                     ┌────────▼───────┐  ┌─────▼─────┐  ┌─────▼─────┐
                     │   PATIENT      │  │ NUTRITIONIST│  │  FAMILY   │
                     │  COMMUNITY     │  │  COMMUNITY  │  │  CIRCLES  │
                     │                │  │             │  │           │
                     │ • Feed         │  │ • Prof. Feed│  │• Private  │
                     │ • Groups       │  │ • Forums    │  │  Groups   │
                     │ • Challenges   │  │ • Resources │  │• Shared   │
                     │ • Recipes      │  │ • Network   │  │  Goals    │
                     └────────────────┘  └─────────────┘  └───────────┘
```

#### 3.1.2 Feed System (Patient Community)

**User Story:**
> As a patient, I want to see inspiring posts from people like me so that I stay motivated on my health journey.

**Acceptance Criteria:**
- ✅ Infinite scroll feed with pagination (20 posts/page)
- ✅ Personalized algorithm shows relevant content (same goals, same nutritionist, same region)
- ✅ Post types: Text, Photo, Progress, Recipe, Question
- ✅ Interactions: Like (corazón ❤️), Support (aplauso 👏), Inspire (fuego 🔥), Save (bookmark 🔖)
- ✅ Comments with nested replies (max 3 levels)
- ✅ Real-time updates (new posts appear with notification)
- ✅ Content moderation (AI + human review for harmful content)

**Technical Specs:**

```typescript
// Post Entity
interface Post {
  id: string; // UUID
  author_id: string; // User ID
  author_type: 'patient' | 'nutritionist' | 'admin';

  // Content
  type: 'text' | 'photo' | 'progress' | 'recipe' | 'question' | 'achievement';
  title?: string;
  body: string; // Markdown support
  media_urls: string[]; // Array of image/video URLs

  // For progress posts
  progress_data?: {
    weight_before_kg: number;
    weight_after_kg: number;
    weight_lost_kg: number;
    time_period_days: number;
    photo_before_url: string;
    photo_after_url: string;
  };

  // For recipe posts
  recipe_data?: {
    recipe_id: string; // Link to Recipe entity
    prep_time_min: number;
    servings: number;
    calories_per_serving: number;
    difficulty: 'easy' | 'medium' | 'hard';
  };

  // For achievement posts
  achievement_data?: {
    badge_id: string;
    badge_name: string;
    badge_icon_url: string;
    description: string;
  };

  // Metadata
  created_at: Date;
  updated_at: Date;
  is_edited: boolean;
  edited_at?: Date;

  // Visibility & Privacy
  visibility: 'public' | 'followers' | 'private_group' | 'nutritionist_only';
  group_id?: string; // If posted in a group

  // Engagement metrics
  likes_count: number;
  comments_count: number;
  shares_count: number;
  saves_count: number;
  views_count: number;

  // Reactions breakdown
  reactions: {
    heart: number;      // ❤️ Me gusta
    clap: number;       // 👏 Apoyo
    fire: number;       // 🔥 Inspirador
    strong: number;     // 💪 Fuerza
    celebrate: number;  // 🎉 Celebración
  };

  // Moderation
  is_flagged: boolean;
  flag_reason?: string;
  is_approved: boolean;
  moderated_by?: string;
  moderated_at?: Date;

  // Virality tracking
  virality_score: number; // 0-100, calculated by engagement
  is_trending: boolean;
  is_featured: boolean; // Curated by team

  // Tags & Search
  tags: string[]; // ["diabetes", "recetas", "bajarpeso"]
  mentioned_users: string[]; // @username mentions

  // Location (optional)
  state?: string; // Estado de México
  city?: string;
}

// Comment Entity
interface Comment {
  id: string;
  post_id: string;
  author_id: string;
  parent_comment_id?: string; // For nested replies

  content: string;
  created_at: Date;
  updated_at: Date;
  is_edited: boolean;

  likes_count: number;
  is_flagged: boolean;

  // Depth tracking (max 3 levels)
  depth_level: number; // 0 = top-level, 1 = reply, 2 = reply to reply
}

// Reaction Entity
interface Reaction {
  id: string;
  user_id: string;
  post_id: string;
  reaction_type: 'heart' | 'clap' | 'fire' | 'strong' | 'celebrate';
  created_at: Date;

  // Prevent double reactions
  UNIQUE_CONSTRAINT: (user_id, post_id)
}
```

**Feed Ranking Algorithm:**

```python
def calculate_feed_score(post, current_user):
    """
    Personalized feed ranking inspired by Facebook/Instagram algorithms
    """
    score = 0

    # 1. Recency (0-30 points)
    hours_old = (now() - post.created_at).total_seconds() / 3600
    if hours_old < 1:
        score += 30
    elif hours_old < 6:
        score += 25
    elif hours_old < 24:
        score += 15
    elif hours_old < 72:
        score += 5

    # 2. Engagement Rate (0-25 points)
    engagement_rate = (post.likes_count + post.comments_count * 3) / max(post.views_count, 1)
    score += min(engagement_rate * 100, 25)

    # 3. Personal Relevance (0-20 points)
    # Same nutritionist
    if post.author.nutritionist_id == current_user.nutritionist_id:
        score += 10
    # Similar goals
    if overlap(post.author.goals, current_user.goals):
        score += 5
    # Same region
    if post.state == current_user.state:
        score += 5

    # 4. Content Type Preference (0-15 points)
    user_preferences = get_user_content_preferences(current_user)
    if post.type in user_preferences.top_types:
        score += 15

    # 5. Author Popularity (0-10 points)
    author_followers = get_follower_count(post.author_id)
    if author_followers > 1000:
        score += 10
    elif author_followers > 500:
        score += 7
    elif author_followers > 100:
        score += 4

    # 6. Trending Bonus (0-10 points)
    if post.is_trending:
        score += 10

    # 7. Diversity Penalty
    # Prevent feed from being dominated by single user
    recent_posts_from_author = count_recent_posts_in_feed(post.author_id, current_user)
    if recent_posts_from_author > 2:
        score -= 15

    # 8. Quality Signals (0-10 points)
    if post.has_media:
        score += 3
    if len(post.body) > 100:  # Substantial content
        score += 2
    if post.comments_count > 5:  # Generates discussion
        score += 5

    return max(score, 0)
```

#### 3.1.3 Groups System

**User Story:**
> As a patient, I want to join groups of people with similar goals (e.g., "Madres con Diabetes", "Runners CDMX") so I can find targeted support.

**Group Types:**

```typescript
enum GroupType {
  OPEN = 'open',              // Anyone can join, anyone can see
  CLOSED = 'closed',          // Anyone can see, must request to join
  PRIVATE = 'private',        // Invite-only, hidden from search
  NUTRITIONIST_ONLY = 'nutritionist_only',
  PATIENT_ONLY = 'patient_only',
}

interface Group {
  id: string;
  name: string;
  description: string;
  cover_image_url: string;
  icon_url: string;

  type: GroupType;
  category: 'goal_based' | 'condition_based' | 'location_based' | 'nutritionist_practice' | 'other';

  // Example categories:
  // - "Pérdida de peso"
  // - "Diabetes Tipo 2"
  // - "Mamás lactando"
  // - "Vegetarianos"
  // - "Runners"
  // - "Pacientes de Dra. Sara"

  created_by: string; // User ID
  admins: string[]; // Multiple admins
  moderators: string[];

  member_count: number;
  post_count: number;

  // Rules
  rules: {
    title: string;
    description: string;
  }[];

  // Posting permissions
  who_can_post: 'everyone' | 'admins_only' | 'approved_members';
  require_post_approval: boolean;

  // Joining
  requires_approval: boolean;
  join_questions?: {
    question: string;
    required: boolean;
  }[];

  // Engagement
  activity_level: 'very_active' | 'active' | 'moderate' | 'low'; // Calculated
  last_post_at: Date;

  // Discovery
  tags: string[];
  state?: string; // For location-based groups
  is_featured: boolean;

  created_at: Date;
  updated_at: Date;
}

interface GroupMember {
  group_id: string;
  user_id: string;
  role: 'admin' | 'moderator' | 'member' | 'pending';

  joined_at: Date;
  invited_by?: string;

  // Engagement tracking
  posts_count: number;
  comments_count: number;
  last_active_at: Date;

  // Notifications
  notification_preference: 'all' | 'mentions_only' | 'none';

  // Answers to join questions
  join_answers?: {
    question: string;
    answer: string;
  }[];
}
```

**Pre-Seeded Groups (Launch Day):**

```json
[
  {
    "name": "🏃‍♀️ Runners Saludables",
    "description": "Comunidad de corredores que buscan mejorar su nutrición deportiva",
    "category": "goal_based",
    "type": "open"
  },
  {
    "name": "💪 Madres Guerreras",
    "description": "Mamás mexicanas recuperando su salud post-embarazo",
    "category": "goal_based",
    "type": "closed"
  },
  {
    "name": "🩺 Venciendo la Diabetes",
    "description": "Soporte para personas con diabetes tipo 2 y pre-diabetes",
    "category": "condition_based",
    "type": "closed"
  },
  {
    "name": "🌮 Tacos Saludables",
    "description": "Recetas mexicanas tradicionales versión saludable",
    "category": "other",
    "type": "open"
  },
  {
    "name": "🥑 Vegetarianos México",
    "description": "Nutrición vegetariana con sabor mexicano",
    "category": "goal_based",
    "type": "open"
  },
  {
    "name": "💼 Oficinistas Activos",
    "description": "Combatir el sedentarismo laboral y comer bien en la oficina",
    "category": "goal_based",
    "type": "open"
  }
]
```

#### 3.1.4 Challenges System

**User Story:**
> As a patient, I want to participate in weekly challenges so that I stay engaged and compete in a fun way.

**Challenge Types:**

```typescript
interface Challenge {
  id: string;
  title: string;
  description: string;
  banner_image_url: string;

  type: 'individual' | 'team' | 'community';
  category: 'weight_loss' | 'steps' | 'water' | 'meals' | 'exercise' | 'custom';

  // Scope
  scope: 'national' | 'state' | 'city' | 'group' | 'nutritionist_patients';
  state?: string; // If scope is state
  group_id?: string; // If scope is group
  nutritionist_id?: string; // If scope is nutritionist_patients

  // Timeline
  start_date: Date;
  end_date: Date;
  duration_days: number;
  status: 'upcoming' | 'active' | 'completed' | 'cancelled';

  // Goal
  goal_type: 'cumulative' | 'daily' | 'weekly' | 'threshold';
  goal_metric: string; // "steps", "kg_lost", "water_glasses", "meals_logged"
  goal_value: number; // Target value
  goal_unit: string; // "steps", "kg", "glasses", "meals"

  // Participation
  participant_count: number;
  max_participants?: number; // Null = unlimited
  requires_approval: boolean;

  // Rewards
  rewards: {
    rank: number; // 1 = first place
    reward_type: 'badge' | 'xp' | 'title' | 'feature';
    reward_value: string; // Badge ID or XP amount
    reward_description: string;
  }[];

  // Team challenges
  team_size?: number; // Null if individual
  teams?: {
    team_id: string;
    team_name: string;
    members: string[];
    score: number;
  }[];

  // Rules
  rules: string[];

  // Visibility
  is_featured: boolean;
  is_sponsored: boolean;
  sponsor_name?: string;
  sponsor_logo_url?: string;

  // Created by
  created_by: string; // User ID or 'system'
  created_by_type: 'admin' | 'nutritionist' | 'patient' | 'system';

  created_at: Date;
  updated_at: Date;
}

interface ChallengeParticipant {
  challenge_id: string;
  user_id: string;
  team_id?: string;

  // Progress tracking
  current_value: number; // Current progress (e.g., 5000 steps today)
  total_value: number; // Cumulative progress
  completion_percentage: number; // 0-100

  // Daily check-ins
  daily_progress: {
    date: Date;
    value: number;
    checked_in: boolean;
  }[];

  // Ranking
  rank: number; // Current position
  previous_rank?: number;

  // Status
  status: 'active' | 'completed' | 'dropped' | 'failed';

  joined_at: Date;
  completed_at?: Date;

  // Rewards earned
  rewards_earned: string[]; // Badge IDs
  xp_earned: number;
}
```

**Example Challenges (Pre-Seeded):**

```json
[
  {
    "title": "Reto Nacional: México Saludable 2025",
    "description": "10,000 mexicanos comprometidos a perder 50,000 kg en 6 meses. Juntos somos más fuertes 🇲🇽",
    "type": "community",
    "category": "weight_loss",
    "scope": "national",
    "start_date": "2025-02-01",
    "end_date": "2025-07-31",
    "duration_days": 180,
    "goal_type": "cumulative",
    "goal_metric": "kg_lost",
    "goal_value": 50000,
    "rewards": [
      {
        "rank": null,
        "reward_type": "badge",
        "reward_value": "mexico_saludable_2025",
        "reward_description": "Badge exclusivo para todos los participantes"
      }
    ]
  },
  {
    "title": "Semana del Nopal 🌵",
    "description": "Incluye nopal en al menos 5 comidas esta semana. ¡Redescubre este superalimento mexicano!",
    "type": "individual",
    "category": "meals",
    "scope": "national",
    "start_date": "2025-02-10",
    "end_date": "2025-02-16",
    "duration_days": 7,
    "goal_type": "threshold",
    "goal_metric": "nopal_meals",
    "goal_value": 5,
    "rewards": [
      {
        "rank": null,
        "reward_type": "badge",
        "reward_value": "guardian_nopal",
        "reward_description": "🌵 Guardián del Nopal"
      },
      {
        "rank": null,
        "reward_type": "xp",
        "reward_value": "100",
        "reward_description": "+100 XP"
      }
    ]
  },
  {
    "title": "Batalla de Estados: CDMX vs Jalisco",
    "description": "¿Qué estado perderá más peso colectivamente este mes?",
    "type": "team",
    "category": "weight_loss",
    "scope": "national",
    "start_date": "2025-02-01",
    "end_date": "2025-02-28",
    "team_size": null,
    "teams": [
      {"team_name": "CDMX", "state": "Ciudad de México"},
      {"team_name": "Jalisco", "state": "Jalisco"}
    ]
  },
  {
    "title": "30 Días de Hidratación",
    "description": "Toma 8 vasos de agua diarios durante 30 días consecutivos",
    "type": "individual",
    "category": "water",
    "scope": "national",
    "duration_days": 30,
    "goal_type": "daily",
    "goal_metric": "water_glasses",
    "goal_value": 8
  }
]
```

#### 3.1.5 Recipe Sharing & Cookbook

**User Story:**
> As a patient, I want to share my healthy versions of traditional Mexican recipes so others can benefit from my discoveries.

```typescript
interface Recipe {
  id: string;
  title: string;
  description: string;

  // Media
  main_photo_url: string;
  gallery_photos: string[];
  video_url?: string; // Tutorial video

  // Author
  author_id: string;
  author_type: 'patient' | 'nutritionist' | 'admin';
  is_verified: boolean; // Verified by nutritionist
  verified_by?: string; // Nutritionist ID

  // Categories
  meal_type: 'desayuno' | 'colacion' | 'comida' | 'cena' | 'postre' | 'bebida';
  cuisine_type: 'mexicana' | 'internacional' | 'fusion';
  dietary_tags: string[]; // ["vegetarian", "gluten_free", "low_carb", "diabetic_friendly"]

  // Difficulty & Time
  difficulty: 'facil' | 'media' | 'dificil';
  prep_time_min: number;
  cook_time_min: number;
  total_time_min: number;
  servings: number;

  // Cost
  cost_estimate_mxn: number;
  cost_level: 'economico' | 'moderado' | 'caro';

  // Cultural
  is_traditional_mexican: boolean;
  region_origin?: string; // "Oaxaca", "Veracruz", etc.
  history_story?: string; // Background on the dish

  // Ingredients
  ingredients: {
    name: string;
    quantity: number;
    unit: string; // "tazas", "piezas", "gramos"
    notes?: string; // "cortado en cubitos"
    is_optional: boolean;
    substitutions?: string[]; // Alternative ingredients
  }[];

  // Instructions
  instructions: {
    step_number: number;
    instruction: string;
    photo_url?: string;
    duration_min?: number;
  }[];

  // Nutrition (per serving)
  nutrition_per_serving: {
    calories: number;
    protein_g: number;
    carbs_g: number;
    fat_g: number;
    fiber_g: number;
    sugar_g: number;
    sodium_mg: number;

    // Equivalents (Mexican system)
    equivalents: string; // "1 cereal, 1 verdura, 1 grasa"
  };

  // Tips
  chef_tips: string[];
  storage_instructions: string;
  reheating_instructions?: string;

  // Engagement
  views_count: number;
  likes_count: number;
  saves_count: number;
  tried_count: number; // Users who marked "I made this"
  rating_average: number; // 1-5 stars
  rating_count: number;

  // Collections
  is_featured: boolean;
  is_trending: boolean;
  is_seasonal: boolean;
  season?: string; // "primavera", "verano", etc.

  // Moderation
  is_published: boolean;
  is_flagged: boolean;
  moderation_status: 'pending' | 'approved' | 'rejected';
  moderation_notes?: string;

  // Metadata
  created_at: Date;
  updated_at: Date;
  published_at?: Date;

  // Search & Discovery
  tags: string[];
  search_keywords: string[]; // Generated automatically
}

interface RecipeReview {
  id: string;
  recipe_id: string;
  user_id: string;

  rating: number; // 1-5
  title: string;
  review_text: string;

  // Did they modify it?
  did_modify: boolean;
  modifications?: string;

  // Photos of their result
  result_photos: string[];

  helpful_count: number; // How many found this review helpful

  created_at: Date;
  updated_at: Date;
}
```

**Recipe Discovery Feed Algorithm:**

```python
def get_personalized_recipes(user):
    """
    Personalized recipe recommendations
    """
    recipes = []

    # 1. Based on user's diet plan
    user_diet = get_current_diet(user)
    if user_diet:
        recipes += get_recipes_matching_diet(user_diet, limit=10)

    # 2. Based on user's saved recipes
    saved_recipes = get_saved_recipes(user)
    similar_recipes = get_similar_recipes(saved_recipes, limit=10)
    recipes += similar_recipes

    # 3. Based on dietary restrictions
    user_restrictions = get_dietary_restrictions(user)
    filtered_recipes = filter_by_restrictions(recipes, user_restrictions)

    # 4. Trending in user's state
    state_trending = get_trending_recipes(user.state, limit=5)
    recipes += state_trending

    # 5. From nutritionist
    if user.nutritionist_id:
        nutritionist_recipes = get_recipes_by_nutritionist(user.nutritionist_id, limit=5)
        recipes += nutritionist_recipes

    # 6. Seasonal recipes
    current_season = get_current_season()
    seasonal = get_seasonal_recipes(current_season, limit=5)
    recipes += seasonal

    # Deduplicate and rank
    recipes = deduplicate(recipes)
    recipes = rank_by_relevance(recipes, user)

    return recipes
```

#### 3.1.6 Family Circles (Unique Feature)

**User Story:**
> As a patient, I want my family members to be part of my health journey, even if they don't have their own nutrition goals, so they can support me and see my progress.

**Concept:**
Unlike traditional health apps, **Family Circles** allow patients to create private groups with family members + their nutritionist. This reflects the Mexican value of "familismo" where family is central to everything.

```typescript
interface FamilyCircle {
  id: string;
  name: string; // "Familia López Saludable"
  description?: string;
  cover_photo_url: string;

  // Owner (patient)
  owner_id: string;
  nutritionist_id: string; // The nutritionist is auto-included

  // Members
  members: {
    user_id: string;
    role: 'owner' | 'family_member' | 'nutritionist' | 'support_friend';
    relationship: string; // "esposo", "mamá", "hijo", "mejor amiga"

    // Permissions
    can_view_progress: boolean; // See weight, measurements
    can_view_meal_log: boolean;
    can_post: boolean;
    can_comment: boolean;
    can_give_encouragement: boolean; // Send encouraging stickers/GIFs

    joined_at: Date;
    last_active_at: Date;
  }[];

  // Privacy settings
  share_progress_automatically: boolean; // Auto-post weekly progress
  share_achievements: boolean; // Auto-post when badge earned
  share_meal_logs: boolean;

  // Family Activities
  family_challenges?: {
    challenge_id: string;
    challenge_name: string;
    participating_members: string[];
  }[];

  // Shared goals
  family_goals: {
    goal_type: 'cook_together' | 'walk_together' | 'meal_prep_sunday' | 'custom';
    description: string;
    frequency: 'daily' | 'weekly';
    participants: string[];
    completed_count: number;
  }[];

  // Family recipes
  family_recipes: string[]; // Recipe IDs shared in circle

  created_at: Date;
  updated_at: Date;
}
```

**Example Use Cases:**

```
Use Case 1: "Apoyo Familiar"
María (patient) creates a Family Circle with:
- Her husband Carlos (can see progress, post encouragement)
- Her mother (can share recipes, comment)
- Her nutritionist Dra. Sara (can post tips, adjust plan)

When María completes 7 days streak:
→ Auto-posted to Family Circle
→ Carlos gets notification: "María completó 7 días 🔥 ¡Dale ánimos!"
→ He taps "¡Felicidades! 🎉" (quick encouragement button)

---

Use Case 2: "Reto Familiar"
The López family (4 members) all want to be healthier:
- Papá: Lose 15kg (has nutritionist)
- Mamá: Lose 10kg (has nutritionist)
- Hijo (16): Build muscle (patient of same nutritionist)
- Hija (12): Learn healthy habits (observer)

They create "Reto Familia López":
- Shared goal: Walk together 30 min daily
- Shared meal planning (everyone eats same meals)
- Shared progress dashboard
- Weekly family challenge

---

Use Case 3: "Abuelita Monitora"
Don Pedro (65) has diabetes. His daughter lives in US.
- Family Circle allows daughter to monitor remotely
- Gets notification if he misses logging meals 2 days in row
- Can video call with him + nutritionist together
- Shares recipes from US that daughter has modified
```

**Family Circle Dashboard:**

```
┌─────────────────────────────────────────────────────┐
│          🏠 Familia López Saludable                 │
├─────────────────────────────────────────────────────┤
│ Miembros (5)                                        │
│ ┌──┬──┬──┬──┬──┐                                   │
│ │😊│👨│👩│👦│👨‍⚕️│                                 │
│ └──┴──┴──┴──┴──┘                                   │
│ María Carlos Ana Jr. Dra.Sara                      │
│                                                     │
├─────────────────────────────────────────────────────┤
│ 📊 Progreso Colectivo (Este Mes)                   │
│ • Comidas saludables: 78/90 ✅                      │
│ • Caminatas familiares: 12/12 ✅                    │
│ • Peso perdido total: 8.5 kg 🎉                    │
│                                                     │
├─────────────────────────────────────────────────────┤
│ 🔥 Actividad Reciente                              │
│                                                     │
│ María 📸                           Hace 2h         │
│ "Preparé los tacos de pescado     [❤️ 4] [💬 2]  │
│  que compartió Dra. Sara!"                         │
│  [Foto de tacos]                                   │
│                                                     │
│ Carlos 💬                          Hace 3h         │
│ "¡Vamos María! Ya casi llegas                      │
│  a tu meta 💪"                                     │
│                                                     │
│ Dra. Sara 📝                      Ayer            │
│ "Tip familiar: Esta semana        [❤️ 5]         │
│  intenten cocinar juntos el                        │
│  domingo. Adjunto recetas →"                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

*[Continued in next section due to length...]*

This is Part 1 of the MD050-PRD document. The document is too large (200+ pages) to fit in one response.

**Shall I continue with:**
- Part 2: Nutritionist Community Features
- Part 3: Gamification Specifications
- Part 4: AI Features
- Part 5: Technical Architecture
- Part 6: Database Schemas

Or would you like me to proceed directly to creating the **MD070 Technical Design Document**?

Let me know which direction you'd like me to take! 🚀