import { grpcService } from './grpcService';
import { getAccessJwtFromStorage } from '../user-auth/authenticateUser';

class AnalyticsService {
  constructor() {
    this.grpcService = grpcService;
    this.sessionId = this.getOrCreateSessionId();
  }

  getOrCreateSessionId() {
    let sessionId = sessionStorage.getItem('asante:analyticsSessionId');
    if (!sessionId) {
      sessionId = this.generateUUID();
      sessionStorage.setItem('asante:analyticsSessionId', sessionId);
    }
    return sessionId;
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  getUserId() {
    const userJson = sessionStorage.getItem('asante:user');
    if (userJson) {
      try {
        const user = JSON.parse(userJson);
        return user.id || '';
      } catch (e) {
        return '';
      }
    }
    return '';
  }

  async trackStep(stepCode, previousStepCode = 0, nextStepCode = 0) {
    const userId = this.getUserId();
    const token = getAccessJwtFromStorage();
    
    try {
      const response = await this.grpcService.trackStep(
        this.sessionId,
        userId,
        stepCode,
        previousStepCode,
        nextStepCode,
        token
      );
      
      // Store interaction ID for completing later
      const interaction = response.getInteraction();
      if (interaction && interaction.getId()) {
        sessionStorage.setItem(`asante:interactionId_${stepCode}`, interaction.getId());
      }
      
      return response;
    } catch (error) {
      // Silently fail - don't block user flow
      console.error('Analytics tracking error (non-blocking):', error);
      return null;
    }
  }

  async completeStep(stepCode, nextStepCode = 0) {
    const interactionId = sessionStorage.getItem(`asante:interactionId_${stepCode}`);
    
    if (!interactionId) {
      console.warn('No interaction ID found for step:', stepCode);
      return null;
    }

    const token = getAccessJwtFromStorage();

    try {
      const response = await this.grpcService.completeStep(
        interactionId,
        nextStepCode,
        token
      );
      
      return response;
    } catch (error) {
      // Silently fail - don't block user flow
      console.error('Analytics completion error (non-blocking):', error);
      return null;
    }
  }

  // Helper method to map session to user after login
  mapSessionToUser(userId) {
    // This will be called after successful login/verification
    // The backend will handle the mapping via app_user_id in future trackStep calls
    console.log('Session mapped to user:', userId);
  }
}

const analyticsServiceInstance = new AnalyticsService();
export { analyticsServiceInstance as analyticsService };