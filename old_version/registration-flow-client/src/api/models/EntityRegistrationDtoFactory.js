import { mapCauseOptionToEnumValue } from "./mapCauseOptionToEnumValue";
export class EntityRegistrationDtoFactory {
  static createOrganizationRegistrationDto(
    entityType,
    userId,
    size,
    causes,
    profileForm,
  ) {
    let name;
    // console.log(entityType);
    if (entityType === "business") {
      name = profileForm.businessName;
    } else if (entityType === "beneficiary") {
      name = profileForm.beneficiaryName;
    }
    return {
      user: {
        id: userId,
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
