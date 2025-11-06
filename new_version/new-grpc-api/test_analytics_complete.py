#!/usr/bin/env python3
"""
Test script for Analytics Service
"""
import grpc
import sys
import uuid
from datetime import datetime, timedelta

# Add path for imports
sys.path.insert(0, 'src')

from codegen.analytics import analytics_pb2, analytics_pb2_grpc
from codegen.error import error_pb2

def test_analytics_service():
    """Test all Analytics Service endpoints"""
    channel = grpc.insecure_channel('localhost:50054')
    stub = analytics_pb2_grpc.AnalyticsServiceStub(channel)
    
    print("\n" + "=" * 60)
    print("ANALYTICS SERVICE TEST")
    print("=" * 60)
    
    # Test 1: Get Registration Steps
    print("\n1. Getting Registration Steps...")
    try:
        response = stub.GetRegistrationSteps(analytics_pb2.GetRegistrationStepsRequest())
        if response.errors:
            print(f"   ✗ Errors: {[e.message for e in response.errors]}")
        else:
            print(f"   ✓ Found {len(response.steps)} registration steps:")
            for step in response.steps:
                print(f"     {step.step_order}. {step.step_name} (code={step.code})")
    except grpc.RpcError as e:
        print(f"   ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Test 2: Track Step - Start registration
    print("\n2. Tracking Registration Steps...")
    session_id = str(uuid.uuid4())
    interaction_ids = []
    
    try:
        # Track signup step
        print(f"   Session ID: {session_id}")
        print("   a. Tracking signup step...")
        response = stub.TrackStep(analytics_pb2.TrackStepRequest(
            session_id=session_id,
            step_code=1  # signup
        ))
        
        if response.errors:
            print(f"      ✗ Errors: {[e.message for e in response.errors]}")
        else:
            interaction_ids.append(response.interaction.id)
            print(f"      ✓ Tracked: {response.interaction.id}")
            
            # Complete the signup step
            print("   b. Completing signup step...")
            complete_response = stub.CompleteStep(analytics_pb2.CompleteStepRequest(
                interaction_id=response.interaction.id,
                next_step_code=2  # verification
            ))
            
            if complete_response.errors:
                print(f"      ✗ Errors: {[e.message for e in complete_response.errors]}")
            else:
                print(f"      ✓ Completed: {complete_response.interaction.step_completed_at}")
        
        # Track verification step
        print("   c. Tracking verification step...")
        response = stub.TrackStep(analytics_pb2.TrackStepRequest(
            session_id=session_id,
            step_code=2,  # verification
            previous_step_code=1  # signup
        ))
        
        if response.errors:
            print(f"      ✗ Errors: {[e.message for e in response.errors]}")
        else:
            interaction_ids.append(response.interaction.id)
            print(f"      ✓ Tracked: {response.interaction.id}")
            
            # Complete verification
            complete_response = stub.CompleteStep(analytics_pb2.CompleteStepRequest(
                interaction_id=response.interaction.id,
                next_step_code=3  # first_login
            ))
            print(f"      ✓ Completed verification")
        
        # Track first_login step with user_id (simulate authenticated user)
        print("   d. Tracking first_login step (with user ID)...")
        test_user_id = str(uuid.uuid4())
        response = stub.TrackStep(analytics_pb2.TrackStepRequest(
            session_id=session_id,
            app_user_id=test_user_id,
            step_code=3,  # first_login
            previous_step_code=2  # verification
        ))
        
        if response.errors:
            print(f"      ✗ Errors: {[e.message for e in response.errors]}")
        else:
            interaction_ids.append(response.interaction.id)
            print(f"      ✓ Tracked with user: {response.interaction.app_user_id[:8]}...")
            
    except grpc.RpcError as e:
        print(f"   ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Test 3: Get Session Journey
    print("\n3. Getting Session Journey...")
    try:
        response = stub.GetSessionJourney(analytics_pb2.GetSessionJourneyRequest(
            session_id=session_id
        ))
        
        if response.errors:
            print(f"   ✗ Errors: {[e.message for e in response.errors]}")
        else:
            print(f"   ✓ Found {len(response.interactions)} interactions in session:")
            for i, interaction in enumerate(response.interactions):
                completed = "✓" if interaction.step_completed_at else "○"
                print(f"     {i+1}. Step {interaction.registration_step_id[:8]}... [{completed}]")
    except grpc.RpcError as e:
        print(f"   ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Test 4: Get User Journey (if we have a user_id)
    if test_user_id:
        print("\n4. Getting User Journey...")
        try:
            response = stub.GetUserJourney(analytics_pb2.GetUserJourneyRequest(
                app_user_id=test_user_id
            ))
            
            if response.errors:
                print(f"   ✗ Errors: {[e.message for e in response.errors]}")
            else:
                print(f"   ✓ Found {len(response.interactions)} interactions for user")
        except grpc.RpcError as e:
            print(f"   ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Test 5: Get Registration Stats
    print("\n5. Getting Registration Statistics...")
    try:
        # Get stats for today
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        response = stub.GetRegistrationStats(analytics_pb2.GetRegistrationStatsRequest(
            start_date=yesterday.isoformat(),
            end_date=today.isoformat()
        ))
        
        if response.errors:
            print(f"   ✗ Errors: {[e.message for e in response.errors]}")
        else:
            stats = response.stats
            print(f"   ✓ Statistics (last 24 hours):")
            print(f"     - Total Sessions: {stats.total_sessions}")
            print(f"     - Completed: {stats.completed_registrations}")
            print(f"     - Incomplete: {stats.incomplete_registrations}")
            print(f"     - Completion Rate: {stats.completion_rate:.1f}%")
            print(f"     - Avg Duration: {stats.average_duration_seconds:.1f} seconds")
            
            if stats.dropoff_by_step:
                print(f"     - Dropoffs by step:")
                for step, count in stats.dropoff_by_step.items():
                    if count > 0:
                        print(f"       • {step}: {count}")
    except grpc.RpcError as e:
        print(f"   ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Test 6: Error Cases
    print("\n6. Testing Error Cases...")
    
    # Invalid session ID
    print("   a. Invalid session ID...")
    try:
        response = stub.TrackStep(analytics_pb2.TrackStepRequest(
            session_id="invalid-uuid",
            step_code=1
        ))
        if response.errors:
            print(f"      ✓ Correctly caught error: {response.errors[0].message}")
        else:
            print(f"      ✗ Should have failed with invalid UUID")
    except grpc.RpcError as e:
        print(f"      ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Invalid step code
    print("   b. Invalid step code...")
    try:
        response = stub.TrackStep(analytics_pb2.TrackStepRequest(
            session_id=str(uuid.uuid4()),
            step_code=99  # Invalid
        ))
        if response.errors:
            print(f"      ✓ Correctly caught error: {response.errors[0].message}")
        else:
            print(f"      ✗ Should have failed with invalid step code")
    except grpc.RpcError as e:
        print(f"      ✗ gRPC Error: {e.code()} - {e.details()}")
    
    # Non-existent interaction
    print("   c. Complete non-existent interaction...")
    try:
        response = stub.CompleteStep(analytics_pb2.CompleteStepRequest(
            interaction_id=str(uuid.uuid4())
        ))
        if response.errors:
            print(f"      ✓ Correctly caught error: {response.errors[0].message}")
        else:
            print(f"      ✗ Should have failed with not found")
    except grpc.RpcError as e:
        print(f"      ✗ gRPC Error: {e.code()} - {e.details()}")
    
    print("\n" + "=" * 60)
    print("ANALYTICS SERVICE TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_analytics_service()