# Database Schema Explanation (MySQL)

## Database Structure Overview

This SaaS platform uses a **multi-tenant architecture** where:
- **Shared tables**: Store tenant information and configurations
- **Tenant-specific tables**: Each company gets their own separate data

## Line-by-Line Schema Explanation (`database/schema.sql`)

### Lines 1-5: Database Creation
```sql
-- Create database
CREATE DATABASE IF NOT EXISTS saas_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE saas_platform;
```
**Simple Explanation:**
- Creates a new database called "saas_platform"
- `IF NOT EXISTS`: Only creates if it doesn't already exist
- `CHARACTER SET utf8mb4`: Supports international characters and emojis
- `COLLATE utf8mb4_unicode_ci`: Rules for sorting and comparing text
- `USE saas_platform`: Switch to using this database

### Lines 10-20: Multi-Tenant Client Table
```sql
CREATE TABLE IF NOT EXISTS django_tenants_client (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    schema_name VARCHAR(63) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_on DATETIME(6) NOT NULL,
    auto_create_schema BOOLEAN NOT NULL DEFAULT TRUE,
    auto_drop_schema BOOLEAN NOT NULL DEFAULT TRUE
);
```
**Simple Explanation:**
- **Purpose**: Stores information about each company using our platform
- `id`: Unique number for each company
- `schema_name`: Database schema name (like "company1", "company2")
- `name`: Company display name (like "Acme Corp")
- `created_on`: When company signed up
- `auto_create_schema`: Automatically create database space for company
- `auto_drop_schema`: Automatically remove database space when company leaves

### Lines 22-30: Domain Table
```sql
CREATE TABLE IF NOT EXISTS django_tenants_domain (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    domain VARCHAR(253) NOT NULL UNIQUE,
    tenant_id BIGINT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (tenant_id) REFERENCES django_tenants_client(id)
);
```
**Simple Explanation:**
- **Purpose**: Maps website domains to companies
- `domain`: Website URL (like "acme.ourapp.com")
- `tenant_id`: Links to which company owns this domain
- `is_primary`: Main domain for this company
- `FOREIGN KEY`: Ensures tenant_id refers to valid company

### Lines 35-50: User Table
```sql
CREATE TABLE IF NOT EXISTS auth_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6),
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined DATETIME(6) NOT NULL
);
```
**Simple Explanation:**
- **Purpose**: Stores user accounts (separate copy for each company)
- `password`: Encrypted password (never stored as plain text)
- `username`: Unique login name
- `email`: User's email address
- `is_superuser`: Can access admin features
- `is_staff`: Can access admin panel
- `is_active`: Account is enabled (false = disabled)
- `date_joined`: When user created account

### Lines 52-65: User Profiles
```sql
CREATE TABLE IF NOT EXISTS core_userprofile (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    phone_number VARCHAR(20) NOT NULL DEFAULT '',
    company VARCHAR(100) NOT NULL DEFAULT '',
    position VARCHAR(100) NOT NULL DEFAULT '',
    avatar VARCHAR(100) NOT NULL DEFAULT '',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id)
);
```
**Simple Explanation:**
- **Purpose**: Additional information about users
- `phone_number`: User's phone number
- `company`: Company they work for
- `position`: Job title
- `avatar`: Profile picture file path
- `timezone`: User's timezone (for displaying correct times)
- `user_id`: Links to auth_user table (one profile per user)

### Lines 67-80: Activity Tracking
```sql
CREATE TABLE IF NOT EXISTS core_activity (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    action VARCHAR(100) NOT NULL,
    description LONGTEXT NOT NULL,
    ip_address CHAR(39),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    INDEX idx_activity_user (user_id),
    INDEX idx_activity_created (created_at)
);
```
**Simple Explanation:**
- **Purpose**: Logs what users do (audit trail)
- `action`: What they did ("login", "create_project", etc.)
- `description`: Detailed description
- `ip_address`: User's internet address (for security)
- `INDEX`: Makes searching faster for user activities and by date

### Lines 85-100: Subscription Plans
```sql
CREATE TABLE IF NOT EXISTS subscriptions_subscriptionplan (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    name VARCHAR(100) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    description LONGTEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    billing_period VARCHAR(20) NOT NULL DEFAULT 'monthly',
    max_users INT NOT NULL,
    max_storage_gb INT NOT NULL,
    features JSON,
    stripe_price_id VARCHAR(100) NOT NULL DEFAULT ''
);
```
**Simple Explanation:**
- **Purpose**: Different pricing tiers (Starter, Pro, Enterprise)
- `name`: Plan name displayed to users
- `plan_type`: Internal code ("starter", "professional", etc.)
- `price`: Monthly cost in dollars
- `DECIMAL(10,2)`: Up to 10 digits, 2 decimal places (like 999999.99)
- `max_users`: How many team members allowed
- `max_storage_gb`: Storage limit in gigabytes
- `features`: JSON list of what's included
- `stripe_price_id`: Stripe payment system identifier

### Lines 102-120: User Subscriptions
```sql
CREATE TABLE IF NOT EXISTS subscriptions_subscription (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    stripe_subscription_id VARCHAR(100) NOT NULL DEFAULT '',
    current_period_start DATETIME(6) NOT NULL,
    current_period_end DATETIME(6) NOT NULL,
    trial_end DATETIME(6),
    user_id INT NOT NULL,
    plan_id BIGINT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    FOREIGN KEY (plan_id) REFERENCES subscriptions_subscriptionplan(id)
);
```
**Simple Explanation:**
- **Purpose**: Tracks which plan each user is paying for
- `status`: "active", "canceled", "past_due", etc.
- `current_period_start/end`: Current billing cycle dates
- `trial_end`: When free trial expires (if applicable)
- Links user to their chosen plan

