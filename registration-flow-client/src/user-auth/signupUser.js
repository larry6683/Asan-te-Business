import { AsanteUsersUserPool } from "./asanteUsersUserPool";

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
      (err, data) => {
        if (err) {
          if (errorCallback) errorCallback(err);
        } else {
          if (successCallback) successCallback();
        }
      },
    );
  } catch (e) {
    if (errorCallback) errorCallback("signup error", e);
  }

  return success;
};
