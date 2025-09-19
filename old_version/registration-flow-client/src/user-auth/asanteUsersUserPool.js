import { CognitoUserPool } from "amazon-cognito-identity-js";

const AsanteUsersUserPoolData = {
  // UserPoolId: "us-east-1_5kRstX61t",
  // ClientId: "6milt3r5u07dahqsk2o65u4rrf",
  UserPoolId: "us-east-2_qsfonb9jL",
  ClientId: "5h29pn5bd520u4ik68induirnc",
};
export const AsanteUsersUserPool = new CognitoUserPool(AsanteUsersUserPoolData);
