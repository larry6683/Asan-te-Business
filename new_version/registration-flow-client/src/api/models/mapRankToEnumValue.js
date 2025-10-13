export const mapRankToEnumValue = (rank) => {
    switch (rank?.toUpperCase()) {
      case "PRIMARY":
        return "RANK_PRIMARY";
      case "SUPPORTING":
        return "RANK_SUPPORTING";
      case "UNRANKED":
        return "RANK_UNRANKED";
      default:
        return "RANK_UNSPECIFIED"; // ← Default case for errors/unknown
    }
  };