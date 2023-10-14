import { DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME } from "$env/static/private";
import * as schemas from "$lib/schemas";
import { connect } from "@planetscale/database";
import { and, eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/planetscale-serverless";
import { generatePrivateKey, generateUserId } from "./generate";

const connection = connect({
    host: DATABASE_HOST,
    username: DATABASE_USERNAME,
    password: DATABASE_PASSWORD,
});

const db = drizzle(connection, { schema: schemas });

export async function findUser(phone: string) {
    const user = await db.query.phones.findFirst({
        where: (phones) => eq(phones.number, phone),
        with: { userId: true },
    });

    return user?.userId;
}

export async function addPassword(user: schemas.User, website: string, password: string) {
    return await db.insert(schemas.passwords).values({ userId: user.id, website, password });
}

export async function removePassword(user: schemas.User, website: string) {
    return await db
        .delete(schemas.passwords)
        .where(and(eq(schemas.passwords.website, website), eq(schemas.passwords.userId, user.id)));
}
export async function modifyPassword(user: schemas.User, website: string, password: string) {
    try {
        await db
            .update(schemas.passwords)
            .set({ password })
            .where(
                and(eq(schemas.passwords.website, website), eq(schemas.passwords.userId, user.id))
            );
        return true;
    } catch {
        return false;
    }
}
export async function getPassword(user: schemas.User, website: string) {
    return await db
        .select({ password: schemas.passwords.password })
        .from(schemas.passwords)
        .where(and(eq(schemas.passwords.website, website), eq(schemas.passwords.userId, user.id)));
}
export async function createUser(phoneNumber: string) {
    const id = generateUserId();
    const privatekey = generatePrivateKey();

    // const res = await fetch("/api/encrypt/private")
    const publicKey = "[12,234]";

    await db.insert(schemas.users).values({ id, publicKey });
    await db.insert(schemas.phones).values({ userId: id, number: phoneNumber });
}
