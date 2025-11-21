import { mapCauseOptionToEnumValue } from "./mapCauseOptionToEnumValue";

export class EntityRegistrationDtoFactory {
  static createOrganizationRegistrationDto(
    entityType,
    user, // 👈 CHANGED: Now accepts the full user object (id & email)
    size,
    causes,
    profileForm,
  ) {
    // Handle different field names between forms (CombinedForm uses 'name', BusinessForm uses 'businessName')
    const entityName = profileForm.name || profileForm.businessName || "";
    console.log("🏭 Factory received User:", user);
    return {
      user: {
        id: user.id,
        email: user.email,  // ✅ FIXED: Uses the logged-in User's email for linking
      },
      registration: {
        entityType: entityType,
        profile: {
          name: entityName,
          email: profileForm.email, // 👈 This stays as the Business Contact Email
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
        causes: causes,
      },
    };
  }
}