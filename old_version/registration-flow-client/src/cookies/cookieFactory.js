import { getAccessJwtFromStorage } from "../user-auth/authenticateUser"
import { AppCookieService } from "./appCookieService";

export class CookieFactory {
    static createAppCookieFromDataOrStorage(userData=null, entityData=null) {
        const accessJwt = getAccessJwtFromStorage();
        let user = {}
        if (!userData) {
            user = sessionStorage.getItem("asante:user");
        } else {
            user = {
                id: userData.id,
                email: userData.email,
                userType: userData.userType
            }
        }
        // must update for beneficiaries when implemented
        let entityType = "";
        let entityId = "";

        if (!entityData) {
            // assume business for now.
            entityType = "business"; // not sure if this is in storage or not.
            entityId = sessionStorage.getItem("asante:businessId");
        } else {
            entityId = entityData.entityId
        }
        const appCookie = AppCookieService.createAppCookie(
            entityType, entityId, user.id, user.email, accessJwt
        )

        return appCookie;
    }
}