import { grpcEndpoint } from './apiUrls';

class AnalyticsService {
  constructor() {
    this.endpoint = grpcEndpoint;
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

  async trackStep(stepCode, previousStepCode = 0, nextStepCode = 0) {
    const userId = this.getUserId();
    
    try {
      const response = await fetch(`${this.endpoint}/analytics.AnalyticsService/TrackStep`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: this.sessionId,
          app_user_id: userId || '',
          step_code: stepCode,
          previous_step_code: previousStepCode,
          next_step_code: nextStepCode
        })
      });

      if (!response.ok) {
        console.error('Analytics tracking failed:', response.status);
        return null;
      }

      const data = await response.json();
      
      // Store interaction ID for completing later
      if (data.interaction && data.interaction.id) {
        sessionStorage.setItem(`asante:interactionId_${stepCode}`, data.interaction.id);
      }
      
      return data;
    } catch (error) {
      console.error('Analytics tracking error:', error);
      return null;
    }
  }

  async completeStep(stepCode, nextStepCode = 0) {
    const interactionId = sessionStorage.getItem(`asante:interactionId_${stepCode}`);
    
    if (!interactionId) {
      console.warn('No interaction ID found for step:', stepCode);
      return null;
    }

    try {
      const response = await fetch(`${this.endpoint}/analytics.AnalyticsService/CompleteStep`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          interaction_id: interactionId,
          next_step_code: nextStepCode
        })
      });

      if (!response.ok) {
        console.error('Analytics completion failed:', response.status);
        return null;
      }

      return await response.json();
    } catch (error) {
      console.error('Analytics completion error:', error);
      return null;
    }
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
}

const analyticsServiceInstance = new AnalyticsService();
export { analyticsServiceInstance as analyticsService };