import { UserServiceClient } from '../proto/user/user_grpc_web_pb';
import { BusinessServiceClient } from '../proto/business/business_grpc_web_pb';
import { BeneficiaryServiceClient } from '../proto/beneficiary/beneficiary_grpc_web_pb';
import { grpcEndpoint } from './apiUrls';

class GrpcService {
  constructor() {
    this.userClient = new UserServiceClient(grpcEndpoint, null, null);
    this.businessClient = new BusinessServiceClient(grpcEndpoint, null, null);
    this.beneficiaryClient = new BeneficiaryServiceClient(grpcEndpoint, null, null);
  }

  getMetadata(token) {
    const metadata = {};
    if (token) {
      metadata['authorization'] = `Bearer ${token}`;
    }
    return metadata;
  }

  // User Service Methods
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

  // Business Service Methods
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

  // Beneficiary Service Methods
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
}

// Create and export singleton instance
const grpcServiceInstance = new GrpcService();
export { grpcServiceInstance as grpcService };
