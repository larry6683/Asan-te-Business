/**
 * Session ID Manager for Analytics Tracking
 * Generates and persists session_id across registration flow
 */
import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'asante_registration_session_id';

/**
 * Get existing session_id or create new one
 * @returns {string} UUID session_id
 */
export const getOrCreateSessionId = () => {
  let sessionId = localStorage.getItem(SESSION_KEY);
  
  if (!sessionId) {
    sessionId = uuidv4();
    localStorage.setItem(SESSION_KEY, sessionId);
    console.log('✅ New registration session created:', sessionId);
  }
  
  return sessionId;
};

/**
 * Clear session_id (call when registration complete)
 */
export const clearSessionId = () => {
  localStorage.removeItem(SESSION_KEY);
  console.log('🗑️ Registration session cleared');
};

/**
 * Get session_id without creating new one
 * @returns {string|null}
 */
export const getSessionId = () => {
  return localStorage.getItem(SESSION_KEY);
};