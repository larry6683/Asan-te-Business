import { CognitoUserPool } from "amazon-cognito-identity-js";

const AsanteUsersUserPoolData = {
  UserPoolId: "us-east-2_bOWZURPch",  // ← Replace with your User Pool ID
  ClientId: "64gg6rq89hd0j5valu3eu91jdf",        // ← Replace with your App Client ID
};

export const AsanteUsersUserPool = new CognitoUserPool(AsanteUsersUserPoolData);