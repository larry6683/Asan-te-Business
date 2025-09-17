export class CookieService {
    constructor() {}

    static setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = this.calculateExpirationTime(days)
            expires = "; expires=" + date.toUTCString();
        }
        if (value) value = JSON.stringify(value);
        document.cookie = name + "=" + (value || "{}") + expires + "; path=/";
    }

    static getCookie(name) {
        let nameEQ = name + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    static eraseCookie(name) {
        document.cookie = name + '=; Max-Age=-99999999; path=/';
    }

    static calculateExpirationTime(days) {
        if (!days)
            days = 1;

        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        return date.toUtcString();
    }
}