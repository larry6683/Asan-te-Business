import { UserServiceClient } from '../proto/user/user_grpc_web_pb';
import { BusinessServiceClient } from '../proto/business/business_grpc_web_pb';
import { BeneficiaryServiceClient } from '../proto/beneficiary/beneficiary_grpc_web_pb';
import { AnalyticsServiceClient } from '../proto/analytics/analytics_grpc_web_pb';
import { grpcEndpoint } from './apiUrls';

class GrpcService {
  constructor() {
    this.userClient = new UserServiceClient(grpcEndpoint, null, null);
    this.businessClient = new BusinessServiceClient(grpcEndpoint, null, null);
    this.beneficiaryClient = new BeneficiaryServiceClient(grpcEndpoint, null, null);
    this.analyticsClient = new AnalyticsServiceClient(grpcEndpoint, null, null);
  }

  getMetadata(token) {
    const metadata = {};
    if (token) {
      metadata['authorization'] = `Bearer ${token}`;
    }
    return metadata;
  }

  // ============================================
  // USER SERVICE METHODS
  // ============================================

  getUserByEmail(email, token) {
    const { GetUserRequest } = require('../proto/user/user_pb');
    const request = new GetUserRequest();
    request.setEmail(email);

    return new Promise((resolve, reject) => {
      this.userClient.getUser(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  createUser(email, userType, mailingListSignup, token) {
    const { CreateUserRequest } = require('../proto/user/user_pb');
    const request = new CreateUserRequest();
    request.setEmail(email);
    request.setUserType(userType);
    request.setMailingListSignup(mailingListSignup);

    return new Promise((resolve, reject) => {
      this.userClient.createUser(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  // ============================================
  // BUSINESS SERVICE METHODS
  // ============================================
// ============================================
  // BUSINESS SERVICE METHODS
  // ============================================

  getBusiness(businessId, token) {
    const { GetBusinessRequest } = require('../proto/business/business_pb');
    const request = new GetBusinessRequest();
    request.setBusinessId(businessId);

    return new Promise((resolve, reject) => {
      this.businessClient.getBusiness(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getBusinessByUserEmail(userEmail, token) {
    const { GetBusinessByUserEmailRequest } = require('../proto/business/business_pb');
    const request = new GetBusinessByUserEmailRequest();
    request.setUserEmail(userEmail);

    return new Promise((resolve, reject) => {
      this.businessClient.getBusinessByUserEmail(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  createBusiness(businessData, token) {
    const { CreateBusinessRequest } = require('../proto/business/business_pb');
    const request = new CreateBusinessRequest();
    
    request.setBusinessName(businessData.businessName || '');
    request.setEmail(businessData.email || '');
    request.setWebsiteUrl(businessData.website || '');
    request.setPhoneNumber(businessData.phoneNumber || '');
    request.setLocationCity(businessData.locationCity || '');
    request.setLocationState(businessData.locationState || '');
    request.setEin(businessData.ein || '');
    request.setBusinessDescription(businessData.businessDescription || '');
    request.setBusinessSize(businessData.businessSize || '');
    request.setUserEmail(businessData.userEmail || '');
    
    // Set cause codes if provided
    if (businessData.causePreferences) {
      const allCauses = [
        ...(businessData.causePreferences.primary || []),
        ...(businessData.causePreferences.supporting || []),
        ...(businessData.causePreferences.unranked || [])
      ];
      request.setCauseCodesList(allCauses);
    }

    return new Promise((resolve, reject) => {
      this.businessClient.createBusiness(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }
  // ============================================
  // BENEFICIARY SERVICE METHODS
  // ============================================

  getBeneficiary(beneficiaryId, token) {
    const { GetBeneficiaryRequest } = require('../proto/beneficiary/beneficiary_pb');
    const request = new GetBeneficiaryRequest();
    request.setBeneficiaryId(beneficiaryId);

    return new Promise((resolve, reject) => {
      this.beneficiaryClient.getBeneficiary(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getBeneficiaryByUserEmail(userEmail, token) {
    const { GetBeneficiaryByUserEmailRequest } = require('../proto/beneficiary/beneficiary_pb');
    const request = new GetBeneficiaryByUserEmailRequest();
    request.setUserEmail(userEmail);

    return new Promise((resolve, reject) => {
      this.beneficiaryClient.getBeneficiaryByUserEmail(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  createBeneficiary(beneficiaryData, token) {
    const { CreateBeneficiaryRequest } = require('../proto/beneficiary/beneficiary_pb');
    const request = new CreateBeneficiaryRequest();
    
    request.setBeneficiaryName(beneficiaryData.beneficiaryName || '');
    request.setEmail(beneficiaryData.email || '');
    request.setWebsiteUrl(beneficiaryData.website || '');
    request.setPhoneNumber(beneficiaryData.phoneNumber || '');
    request.setLocationCity(beneficiaryData.locationCity || '');
    request.setLocationState(beneficiaryData.locationState || '');
    request.setEin(beneficiaryData.ein || '');
    request.setBeneficiaryDescription(beneficiaryData.beneficiaryDescription || '');
    request.setBeneficiarySize(beneficiaryData.beneficiarySize || '');
    request.setUserEmail(beneficiaryData.userEmail || '');
    
    // Set cause codes if provided
    if (beneficiaryData.causePreferences) {
      const allCauses = [
        ...(beneficiaryData.causePreferences.primary || []),
        ...(beneficiaryData.causePreferences.supporting || []),
        ...(beneficiaryData.causePreferences.unranked || [])
      ];
      request.setCauseCodesList(allCauses);
    }

    return new Promise((resolve, reject) => {
      this.beneficiaryClient.createBeneficiary(request, this.getMetadata(token), (err, response) => {
        if (err) {
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  // ============================================
  // ANALYTICS SERVICE METHODS
  // ============================================

  getAllSessions(token) {
    const { GetAllSessionsRequest } = require('../proto/analytics/analytics_pb');
    const request = new GetAllSessionsRequest();

    return new Promise((resolve, reject) => {
      this.analyticsClient.getAllSessions(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics getAllSessions error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics getAllSessions errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            // Assuming the response has a list of sessions
            // Adjust .getSessionsList() if your proto definition is different
            resolve(response.getSessionsList());
          }
        }
      });
    });
  }
  
  trackStep(sessionId, appUserId, stepCode, previousStepCode = 0, nextStepCode = 0, token) {
    const { TrackStepRequest } = require('../proto/analytics/analytics_pb');
    const request = new TrackStepRequest();
    
    request.setSessionId(sessionId);
    if (appUserId) {
      request.setAppUserId(appUserId);
    }
    request.setStepCode(stepCode);
    if (previousStepCode > 0) {
      request.setPreviousStepCode(previousStepCode);
    }
    if (nextStepCode > 0) {
      request.setNextStepCode(nextStepCode);
    }

    return new Promise((resolve, reject) => {
      this.analyticsClient.trackStep(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics trackStep error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics trackStep errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  completeStep(interactionId, nextStepCode = 0, token) {
    const { CompleteStepRequest } = require('../proto/analytics/analytics_pb');
    const request = new CompleteStepRequest();
    
    request.setInteractionId(interactionId);
    if (nextStepCode > 0) {
      request.setNextStepCode(nextStepCode);
    }

    return new Promise((resolve, reject) => {
      this.analyticsClient.completeStep(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics completeStep error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics completeStep errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getRegistrationSteps(token) {
    const { GetRegistrationStepsRequest } = require('../proto/analytics/analytics_pb');
    const request = new GetRegistrationStepsRequest();

    return new Promise((resolve, reject) => {
      this.analyticsClient.getRegistrationSteps(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics getRegistrationSteps error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics getRegistrationSteps errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getUserJourney(appUserId, token) {
    const { GetUserJourneyRequest } = require('../proto/analytics/analytics_pb');
    const request = new GetUserJourneyRequest();
    request.setAppUserId(appUserId);

    return new Promise((resolve, reject) => {
      this.analyticsClient.getUserJourney(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics getUserJourney error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics getUserJourney errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getSessionJourney(sessionId, token) {
    const { GetSessionJourneyRequest } = require('../proto/analytics/analytics_pb');
    const request = new GetSessionJourneyRequest();
    request.setSessionId(sessionId);

    return new Promise((resolve, reject) => {
      this.analyticsClient.getSessionJourney(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics getSessionJourney error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics getSessionJourney errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }

  getRegistrationStats(startDate, endDate, token) {
    const { GetRegistrationStatsRequest } = require('../proto/analytics/analytics_pb');
    const request = new GetRegistrationStatsRequest();
    
    if (startDate) {
      request.setStartDate(startDate);
    }
    if (endDate) {
      request.setEndDate(endDate);
    }

    return new Promise((resolve, reject) => {
      this.analyticsClient.getRegistrationStats(request, this.getMetadata(token), (err, response) => {
        if (err) {
          console.error('Analytics getRegistrationStats error:', err);
          reject(err);
        } else {
          const errors = response.getErrorsList();
          if (errors && errors.length > 0) {
            console.error('Analytics getRegistrationStats errors:', errors);
            reject(new Error(errors.map(e => e.getMessage()).join(', ')));
          } else {
            resolve(response);
          }
        }
      });
    });
  }
}

// Create and export singleton instance
const grpcServiceInstance = new GrpcService();
export { grpcServiceInstance as grpcService };