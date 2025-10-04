import { grpcService } from "./grpcService";
import { getAccessJwtFromStorage } from "../user-auth/authenticateUser";

export class UserApiService {
  constructor() {
    this.grpcService = grpcService;
  }

  async createUser(email, onSuccess, onFailure) {
    try {
      const token = getAccessJwtFromStorage();
      
      // Default values for user creation
      const userType = "BUSINESS";
      const mailingListSignup = false;
      
      const response = await this.grpcService.createUser(email, userType, mailingListSignup, token);
      
      // Convert gRPC response to expected JSON format
      const user = response.getUser();
      const jsonResponse = {
        data: {
          id: user.getId(),
          type: 'user',
          attributes: {
            email: user.getEmail(),
            userType: user.getUserType(),
            mailingListSignup: user.getMailingListSignup()
          }
        }
      };

      if (onSuccess) {
        onSuccess(jsonResponse);
      }
      return jsonResponse;

    } catch (error) {
      console.error('Failed to create user:', error);
      if (onFailure) {
        onFailure(error);
      } else {
        throw error;
      }
    }
  }

  async getUserByEmail(email, onSuccess, onFailure) {
    try {
      const token = getAccessJwtFromStorage();
      
      const response = await this.grpcService.getUserByEmail(email, token);
      
      // Convert gRPC response to expected JSON format
      const user = response.getUser();
      const jsonResponse = {
        data: {
          id: user.getId(),
          type: 'user',
          attributes: {
            email: user.getEmail(),
            userType: user.getUserType(),
            mailingListSignup: user.getMailingListSignup()
          },
          // ✅ NEW: Add relationships field
          relationships: {}
        }
      };

      // ✅ NEW: Check for business/beneficiary relationships
      try {
        // First check session storage (current session)
        let businessId = sessionStorage.getItem("asante:businessId");
        let beneficiaryId = sessionStorage.getItem("asante:beneficiaryId");
        
        // If not in session, try to get from cookies (persists across sessions)
        if (!businessId && !beneficiaryId) {
          const cookies = document.cookie.split(';');
          for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'asanteApp') {  // ✅ Fixed: correct cookie name
              try {
                const cookieData = JSON.parse(decodeURIComponent(value));
                console.log('🔍 Cookie data:', cookieData);
                
                // ✅ Fixed: check cookieData.app.entityType (nested structure)
                if (cookieData.app && cookieData.app.entityType === 'business' && cookieData.app.entityId) {
                  businessId = cookieData.app.entityId;
                  // Restore to session storage for this session
                  sessionStorage.setItem("asante:businessId", businessId);
                  console.log('✅ Restored business ID from cookie:', businessId);
                } else if (cookieData.app && cookieData.app.entityType === 'beneficiary' && cookieData.app.entityId) {
                  beneficiaryId = cookieData.app.entityId;
                  // Restore to session storage for this session
                  sessionStorage.setItem("asante:beneficiaryId", beneficiaryId);
                  console.log('✅ Restored beneficiary ID from cookie:', beneficiaryId);
                }
              } catch (e) {
                console.log('⚠️ Could not parse cookie data:', e);
              }
              break;
            }
          }
        }
        
        // Add relationships if found
        if (businessId) {
          jsonResponse.data.relationships.businesses = {
            data: [{ id: businessId, type: 'business' }]
          };
          console.log('✅ Found business relationship:', businessId);
        }
        
        if (beneficiaryId) {
          jsonResponse.data.relationships.beneficiaries = {
            data: [{ id: beneficiaryId, type: 'beneficiary' }]
          };
          console.log('✅ Found beneficiary relationship:', beneficiaryId);
        }
      } catch (err) {
        console.log('⚠️ Error checking relationships:', err);
      }

      // ✅ If no relationships found, remove the empty object
      if (Object.keys(jsonResponse.data.relationships).length === 0) {
        delete jsonResponse.data.relationships;
        console.log('ℹ️ No relationships found for user');
      }

      if (onSuccess) {
        onSuccess(jsonResponse);
      }
      return jsonResponse;

    } catch (error) {
      console.error('Failed to get user by email:', error);
      if (onFailure) {
        onFailure(error);
      } else {
        throw error;
      }
    }
  }
}