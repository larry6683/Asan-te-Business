import { grpcService } from "./grpcService";
import { getAccessJwtFromStorage } from "../user-auth/authenticateUser";

export class RegistrationApiService {
  constructor() {
    this.grpcService = grpcService;
  }

  /**
   * Register a business entity
   */
  async registerBusiness(businessRegistrationDto, onSuccess, onError) {
    try {
      const token = getAccessJwtFromStorage();
      
      // ✅ FIXED: Access data from the deeply nested structure
      const profile = businessRegistrationDto.registration.profile;
      const user = businessRegistrationDto.user;
      
      // Map the DTO to gRPC format
      const businessData = {
        businessName: profile.name,
        email: profile.email,
        website: profile.website || '',
        phoneNumber: profile.phone || '',
        locationCity: profile.location.city,
        locationState: profile.location.state,
        ein: '',  // Not in form yet
        businessDescription: '',  // Not in form yet
        businessSize: profile.size,
        userEmail: user.email
      };

      console.log('📤 Registering business via gRPC:', businessData);

      const response = await this.grpcService.createBusiness(businessData, token);
      
      // Convert gRPC response to format expected by frontend
      const business = response.getBusiness();
      const jsonResponse = {
        data: {
          id: business.getId(),
          type: 'business',
          attributes: {
            businessName: business.getBusinessName(),
            email: business.getEmail(),
            websiteUrl: business.getWebsiteUrl(),
            phoneNumber: business.getPhoneNumber(),
            locationCity: business.getLocationCity(),
            locationState: business.getLocationState(),
            ein: business.getEin(),
            businessDescription: business.getBusinessDescription(),
            businessSize: business.getBusinessSize()
          }
        }
      };

      console.log('✅ Business registered successfully:', jsonResponse);

      if (onSuccess) {
        onSuccess(jsonResponse);
      }
      return jsonResponse;

    } catch (error) {
      console.error('❌ Business registration failed:', error);
      if (onError) {
        onError(error);
      } else {
        throw error;
      }
    }
  }

  /**
   * Register a beneficiary entity
   */
  async registerBeneficiary(beneficiaryRegistrationDto, onSuccess, onError) {
    try {
      const token = getAccessJwtFromStorage();
      
      // ✅ FIXED: Access data from the correct nested structure
      const registration = beneficiaryRegistrationDto.registration;
      const user = beneficiaryRegistrationDto.user;
      
      // Map the DTO to gRPC format
      const beneficiaryData = {
        beneficiaryName: registration.name,           // ✅ Changed from beneficiaryRegistrationDto.entityName
        email: registration.email,                    // ✅ Changed from beneficiaryRegistrationDto.email
        website: registration.website,                // ✅ Changed from beneficiaryRegistrationDto.websiteUrl
        phoneNumber: registration.phoneNumber,        // ✅ Changed from beneficiaryRegistrationDto.phoneNumber
        locationCity: registration.locationCity,      // ✅ Changed from beneficiaryRegistrationDto.locationCity
        locationState: registration.locationState,    // ✅ Changed from beneficiaryRegistrationDto.locationState
        ein: registration.ein || '',
        beneficiaryDescription: registration.description || '',
        beneficiarySize: registration.entitySize,     // ✅ Changed from beneficiaryRegistrationDto.entitySize
        userEmail: user.email                         // ✅ Changed from beneficiaryRegistrationDto.userEmail
      };

      console.log('📤 Registering beneficiary via gRPC:', beneficiaryData);

      const response = await this.grpcService.createBeneficiary(beneficiaryData, token);
      
      // Convert gRPC response to format expected by frontend
      const beneficiary = response.getBeneficiary();
      const jsonResponse = {
        data: {
          id: beneficiary.getId(),
          type: 'beneficiary',
          attributes: {
            beneficiaryName: beneficiary.getBeneficiaryName(),
            email: beneficiary.getEmail(),
            websiteUrl: beneficiary.getWebsiteUrl(),
            phoneNumber: beneficiary.getPhoneNumber(),
            locationCity: beneficiary.getLocationCity(),
            locationState: beneficiary.getLocationState(),
            ein: beneficiary.getEin(),
            beneficiaryDescription: beneficiary.getBeneficiaryDescription(),
            beneficiarySize: beneficiary.getBeneficiarySize()
          }
        }
      };

      console.log('✅ Beneficiary registered successfully:', jsonResponse);

      if (onSuccess) {
        onSuccess(jsonResponse);
      }
      return jsonResponse;

    } catch (error) {
      console.error('❌ Beneficiary registration failed:', error);
      if (onError) {
        onError(error);
      } else {
        throw error;
      }
    }
  }
}