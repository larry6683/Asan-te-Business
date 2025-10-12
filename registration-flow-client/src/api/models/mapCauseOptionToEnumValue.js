export const mapCauseOptionToEnumValue = (value) => {
  switch (value) {
    // community causes
    case "Homelessness":
      return "HOMELESSNESS";
    case "Events & Advocacy":
      return "EVENTS_ADVOCACY";
    case "First Responders":
      return "FIRST_RESPONDERS";
    case "Disadvantaged Populations":
      return "DISADVANTAGED_POPULATIONS";
    case "Schools & Teachers":
      return "SCHOOLS_TEACHERS";
    case "Animal Welfare":
      return "ANIMAL_WELFARE";
    // social causes
    case "Sports":
      return "SPORTS";
    case "Arts":
      return "ARTS";
    case "Faith Based Orgs":
      return "FAITH_BASED_ORGS";
    case "Education":
      return "EDUCATION";
    case "Social Justice":
      return "SOCIAL_JUSTICE";
    case "Health & Wellbeing":
      return "HEALTH_WELLBEING";
    // Innovation/Entrepreneurship
    case "Youth Empowerment":
      return "YOUTH_EMPOWERMENT";
    case "Innovation":
      return "INNOVATION";
    case "Sustainable Innovation":
      return "SUSTAINABLE_INNOVATION";
    case "Social Entrepreneurship":
      return "SOCIAL_ENTREPRENEURSHIP";
    // environment
    case "Droughts & Fire Management":
      return "DROUGHTS_FIRE_MANAGEMENT";
    case "Climate Advocacy":
      return "CLIMATE_ADVOCACY";
    case "Water Sustainability":
      return "WATER_SUSTAINABILITY";
    case "Food Systems":
      return "FOOD_SYSTEMS";
    case "Wildlife Protection":
      return "WILDLIFE_PROTECTION";
    // emergency relief
    case "Emergency Relief":
      return "EMERGENCY_RELIEF";
    default:
      return "UNSPECIFIED";
  }
};

