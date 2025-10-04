import { apiUrls } from "./apiUrls";
import { getAccessJwtFromStorage } from "../user-auth/authenticateUser";

const baseUrl = apiUrls.dev;

export class UserApiService {
  constructor() {}
  async createUser(email, onSuccess, onFailure) {
    const request = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        authorization: `Bearer ${getAccessJwtFromStorage()}`,
      },
      body: JSON.stringify({
        email: email,
      }),
    };
    const url = `${baseUrl}/user`;
    // console.log(`outgoing request. url: ${url}`, request);
    try {
      const response = request ? await fetch(url, request) : await fetch(url);
      if (!response.ok) {
        const text = await response.text();
        throw Error(text);
      }

      const jsonResponse = await response.json();
      if (onSuccess) onSuccess(jsonResponse);
      else return jsonResponse
    } catch (error) {
      if (onFailure) onFailure(error);
      else throw error;
    }
  }

  async getUserByEmail(email, onSuccess, onFailure) {
    const params = new URLSearchParams({ email: email });
    const url = `${baseUrl}/userEmail?${params.toString()}`;
    const request = {
      method: "GET",
      headers: {
        authorization: `Bearer ${getAccessJwtFromStorage()}`,
      },
    };
    try {
      const response = await fetch(url, request);
      if (!response.ok) {
        const text = await response.text();
        throw Error(text);
      }

      const jsonResponse = await response.json();
      if (onSuccess) onSuccess(jsonResponse)
      else return jsonResponse
    } catch (error) {
      if (onFailure) onFailure(error);
      else throw error;
    }
  }
    
}
