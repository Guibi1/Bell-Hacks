export const load = async ({ url, cookies, depends }) => {
    depends("app:auth");

    return {
        isFr: url.pathname.startsWith("/fr"),
        lang: url.pathname.substring(1, 3),
        isLoggedIn: !!cookies.get("userId"),
    };
};