### Lines 125-145: Invoices
```sql
CREATE TABLE IF NOT EXISTS subscriptions_invoice (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    stripe_invoice_id VARCHAR(100) NOT NULL DEFAULT '',
    amount_due DECIMAL(10,2) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(20) NOT NULL,
    due_date DATETIME(6) NOT NULL,
    paid_at DATETIME(6),
    subscription_id BIGINT NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions_subscription(id)
);
```
**Simple Explanation:**
- **Purpose**: Monthly bills and payment records
- `amount_due`: How much customer owes
- `amount_paid`: How much they've paid
- `due_date`: When payment is due
- `paid_at`: When they actually paid (null if unpaid)
- Links to specific subscription

### Lines 150-165: Usage Metrics
```sql
CREATE TABLE IF NOT EXISTS subscriptions_usagemetric (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    metric_type VARCHAR(50) NOT NULL,
    value DECIMAL(15,2) NOT NULL,
    date DATE NOT NULL,
    subscription_id BIGINT NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions_subscription(id),
    UNIQUE KEY unique_metric_per_day (subscription_id, metric_type, date)
);
```
**Simple Explanation:**
- **Purpose**: Tracks daily usage (API calls, storage, bandwidth)
- `metric_type`: What we're measuring ("api_calls", "storage_used")
- `value`: Amount used that day
- `UNIQUE KEY`: Prevents duplicate metrics for same day
- Used for billing and showing usage dashboards

### Lines 170-185: Projects
```sql
CREATE TABLE IF NOT EXISTS dashboard_project (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    name VARCHAR(200) NOT NULL,
    description LONGTEXT NOT NULL,
    color VARCHAR(7) NOT NULL DEFAULT '#6366f1',
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES auth_user(id)
);
```
**Simple Explanation:**
- **Purpose**: Work projects that users create
- `name`: Project name
- `color`: Color code for visual identification (hex format)
- `is_archived`: Hidden from main view but not deleted
- `owner_id`: Who created and owns this project

### Lines 190-205: Project Members
```sql
CREATE TABLE IF NOT EXISTS dashboard_projectmember (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    project_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES dashboard_project(id),
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    UNIQUE KEY unique_project_user (project_id, user_id)
);
```
**Simple Explanation:**
- **Purpose**: Who can access each project and their permission level
- `role`: "owner", "admin", "member", "viewer"
- `UNIQUE KEY`: Each user can only have one role per project
- Links projects to team members

### Lines 210-230: Tasks
```sql
CREATE TABLE IF NOT EXISTS dashboard_task (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    title VARCHAR(200) NOT NULL,
    description LONGTEXT NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    status VARCHAR(20) NOT NULL DEFAULT 'todo',
    due_date DATETIME(6),
    completed_at DATETIME(6),
    project_id BIGINT NOT NULL,
    assignee_id INT,
    creator_id INT NOT NULL
);
```
**Simple Explanation:**
- **Purpose**: Individual tasks within projects
- `priority`: "low", "medium", "high", "urgent"
- `status`: "todo", "in_progress", "review", "done"
- `due_date`: When task should be finished
- `completed_at`: When it was actually finished
- `assignee_id`: Who is responsible for the task
- `creator_id`: Who created the task

### Lines 270-290: Default Data Insertion
```sql
INSERT INTO subscriptions_subscriptionplan
(created_at, updated_at, name, plan_type, description, price, billing_period, max_users, max_storage_gb, features)
VALUES
(NOW(), NOW(), 'Starter', 'starter', 'Perfect for small teams getting started', 19.00, 'monthly', 5, 10,
 JSON_ARRAY('Basic analytics', 'Email support', '10GB storage', 'Up to 5 users'));
```
**Simple Explanation:**
- Automatically creates the three pricing plans (Starter, Professional, Enterprise)
- `NOW()`: Current timestamp
- `JSON_ARRAY()`: Creates a list in JSON format
- This data is available immediately when database is set up

### Lines 295-305: Performance Indexes
```sql
CREATE INDEX idx_user_email ON auth_user(email);
CREATE INDEX idx_user_username ON auth_user(username);
ALTER TABLE dashboard_task ADD FULLTEXT(title, description);
```
**Simple Explanation:**
- `CREATE INDEX`: Makes searching by email/username much faster
- `FULLTEXT`: Enables searching inside task titles and descriptions
- Indexes are like phone book - help find data quickly without checking every row

## Multi-Tenant Architecture Explanation

### How Multi-Tenancy Works:

1. **Shared Infrastructure**: One database server, one application
2. **Separate Schemas**: Each company gets their own "schema" (like a folder)
3. **Data Isolation**: Company A cannot see Company B's data
4. **Shared Configuration**: Subscription plans and tenant info are shared

### Example:
- **Shared**: `django_tenants_client`, `django_tenants_domain`, `subscriptions_subscriptionplan`
- **Tenant-Specific**: `auth_user`, `dashboard_project`, `dashboard_task`

### When Company "Acme Corp" Signs Up:
1. Record created in `django_tenants_client` with schema_name="acme"
2. Domain created: "acme.ourapp.com" pointing to this tenant
3. Separate database schema "acme" is created
4. All user data goes into "acme" schema, isolated from other companies

This design allows:
- **Scalability**: Thousands of companies on one system
- **Security**: Complete data isolation
- **Efficiency**: Shared infrastructure and updates
- **Customization**: Each company can have different configurations