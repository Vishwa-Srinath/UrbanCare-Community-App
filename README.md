# 🏙️ UrbanCare: Urban Infrastructure Management System

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![PostGIS](https://img.shields.io/badge/PostGIS-1E8C45?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)

> **UrbanCare** is a comprehensive, hybrid mobile and web platform designed to bridge the gap between citizens and municipal authorities. It enables real-time reporting, tracking, and resolution of urban infrastructure issues (e.g., road damage, water leaks, streetlight failures) using location-based services and an automated performance leaderboard.

Developed as a group project applying strict **Object-Oriented Software Development (OOSD)** principles.

---

## 📸 System Overview
*[📸 DEAR VISITOR: ADD YOUR HIGH-LEVEL PROJECT OVERVIEW DRAW.IO DIAGRAM HERE - Showing Flutter Mobile -> FastAPI -> PostgreSQL & Firebase]*

---

## 👨‍💻 My Role: Database Lead & Architect
While UrbanCare is a collaborative team effort, this specific fork highlights my contributions as the **Database Architect and Lead**. 

My primary responsibility was to design, optimize, and deploy a robust, scalable data foundation capable of handling real-time GPS queries, complex hierarchical user roles, and high-volume audit logs. 

**Key Engineering Achievements:**
* **100% PostgreSQL Strategy:** Eliminated the need for a secondary NoSQL database by utilizing PostgreSQL's native `JSONB` capabilities for flexible notification and activity log payloads.
* **Spatial Engineering:** Implemented **PostGIS** to handle advanced geographic mapping, enabling a battery-safe, OS-level geofencing strategy via `ST_DWithin()` spatial queries.
* **Cloud & Edge:** Deployed the production database via **Supabase**, integrating smoothly with Firebase Storage for decentralized image hosting (storing only CDN URLs in the DB).
* **Database-Level Automation:** Built complex PL/pgSQL triggers to automate timestamp updates, calculate authority leaderboard points, and ensure referential integrity (`ON DELETE CASCADE`).

---

## 🏗️ Database Architecture (v4)

The database schema is heavily normalized and strictly adheres to Object-Oriented Inheritance patterns.

### 1. The Identity Layer (Inheritance Pattern)
To satisfy OOSD requirements, the database uses a 1:1 table inheritance structure.
* `users`: The base core class handling authentication, hashing, and roles.
* `citizens`: Inherits from `users`. Stores specific contact and reputation data.
* `authorities`: Inherits from `users`. Links to the `departments` table and tracks resolution performance.

*[📸 INSERT YOUR DRAW.IO "LAYER 02: IDENTITY & INHERITANCE" DIAGRAM HERE]*

### 2. The Transactional Layer (Complaints & Auditing)
The `complaints` table acts as the central hub connecting Citizens, Authorities, and Locations. 
* Enforces data integrity through `complaint_status` ENUMs.
* Every status change automatically writes an immutable record to the `status_updates` audit table.
* Image processing is offloaded to Firebase, with the `complaint_images` table storing 1-to-Many relationships for visual proof (before/after photos).

*[📸 INSERT YOUR DRAW.IO "LAYER 04: ERD / TABLE RELATIONSHIPS" DIAGRAM HERE]*

### 3. The Spatial Layer (PostGIS Geofencing)
To solve the issue of continuous GPS polling draining mobile batteries, the database utilizes a lightweight PostGIS View: `active_complaint_points`.

When a user opens the app, the backend queries this view to fetch the nearest unresolved issues using spatial indexes (`GIST`). The mobile OS then registers low-power geofences for these exact coordinates.

```sql
-- Core Geofencing Query Example
SELECT complaint_id, issue_type, latitude, longitude 
FROM active_complaint_points 
WHERE ST_DWithin(geom, ST_MakePoint($1,$2)::geography, 5000);
