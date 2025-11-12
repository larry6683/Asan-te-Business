#!/usr/bin/env python3
"""
Test frontend analytics integration
Queries the database to verify tracking data
"""
import psycopg2
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="asante_dev",
    password="password"
)
cur = conn.cursor()

print("=" * 60)
print("FRONTEND ANALYTICS VERIFICATION")
print("=" * 60)

# 1. Check if registration steps exist
print("\n1️⃣ REGISTRATION STEPS IN DATABASE:")
print("-" * 60)
cur.execute("""
    SELECT code, step_name, step_order, description
    FROM analytics.registration_step
    ORDER BY step_order
""")
steps = cur.fetchall()
if steps:
    for code, name, order, desc in steps:
        print(f"   Step {code}: {name} (order: {order})")
else:
    print("   ❌ No steps found! Run seed script.")

# 2. Check recent interactions
print("\n2️⃣ RECENT REGISTRATION INTERACTIONS:")
print("-" * 60)
cur.execute("""
    SELECT 
        ri.session_id,
        ri.app_user_id,
        rs.step_name,
        ri.step_began_at,
        ri.step_completed_at,
        EXTRACT(EPOCH FROM (ri.step_completed_at - ri.step_began_at)) as duration
    FROM analytics.registration_interaction ri
    JOIN analytics.registration_step rs ON ri.registration_step_id = rs.registration_step_id
    ORDER BY ri.step_began_at DESC
    LIMIT 20
""")
interactions = cur.fetchall()
if interactions:
    for session, user, step, began, completed, duration in interactions:
        status = "✅ Completed" if completed else "⏳ In Progress"
        duration_str = f"{duration:.1f}s" if duration else "N/A"
        print(f"   {step}: {status} (duration: {duration_str})")
        print(f"      Session: {session}")
        if user:
            print(f"      User: {user}")
else:
    print("   ℹ️ No interactions found yet")

# 3. Check sessions with most activity
print("\n3️⃣ SESSIONS BY ACTIVITY:")
print("-" * 60)
cur.execute("""
    SELECT 
        session_id,
        COUNT(*) as step_count,
        COUNT(DISTINCT registration_step_id) as unique_steps,
        MIN(step_began_at) as first_step,
        MAX(step_began_at) as last_step
    FROM analytics.registration_interaction
    GROUP BY session_id
    ORDER BY step_count DESC
    LIMIT 5
""")
sessions = cur.fetchall()
if sessions:
    for session, count, unique, first, last in sessions:
        print(f"   Session: {session}")
        print(f"      Total interactions: {count}")
        print(f"      Unique steps: {unique}/6")
        print(f"      Duration: {first} to {last}")
        print()
else:
    print("   ℹ️ No sessions found yet")

# 4. Check completion funnel
print("\n4️⃣ REGISTRATION FUNNEL:")
print("-" * 60)
cur.execute("""
    SELECT 
        rs.code,
        rs.step_name,
        COUNT(DISTINCT ri.session_id) as sessions_reached,
        COUNT(CASE WHEN ri.step_completed_at IS NOT NULL THEN 1 END) as sessions_completed
    FROM analytics.registration_step rs
    LEFT JOIN analytics.registration_interaction ri ON rs.registration_step_id = ri.registration_step_id
    GROUP BY rs.code, rs.step_name
    ORDER BY rs.code
""")
funnel = cur.fetchall()
if funnel:
    for code, name, reached, completed in funnel:
        completion_rate = (completed / reached * 100) if reached > 0 else 0
        print(f"   Step {code} ({name}): {reached} reached, {completed} completed ({completion_rate:.1f}%)")
else:
    print("   ℹ️ No funnel data yet")

# 5. Check user journeys
print("\n5️⃣ COMPLETE USER JOURNEYS:")
print("-" * 60)
cur.execute("""
    SELECT 
        app_user_id,
        COUNT(*) as steps_taken,
        MIN(step_began_at) as started,
        MAX(step_completed_at) as finished
    FROM analytics.registration_interaction
    WHERE app_user_id IS NOT NULL
    GROUP BY app_user_id
    HAVING COUNT(CASE WHEN step_completed_at IS NOT NULL THEN 1 END) >= 6
""")
complete_journeys = cur.fetchall()
if complete_journeys:
    print(f"   ✅ {len(complete_journeys)} users completed full registration")
    for user, steps, started, finished in complete_journeys[:5]:
        print(f"      User {user}: {steps} steps, {started} to {finished}")
else:
    print("   ℹ️ No completed journeys yet")

conn.close()

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)