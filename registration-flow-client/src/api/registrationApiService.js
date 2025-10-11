import { grpcService } from "./grpcService";
import { getAccessJwtFromStorage } from "../user-auth/authenticateUser";
import { mapCauseOptionToEnumValue } from "./models/mapCauseOptionToEnumValue"; 

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
      
      const profile = businessRegistrationDto.registration.profile;
      const user = businessRegistrationDto.user;
      const causes = businessRegistrationDto.registration.causes || [];
      
      // 🆕 Map cause names to enum values and group by rank
      const causePreferences = {
        primary: [],
        supporting: [],
        unranked: []
      };
      
      causes.forEach(cause => {
        const enumValue = mapCauseOptionToEnumValue(cause.name); // 🆕 Map to enum
        const rank = cause.rank?.toLowerCase() || 'unranked';
        
        if (causePreferences[rank]) {
          causePreferences[rank].push(enumValue); // 🆕 Push ENUM value, not name
        }
      });
      
      // 🆕 ADD THIS - Test your transformation
      console.log('🔍 TESTING CAUSE TRANSFORMATION:');
      console.log('Input causes from sessionStorage:', causes);
      console.log('Output causePreferences for API:', causePreferences);
      console.log('Flattened for gRPC:', [
        ...causePreferences.primary,
        ...causePreferences.supporting,
        ...causePreferences.unranked
      ]);
      
      // Map the DTO to gRPC format
      const businessData = {
        businessName: profile.name,
        email: profile.email,
        website: profile.website || '',
        phoneNumber: profile.phone || '',
        locationCity: profile.location.city,
        locationState: profile.location.state,
        ein: '',
        businessDescription: '',
        businessSize: profile.size,
        userEmail: user.email,
        causePreferences: causePreferences // 🆕 Send grouped enum values
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
      
      const registration = beneficiaryRegistrationDto.registration;
      const user = beneficiaryRegistrationDto.user;
      const causes = registration.causes || [];
      
      // 🆕 Map cause names to enum values and group by rank
      const causePreferences = {
        primary: [],
        supporting: [],
        unranked: []
      };
      
      causes.forEach(cause => {
        const enumValue = mapCauseOptionToEnumValue(cause.name); // 🆕 Map to enum
        const rank = cause.rank?.toLowerCase() || 'unranked';
        
        if (causePreferences[rank]) {
          causePreferences[rank].push(enumValue); // 🆕 Push ENUM value, not name
        }
      });
      
      const beneficiaryData = {
        beneficiaryName: registration.profile.name,
        email: registration.profile.email,
        website: registration.profile.website,
        phoneNumber: registration.profile.phone,
        locationCity: registration.profile.location.city,
        locationState: registration.profile.location.state,
        ein: registration.profile.ein || '',
        beneficiaryDescription: registration.profile.description || '',
        beneficiarySize: registration.profile.size,
        userEmail: user.email,
        causePreferences: causePreferences // 🆕 Send grouped enum values
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