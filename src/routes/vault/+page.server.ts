import { getAllPasswords, getUser } from "$lib/database";
import { redirect } from "@sveltejs/kit";

export const load = async ({ locals }) => {
    const user = await getUser(locals.userId);
    if (!user) {
        throw redirect(302, "/");
    }

    return { passwords: await getAllPasswords(user) };
};
