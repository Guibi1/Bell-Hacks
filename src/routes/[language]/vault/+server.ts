import { decrypt, encrypt } from "$lib/crypto";
import {
    addPassword,
    getPasswordById,
    getUser,
    modifyPasswordById,
    removePasswordById,
} from "$lib/database";
import { error, json } from "@sveltejs/kit";
import { validate } from "sveltekit-typesafe-api/server";
import { z } from "zod";

export async function GET({ request, locals, cookies, fetch }) {
    const { data } = await validate(request, { searchParams: z.object({ id: z.coerce.number() }) });

    const user = await getUser(locals.userId);
    const privateKey = JSON.parse(cookies.get("privateKey") ?? "null");
    if (!user || !privateKey) throw error(401);

    const encrypted = await getPasswordById(user, data.searchParams.id);
    if (encrypted) {
        const password = await decrypt(fetch, privateKey, user.publicKey, encrypted);
        return json({ success: true, password });
    }

    return json({ success: true });
}

export async function POST({ request, locals }) {
    const { data } = await validate(request, { website: z.string(), password: z.string() });

    const user = await getUser(locals.userId);
    if (!user) throw error(401);

    return json({ success: await addPassword(user, data.website, data.password) });
}

export async function PUT({ request, locals, fetch }) {
    const { data } = await validate(request, { id: z.number(), password: z.string() });

    const user = await getUser(locals.userId);
    if (!user) throw error(401);

    const encrypted = await encrypt(fetch, user.publicKey, data.password);
    return json({ success: await modifyPasswordById(user, data.id, encrypted) });
}

export async function DELETE({ request, locals }) {
    const { data } = await validate(request, { id: z.number() });

    const user = await getUser(locals.userId);
    if (!user) throw error(401);

    return json({ success: await removePasswordById(user, data.id) });
}
