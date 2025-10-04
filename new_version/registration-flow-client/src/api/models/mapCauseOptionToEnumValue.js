/* 
    the lambda function should be able to handle mixed case values.
    Howver in the API all caps will eliminate any issues
*/
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
    // social causes
    case "Sports":
      return "SPORTS";
    case "Arts":
      return "ARTS";
    case "Education":
      return "EDUCATION";
    case "Social Justice":
      return "SOCIAL_JUSTICE";
    case "Mental Health & Wellbeing":
      return "MENTAL_HEALTH";
    // Innovation/Entrepreneurship
    case "Youth Empowerment":
      return "YOUTH_EMPOWERMENT";
    case "Social Innovation":
      return "SOCIAL_INNOVATION";
    case "Sustainable Innovation":
      return "SUSTAINABLE_INNOVATION";
    case "Social Entrepreneurship":
      return "SOCIAL_ENTREPRENEURSHIP";
    // environment
    case "Droughts & Fire Management":
      return "DROUGHT_FIRE_MANAGEMENT";
    case "Climate Advocacy":
      return "CLIMATE_ADVOCACY";
    case "Climate Refugees":
      return "CLIMATE_REFUGEES";
    case "Water Sustainability":
      return "WATER_SUSTAINABILITY";
    // emergency relief
    case "Emergency Relief":
      return "EMERGENCY_RELIEF";
    default:
      return "UNSPECIFIED";
  }
};
