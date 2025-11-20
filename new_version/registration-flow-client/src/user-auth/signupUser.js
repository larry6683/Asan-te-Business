import { AsanteUsersUserPool } from "./asanteUsersUserPool";
import { UserApiService } from "../api/userApiService";
import { USER_TYPE } from "../types/userType";

// Initialize the user API service
const userApiService = new UserApiService();

export const signupUser = (
  userType,
  email,
  password,
  mailingListSignup,
  successCallback,
  errorCallback,
) => {
  const pool = AsanteUsersUserPool;
  let success = false;
  
  try {
    pool.signUp(
      email,
      password,
      [
        {
          Name: "email",
          Value: email,
        },
        {
          Name: "custom:mailing_list_signup",
          Value: mailingListSignup,
        },
        {
          Name: "custom:user_type",
          Value: userType,
        },
      ],
      null,
      async (err, data) => {
        if (err) {
          if (errorCallback) errorCallback(err);
        } else {
          console.log('✅ Cognito sign-up successful, creating user in database...');
          
          // MAP USER TYPE FOR API
          let apiUserType = "CONSUMER";
          if (userType === USER_TYPE.BUSINESS_ADMIN) {
            apiUserType = "BUSINESS";
          } else if (userType === USER_TYPE.BENEFICIARY_ADMIN) {
            apiUserType = "BENEFICIARY";
          }
          
          // Convert mailingListSignup string to boolean
          const isMailingList = mailingListSignup === "true";

          try {
            // UPDATED: Passing apiUserType and isMailingList
            await userApiService.createUser(
              email,
              apiUserType,
              isMailingList,
              (response) => {
                console.log('✅ User created in database:', response);
                if (successCallback) successCallback();
              },
              (dbError) => {
                console.error('⚠️ User created in Cognito but failed to save to database:', dbError);
                if (successCallback) successCallback();
              }
            );
          } catch (dbError) {
            console.error('⚠️ Database error during user creation:', dbError);
            if (successCallback) successCallback();
          }
        }
      },
    );
  } catch (e) {
    if (errorCallback) errorCallback("signup error", e);
  }
  
  return success;
};