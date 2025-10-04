import { mapCauseOptionToEnumValue } from "./mapCauseOptionToEnumValue";

export class EntityRegistrationDtoFactory {
  static createOrganizationRegistrationDto(
    entityType,
    userId,
    size,
    causes,
    profileForm,
  ) {
    // ✅ SIMPLIFIED: Both business and beneficiary use 'name'
    const name = profileForm.name;
    
    return {
      user: {
        id: userId,
        email: profileForm.email,  // ✅ Also add user email
      },
      registration: {
        entityType: entityType,
        profile: {
          name: name,
          email: profileForm.email,
          phone: profileForm.phoneNumber,
          location: {
            city: profileForm.locationCity,
            state: profileForm.locationState,
          },
          website: profileForm.website,
          size: size,
          shopUrl: profileForm.shopUrl,
          socialMediaUrls: [profileForm.socialMedia],
          teamMemberEmails: [profileForm.teamMemberEmail],
        },
        causes: causes.map((cause) => mapCauseOptionToEnumValue(cause)),
      },
    };
  }
}