"""
Analytics Seed Data Generator

Generates realistic registration_interaction test data based on patterns from
the CU Boulder Admin-Registration_Process-Datapipeline spreadsheet.

This simulates:
- 115 users with varying completion states (69 complete, 46 incomplete)
- Multiple sessions per user (1-10 sessions)
- Realistic step progression with timestamps
- Forward and backward navigation patterns
- Abandoned/paused registrations at various steps
"""

import sys
import os
from pathlib import Path
import uuid
from datetime import datetime, timedelta
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
project_root = Path(__file__).parent.parent.parent  # Goes up to database_schema_sqlalchemy
sys.path.insert(0, str(project_root))

from src.analytics.tables import RegistrationStep, RegistrationInteraction


def create_database_url(host="localhost", port="5432", user="asante_dev", password="password", database="postgres"):
    """Create database connection URL"""
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_registration_steps(session):
    """Get all registration steps ordered by step_order"""
    return session.query(RegistrationStep).order_by(RegistrationStep.step_order).all()


def generate_session_id():
    """Generate a random session ID"""
    return uuid.uuid4()


def generate_realistic_timestamp(base_time, min_seconds=10, max_seconds=300):
    """Generate a timestamp with realistic offset from base time"""
    offset = random.randint(min_seconds, max_seconds)
    return base_time + timedelta(seconds=offset)


def create_user_journey(session, app_user_id, user_email, completed, num_sessions, start_date, steps):
    """
    Create a realistic user journey through registration steps.
    
    Args:
        session: SQLAlchemy session
        app_user_id: UUID of the app_user (can be None for anonymous)
        user_email: Email for logging
        completed: Boolean - did user complete registration?
        num_sessions: How many sessions did user take?
        start_date: When registration started
        steps: List of RegistrationStep objects
    """
    print(f"  Creating journey for {user_email}: "
          f"{'completed' if completed else 'incomplete'}, {num_sessions} sessions")
    
    interactions = []
    current_time = start_date
    
    # Determine how far user progressed
    if completed:
        max_step_reached = len(steps)  # All 6 steps
    else:
        # Incomplete users stop at random step (2-5)
        max_step_reached = random.randint(2, 5)
    
    # Split steps across sessions
    steps_per_session = max_step_reached // num_sessions
    remaining_steps = max_step_reached % num_sessions
    
    session_steps = []
    for i in range(num_sessions):
        # Distribute steps across sessions
        steps_in_session = steps_per_session + (1 if i < remaining_steps else 0)
        session_steps.append(steps_in_session)
    
    current_step_idx = 0
    
    for session_num in range(num_sessions):
        session_id = generate_session_id()
        steps_in_this_session = session_steps[session_num]
        
        # Add gap between sessions (except first)
        if session_num > 0:
            gap_minutes = random.randint(30, 1440)  # 30 min to 24 hours
            current_time += timedelta(minutes=gap_minutes)
        
        for step_in_session in range(steps_in_this_session):
            if current_step_idx >= max_step_reached:
                break
                
            current_step = steps[current_step_idx]
            
            # Determine previous and next steps
            previous_step_id = steps[current_step_idx - 1].registration_step_id if current_step_idx > 0 else None
            
            # Check if this is the last step for this user
            is_last_step = (current_step_idx == max_step_reached - 1)
            
            if is_last_step and not completed:
                # Incomplete registration - no next step, no completion time
                next_step_id = None
                step_completed_at = None
            else:
                # Normal progression
                next_step_id = steps[current_step_idx + 1].registration_step_id if current_step_idx < len(steps) - 1 else None
                
                # Generate step completion time (varying durations)
                step_duration = random.randint(30, 600)  # 30 sec to 10 min
                step_completed_at = current_time + timedelta(seconds=step_duration)
            
            # Create interaction
            interaction = RegistrationInteraction(
                app_user_id=app_user_id,
                session_id=session_id,
                registration_step_id=current_step.registration_step_id,
                previous_step_id=previous_step_id,
                next_step_id=next_step_id,
                step_began_at=current_time,
                step_completed_at=step_completed_at
            )
            
            interactions.append(interaction)
            
            # Move time forward
            if step_completed_at:
                current_time = step_completed_at
                # Add small gap before next step
                current_time += timedelta(seconds=random.randint(2, 15))
            
            current_step_idx += 1
        
        # 20% chance of backward navigation (going back to previous step)
        if random.random() < 0.2 and current_step_idx > 1:
            # User goes back to previous step
            back_step_idx = current_step_idx - 2
            back_step = steps[back_step_idx]
            
            # Add small time gap
            current_time += timedelta(seconds=random.randint(10, 60))
            
            # Create backward interaction
            interaction = RegistrationInteraction(
                app_user_id=app_user_id,
                session_id=session_id,
                registration_step_id=back_step.registration_step_id,
                previous_step_id=steps[current_step_idx - 1].registration_step_id,
                next_step_id=back_step.registration_step_id,  # Points to same step (backward)
                step_began_at=current_time,
                step_completed_at=current_time + timedelta(seconds=random.randint(30, 180))
            )
            
            interactions.append(interaction)
            current_time = interaction.step_completed_at + timedelta(seconds=random.randint(5, 20))
    
    return interactions


