import { verifyPrivateKey } from "$lib/crypto";
import { findUser } from "$lib/database";
import { error, json } from "@sveltejs/kit";
import { validate } from "sveltekit-typesafe-api/server";
import { z } from "zod";

export async function POST({ request, cookies, fetch }) {
    const { data } = await validate(request, {
        phone: z.string(),
        privateKey: z.string().array().length(4),
    });

    const user = await findUser(data.phone);
    if (!user) {
        throw error(401);
    }

    if (await verifyPrivateKey(fetch, data.privateKey, user.publicKey)) {
        cookies.set("userId", user.id, { path: "/", sameSite: true, secure: true });
        cookies.set("privateKey", JSON.stringify(data.privateKey), {
            path: "",
            sameSite: true,
            secure: true,
        });
        return json({ success: true });
    }

    return json({ success: false, invalidPassword: true });
}
