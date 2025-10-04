import { AsanteUsersUserPool } from "./asanteUsersUserPool";
import { UserApiService } from "../api/userApiService";

// Initialize the user API service
const userApiService = new UserApiService();

// callbacks are so extra but i was running into some weird async shenanigains
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
          // ✅ NEW: After Cognito sign-up succeeds, create user in database
          console.log('✅ Cognito sign-up successful, creating user in database...');
          
          try {
            await userApiService.createUser(
              email,
              (response) => {
                console.log('✅ User created in database:', response);
                if (successCallback) successCallback();
              },
              (dbError) => {
                console.error('⚠️ User created in Cognito but failed to save to database:', dbError);
                // Still call success since Cognito account was created
                // The user will be created in DB on first sign-in as fallback
                if (successCallback) successCallback();
              }
            );
          } catch (dbError) {
            console.error('⚠️ Database error during user creation:', dbError);
            // Still call success since Cognito account was created
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