def generate_test_data(database_url="postgresql://asante_dev:password@localhost:5432/postgres", num_users=115):
    """
    Generate test data matching patterns from the Excel spreadsheet.
    
    From Excel analysis:
    - 115 total users
    - 69 completed (60%)
    - 46 incomplete (40%)
    - Sessions range from 1-10
    - Mix of business, consumer, non-profit users
    """
    print("="*60)
    print("ANALYTICS SEED DATA GENERATION")
    print("="*60)
    print(f"\nGenerating data for {num_users} users...")
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Get registration steps
        steps = get_registration_steps(session)
        if len(steps) != 6:
            raise Exception(f"Expected 6 registration steps, found {len(steps)}")
        
        print(f"✅ Found {len(steps)} registration steps")
        
        # Get actual app_users from public schema (if they exist)
        # For now, we'll use NULL for app_user_id and just track by session
        # In real usage, the API would link session_id to app_user_id after authentication
        
        all_interactions = []
        
        # Generate base date range (last 90 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        # Generate users
        completed_count = int(num_users * 0.6)  # 60% complete
        incomplete_count = num_users - completed_count
        
        user_categories = ['business', 'consumer', 'nonprofit']
        
        for i in range(num_users):
            # Determine if this user completed
            is_completed = i < completed_count
            
            # Generate random attributes
            category = random.choice(user_categories)
            user_email = f"test_user_{i+1}@{category}.example.com"
            
            # Random start date in the past 90 days
            days_ago = random.randint(0, 90)
            user_start_date = end_date - timedelta(days=days_ago)
            
            # Number of sessions (weighted towards lower numbers)
            if is_completed:
                # Completed users: 1-7 sessions, weighted towards 1-3
                num_sessions = random.choices([1, 2, 3, 4, 5, 6, 7], weights=[30, 25, 20, 12, 7, 4, 2])[0]
            else:
                # Incomplete users: 1-10 sessions, more variety
                num_sessions = random.choices(range(1, 11), weights=[20, 18, 15, 12, 10, 8, 6, 5, 4, 2])[0]
            
            # For seed data, use NULL for app_user_id (simulating anonymous tracking)
            # In real scenario, this would be populated after authentication
            app_user_id = None
            
            # Generate journey
            journey_interactions = create_user_journey(
                session=session,
                app_user_id=app_user_id,
                user_email=user_email,
                completed=is_completed,
                num_sessions=num_sessions,
                start_date=user_start_date,
                steps=steps
            )
            
            all_interactions.extend(journey_interactions)
        
        # Bulk insert all interactions
        print(f"\n💾 Inserting {len(all_interactions)} interactions into database...")
        session.bulk_save_objects(all_interactions)
        session.commit()
        
        print(f"✅ Successfully created {len(all_interactions)} registration interactions")
        
        # Print statistics
        print("\n" + "="*60)
        print("DATA GENERATION SUMMARY")
        print("="*60)
        
        from sqlalchemy import func, case
        
        # Total interactions
        total = session.query(func.count(RegistrationInteraction.registration_interaction_id)).scalar()
        print(f"\nTotal interactions: {total}")
        
        # Completed vs incomplete
        completed_steps = session.query(
            func.count(RegistrationInteraction.registration_interaction_id)
        ).filter(RegistrationInteraction.step_completed_at.isnot(None)).scalar()
        
        incomplete_steps = session.query(
            func.count(RegistrationInteraction.registration_interaction_id)
        ).filter(RegistrationInteraction.step_completed_at.is_(None)).scalar()
        
        print(f"Completed step interactions: {completed_steps}")
        print(f"Incomplete step interactions: {incomplete_steps}")
        
        # Unique sessions
        unique_sessions = session.query(
            func.count(func.distinct(RegistrationInteraction.session_id))
        ).scalar()
        print(f"Unique sessions: {unique_sessions}")
        
        # Distribution by step
        print("\nInteractions per step:")
        step_counts = session.query(
            RegistrationStep.step_name,
            func.count(RegistrationInteraction.registration_interaction_id).label('count')
        ).join(
            RegistrationInteraction,
            RegistrationStep.registration_step_id == RegistrationInteraction.registration_step_id
        ).group_by(
            RegistrationStep.step_name,
            RegistrationStep.step_order
        ).order_by(
            RegistrationStep.step_order
        ).all()
        
        for step_name, count in step_counts:
            print(f"  {step_name}: {count}")
        
        session.close()
        
        print("\n" + "="*60)
        print("✅ SEED DATA GENERATION COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Verify data in pgAdmin: SELECT * FROM analytics.registration_interaction LIMIT 10;")
        print("2. Test analytics queries")
        print("3. Build API endpoints to track real registration data")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Seed data generation failed: {e}")
        import traceback
        traceback.print_exc()
        if 'session' in locals():
            session.rollback()
            session.close()
        return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate analytics seed data')
    parser.add_argument('--host', default='localhost', help='Database host')
    parser.add_argument('--port', default='5432', help='Database port')
    parser.add_argument('--user', default='asante_dev', help='Database user')
    parser.add_argument('--password', default='password', help='Database password')
    parser.add_argument('--database', default='postgres', help='Database name')
    parser.add_argument('--num-users', type=int, default=115, help='Number of test users to generate')
    
    args = parser.parse_args()
    
    database_url = create_database_url(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    success = generate_test_data(database_url, num_users=args.num_users)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())