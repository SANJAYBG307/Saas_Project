-- MySQL Database Schema for SaaS Platform
-- This file creates the database and initial setup

-- Create database
CREATE DATABASE IF NOT EXISTS saas_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE saas_platform;

-- Create users (this would be handled by Django migrations in production)
-- But here's the conceptual schema for reference

-- Multi-tenant schema structure
-- Django-tenants will create separate schemas for each tenant

-- Shared tables (available to all tenants)
CREATE TABLE IF NOT EXISTS django_tenants_client (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    schema_name VARCHAR(63) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_on DATETIME(6) NOT NULL,
    auto_create_schema BOOLEAN NOT NULL DEFAULT TRUE,
    auto_drop_schema BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS django_tenants_domain (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    domain VARCHAR(253) NOT NULL UNIQUE,
    tenant_id BIGINT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (tenant_id) REFERENCES django_tenants_client(id)
);

-- Example tenant-specific tables (these will be created in each tenant's schema)
-- User authentication and profiles
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

-- User profiles
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

-- Activity tracking
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

-- Subscription plans
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

-- User subscriptions
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
    FOREIGN KEY (plan_id) REFERENCES subscriptions_subscriptionplan(id),
    INDEX idx_subscription_user (user_id),
    INDEX idx_subscription_status (status)
);

-- Invoices
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
    FOREIGN KEY (subscription_id) REFERENCES subscriptions_subscription(id),
    INDEX idx_invoice_status (status),
    INDEX idx_invoice_due_date (due_date)
);

-- Usage metrics
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
    UNIQUE KEY unique_metric_per_day (subscription_id, metric_type, date),
    INDEX idx_usage_date (date),
    INDEX idx_usage_type (metric_type)
);

-- Projects
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
    FOREIGN KEY (owner_id) REFERENCES auth_user(id),
    INDEX idx_project_owner (owner_id),
    INDEX idx_project_active (is_active, is_archived)
);

-- Project members
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
    UNIQUE KEY unique_project_user (project_id, user_id),
    INDEX idx_member_user (user_id),
    INDEX idx_member_role (role)
);

-- Tasks
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
    creator_id INT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES dashboard_project(id),
    FOREIGN KEY (assignee_id) REFERENCES auth_user(id),
    FOREIGN KEY (creator_id) REFERENCES auth_user(id),
    INDEX idx_task_assignee (assignee_id),
    INDEX idx_task_status (status),
    INDEX idx_task_due_date (due_date),
    INDEX idx_task_priority (priority)
);

-- Comments
CREATE TABLE IF NOT EXISTS dashboard_comment (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    content LONGTEXT NOT NULL,
    task_id BIGINT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES dashboard_task(id),
    FOREIGN KEY (author_id) REFERENCES auth_user(id),
    INDEX idx_comment_task (task_id),
    INDEX idx_comment_author (author_id)
);

-- Dashboard widgets
CREATE TABLE IF NOT EXISTS dashboard_dashboardwidget (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    widget_type VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    configuration JSON,
    position_x INT NOT NULL DEFAULT 0,
    position_y INT NOT NULL DEFAULT 0,
    width INT NOT NULL DEFAULT 4,
    height INT NOT NULL DEFAULT 4,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    INDEX idx_widget_user (user_id),
    INDEX idx_widget_position (position_y, position_x)
);

-- Insert default subscription plans
INSERT INTO subscriptions_subscriptionplan
(created_at, updated_at, name, plan_type, description, price, billing_period, max_users, max_storage_gb, features)
VALUES
(NOW(), NOW(), 'Starter', 'starter', 'Perfect for small teams getting started', 19.00, 'monthly', 5, 10,
 JSON_ARRAY('Basic analytics', 'Email support', '10GB storage', 'Up to 5 users')),

(NOW(), NOW(), 'Professional', 'professional', 'Best for growing businesses', 49.00, 'monthly', 25, 100,
 JSON_ARRAY('Advanced analytics', 'Priority support', '100GB storage', 'Up to 25 users', 'API access', 'Custom integrations')),

(NOW(), NOW(), 'Enterprise', 'enterprise', 'For large organizations', 99.00, 'monthly', -1, -1,
 JSON_ARRAY('Enterprise analytics', '24/7 phone support', 'Unlimited storage', 'Unlimited users', 'White-label options', 'Custom development'));

-- Create indexes for performance
CREATE INDEX idx_user_email ON auth_user(email);
CREATE INDEX idx_user_username ON auth_user(username);
CREATE INDEX idx_user_active ON auth_user(is_active);

-- Full-text search indexes
ALTER TABLE dashboard_task ADD FULLTEXT(title, description);
ALTER TABLE dashboard_project ADD FULLTEXT(name, description);