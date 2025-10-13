import { AsanteUsersUserPool } from "./asanteUsersUserPool";
import { resendAuthenticationCode } from "../authentication/resendAuthenticationCode";

export const resendUserVerificationCode = (email) => {
  resendAuthenticationCode(email, AsanteUsersUserPool);
};
