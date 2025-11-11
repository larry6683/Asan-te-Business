#!/usr/bin/env python3
"""
Test script for Analytics Service
Tests registration step tracking and metrics
"""
import grpc
import sys
import uuid
from datetime import datetime, timedelta

sys.path.insert(0, 'src')

from codegen.analytics.analytics_pb2 import (
    TrackInteractionRequest, CompleteStepRequest,
    GetUserProgressRequest, GetRegistrationMetricsRequest,
    RegistrationStepCode
)
from codegen.analytics.analytics_pb2_grpc import AnalyticsServiceStub
from codegen.user.user_pb2 import CreateUserRequest
from codegen.user.user_pb2_grpc import UserServiceStub
from codegen.business.business_pb2 import CreateBusinessRequest
from codegen.business.business_pb2_grpc import BusinessServiceStub


def test_analytics_service():
    """Test the analytics service with a simulated registration flow"""
    print("\n" + "=" * 60)
    print("ANALYTICS SERVICE TEST")
    print("=" * 60)
    
    # Create channels
    analytics_channel = grpc.insecure_channel('localhost:50054')
    user_channel = grpc.insecure_channel('localhost:50051')
    business_channel = grpc.insecure_channel('localhost:50052')
    
    analytics_stub = AnalyticsServiceStub(analytics_channel)
    user_stub = UserServiceStub(user_channel)
    business_stub = BusinessServiceStub(business_channel)
    
    # Generate session ID (simulating frontend)
    session_id = str(uuid.uuid4())
    print(f"\n📱 Session ID: {session_id}")
    
    try:
        # Test 1: Track signup step (anonymous user)
        print("\n1️⃣ TRACKING SIGNUP STEP (Anonymous)")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_SIGNUP
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print(f"✅ Tracked signup step")
            print(f"   Interaction ID: {track_response.interaction_id}")
            signup_interaction_id = track_response.interaction_id
        else:
            print(f"❌ Failed to track signup: {track_response.errors}")
            return
        
        # Test 2: Create user (with session tracking)
        print("\n2️⃣ CREATING USER")
        print("-" * 40)
        
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        metadata = [('session-id', session_id)]
        
        user_request = CreateUserRequest(
            email=email,
            user_type='BUSINESS',
            mailing_list_signup=True
        )
        
        user_response = user_stub.CreateUser(user_request, metadata=metadata)
        
        if not user_response.errors:
            print(f"✅ Created user: {user_response.user.email}")
            print(f"   User ID: {user_response.user.id}")
            user_id = user_response.user.id
        else:
            print(f"❌ Failed to create user: {user_response.errors}")
            return
        
        # Test 3: Complete signup step
        print("\n3️⃣ COMPLETING SIGNUP STEP")
        print("-" * 40)
        
        complete_request = CompleteStepRequest(
            interaction_id=signup_interaction_id
        )
        
        complete_response = analytics_stub.CompleteStep(complete_request)
        
        if complete_response.success:
            print("✅ Completed signup step")
        else:
            print(f"❌ Failed to complete step: {complete_response.errors}")
        
        # Test 4: Track verification step
        print("\n4️⃣ TRACKING VERIFICATION STEP")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            app_user_id=user_id,
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_VERIFICATION,
            previous_step_id=signup_interaction_id
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print("✅ Tracked verification step")
            verification_interaction_id = track_response.interaction_id
            
            # Immediately complete it (simulating email verification)
            complete_response = analytics_stub.CompleteStep(
                CompleteStepRequest(interaction_id=verification_interaction_id)
            )
            if complete_response.success:
                print("✅ Completed verification step")
        
        # Test 5: Track first login
        print("\n5️⃣ TRACKING FIRST LOGIN")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            app_user_id=user_id,
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_FIRST_LOGIN,
            previous_step_id=verification_interaction_id
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print("✅ Tracked first login")
            login_interaction_id = track_response.interaction_id
            analytics_stub.CompleteStep(
                CompleteStepRequest(interaction_id=login_interaction_id)
            )
        
        # Test 6: Track cause selection
        print("\n6️⃣ TRACKING CAUSE SELECTION")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            app_user_id=user_id,
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_CAUSE_SELECTION
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print("✅ Tracked cause selection")
            cause_interaction_id = track_response.interaction_id
            analytics_stub.CompleteStep(
                CompleteStepRequest(interaction_id=cause_interaction_id)
            )
        
        # Test 7: Track size selection
        print("\n7️⃣ TRACKING SIZE SELECTION")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            app_user_id=user_id,
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_SIZE
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print("✅ Tracked size selection")
            size_interaction_id = track_response.interaction_id
            analytics_stub.CompleteStep(
                CompleteStepRequest(interaction_id=size_interaction_id)
            )
        
        # Test 8: Track entity information (and create business)
        print("\n8️⃣ TRACKING ENTITY INFORMATION")
        print("-" * 40)
        
        track_request = TrackInteractionRequest(
            app_user_id=user_id,
            session_id=session_id,
            step_code=RegistrationStepCode.STEP_ENTITY_INFORMATION
        )
        
        track_response = analytics_stub.TrackInteraction(track_request)
        
        if track_response.success:
            print("✅ Tracked entity information")
            entity_interaction_id = track_response.interaction_id
            
            # Create business (this completes registration)
            business_request = CreateBusinessRequest(
                business_name=f"Test Business {uuid.uuid4().hex[:8]}",
                email=f"biz_{uuid.uuid4().hex[:8]}@example.com",
                location_city="Denver",
                location_state="CO",
                business_size="MEDIUM",
                user_email=email,
                cause_codes=["EDUCATION", "CLIMATE_ADVOCACY"]
            )
            
            business_response = business_stub.CreateBusiness(
                business_request, 
                metadata=metadata
            )
            
            if not business_response.errors:
                print(f"✅ Created business: {business_response.business.business_name}")
                
                # Complete entity information step
                analytics_stub.CompleteStep(
                    CompleteStepRequest(interaction_id=entity_interaction_id)
                )
                print("✅ Completed registration!")
        
        # Test 9: Get user progress
        print("\n9️⃣ GETTING USER PROGRESS")
        print("-" * 40)
        
        progress_request = GetUserProgressRequest(
            app_user_id=user_id,
            session_id=session_id
        )
        
        progress_response = analytics_stub.GetUserProgress(progress_request)
        
        if not progress_response.errors:
            print(f"📊 Registration Progress:")
            print(f"   Current Step: {progress_response.current_step}")
            print(f"   Completion: {progress_response.completion_percentage:.1f}%")
            print(f"   Steps Completed:")
            
            for step in progress_response.steps:
                status = "✅" if step.completed else "⏳"
                print(f"     {status} {step.step_name}")
                if step.began_at:
                    print(f"        Started: {step.began_at[:19]}")
                if step.completed_at:
                    print(f"        Completed: {step.completed_at[:19]}")
        
        # Test 10: Get registration metrics
        print("\n🔟 GETTING REGISTRATION METRICS")
        print("-" * 40)
        
        # Get metrics for last 30 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        metrics_request = GetRegistrationMetricsRequest(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )
        
        metrics_response = analytics_stub.GetRegistrationMetrics(metrics_request)
        
        if not metrics_response.errors:
            metrics = metrics_response.metrics
            print(f"📈 Registration Metrics (Last 30 Days):")
            print(f"   Total Sessions: {metrics.total_sessions}")
            print(f"   Completed Registrations: {metrics.completed_registrations}")
            print(f"   Abandoned Registrations: {metrics.abandoned_registrations}")
            print(f"   Completion Rate: {metrics.completion_rate:.1f}%")
            print(f"   Avg Time to Complete: {metrics.avg_time_to_complete_minutes:.1f} minutes")
            
            if metrics.dropout_by_step:
                print(f"   Dropouts by Step:")
                for step_name, count in metrics.dropout_by_step.items():
                    if count > 0:
                        print(f"     - {step_name}: {count}")
        
        print("\n" + "=" * 60)
        print("✅ ALL ANALYTICS TESTS PASSED!")
        print("=" * 60)
        
    except grpc.RpcError as e:
        print(f"\n❌ gRPC Error: {e.code()}: {e.details()}")
        print("\nMake sure all services are running:")
        print("  - User Service (port 50051)")
        print("  - Business Service (port 50052)")
        print("  - Analytics Service (port 50054)")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analytics_channel.close()
        user_channel.close()
        business_channel.close()


if __name__ == '__main__':
    test_analytics_service()