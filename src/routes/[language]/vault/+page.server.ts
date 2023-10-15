import { getAllPasswords, getUser } from "$lib/database";
import { redirect } from "@sveltejs/kit";

export const load = async ({ locals, depends }) => {
    depends("app:passwords");

    const user = await getUser(locals.userId);
    if (!user) {
        throw redirect(302, "/");
    }

    return { passwords: await getAllPasswords(user), userId: user.id };
};
