import { CookieService } from "./cookieService"
import { redirectUrls } from "../web-data/redirectUrls";

export class AppCookieService extends CookieService {
    static appCookieName = "asanteApp"

    constructor() {
        super();
    }

    static saveAppCookie(data) {
        CookieService.setCookie(this.appCookieName, data);
    }

    static getAppCookie() {
        const appCookieData = CookieService.getCookie(this.appCookieName);
        if (appCookieData)
            return JSON.parse(appCookieData)
        else return null;
    }

    static createAppCookie(entityType, entityId, userId, userEmail, accessJwt) {
        const cookieData = {
            app: {
                entityType,
                entityId
            },
            user: {
                userId,
                userEmail
            },
            auth: {
                accessJwt
            }
        }
        this.saveAppCookie(cookieData)
        return this.getAppCookie();
    }

    static updateAppCookie(data) {
        let appCookie = this.getAppCookie();
        if (!appCookie) {
            if (data.entityType && data.entityId && data.userId && data.userEmail && data.accessJwt)
                this.createAppCookie(
                    data.entityType, data.entityId, data.userId, data.userEmail, data.accessJwt
                )
            else 
                window.location.href = `${redirectUrls.registration}/`;
        }
        else {
            if (data.entityType)
                appCookie.app.entityType = data.entityType;
            if (data.entityId)
                appCookie.app.entityId = data.entityId;
            if (data.userId)
                appCookie.user.userId = data.userId;
            if (data.userEmail)
                appCookie.user.userEmail = data.userEmail;
            if (data.accessJwt)
                appCookie.auth.accessJwt = data.accessJwt;
        }
        
        this.saveAppCookie(appCookie)
    }

    static removeAppCookie() {
        CookieService.eraseCookie(this.appCookieName)
    }

    static getAccessJwtFromAppCookie() {
        const cookie = this.getAppCookie();
        if (cookie && cookie.auth){
            return cookie.auth.accessJwt;
        }
    }

    static getBasicEntityDataFromAppCookie() {
        const cookie = this.getAppCookie();
        if (cookie && cookie.app) {
            return {
                entityType: cookie.app.entityType,
                entityId: cookie.app.entityId
            }
        } else return null;
        
    }
}