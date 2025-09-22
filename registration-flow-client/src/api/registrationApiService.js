import { apiUrls } from "./apiUrls";
import { getAccessJwtFromStorage } from "../user-auth/authenticateUser";
const baseUrl = apiUrls.dev;

export class RegistrationApiService {
  constructor() {}
  // not a fan of passing success/error responsees but ok
  async registerBusiness(business, onSuccess, onError) {
    let url = `${baseUrl}/register/entity`;
    let request = this.createRequest(business);
    await this.processRequest(url, request, onSuccess, onError);
  }

  async registerBeneficiary(beneficiary) {
    const url = `${baseUrl}/register/entity`;
    let request = this.createRequest(beneficiary);
    await this.processRequest(url, request);
  }

  createRequest(requestBody) {
    return {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        authorization: `Bearer ${getAccessJwtFromStorage()}`,
      },
      body: JSON.stringify(requestBody),
    };
  }

  async processRequest(url, request, onSuccess, onError) {
    // console.log(`outgoing registration request. url: ${url}`, request);
    try {
      const response = await fetch(url, request);
      if (!response.ok) {
        const text = await response.text();
        throw Error(text);
      }

      const jsonResponse = await response.json();
      if (onSuccess) onSuccess(jsonResponse);
      else return jsonResponse
    } catch (error) {
      if (onError) onError(error);
      else throw error;
    }
  }
}
