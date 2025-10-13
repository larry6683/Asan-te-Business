class OrganizationRegistrationDto {
  constructor(
    entity_type,
    registeringUserId,
    registeringUserEmail,
    causePreferences,
    size,
    name,
    email,
    website,
    phone,
    locationCity,
    locationState,
    socialMedia,
    ein,
    teamMemberEmails,
  ) {
    this.registeringUser = {
      id: registeringUserId,
      email: registeringUserEmail,
    };
    this.entityType = entity_type;
    this.causePreferences = causePreferences;
    this.profile = {
      size: size,
      name: name,
      email: email,
      website: website,
      phone: phone,
      location: {
        city: locationCity,
        state: locationState,
      },
      socialMedia: socialMedia,
      ein: ein,
    };
    this.teamMemberEmails = teamMemberEmails;
  }
}
