import { DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME } from "$env/static/private";
import * as schemas from "$lib/schemas";
import { connect } from "@planetscale/database";
import { and, eq, like } from "drizzle-orm";
import { drizzle } from "drizzle-orm/planetscale-serverless";
import { generateUserId } from "./generate";

const connection = connect({
    host: DATABASE_HOST,
    username: DATABASE_USERNAME,
    password: DATABASE_PASSWORD,
});

const db = drizzle(connection, { schema: schemas });

export async function getUser(id: string | null) {
    if (!id) return null;

    try {
        const res = await db.select().from(schemas.users).where(eq(schemas.users.id, id)).limit(1);
        return res.at(0) ?? null;
    } catch {
        return null;
    }
}

export async function findUserId(phone: string) {
    const user = await db.query.phones.findFirst({
        columns: { userId: true },
        where: (phones) => eq(phones.number, phone),
    });

    return user?.userId;
}

export async function findUser(phone: string) {
    const result = await db.query.phones.findFirst({
        columns: {},
        where: (phones) => like(phones.number, `%${phone}`),
        with: { user: true },
    });

    return result?.user ?? null;
}

export async function addPassword(user: schemas.User, website: string, password: string) {
    try {
        await db.insert(schemas.passwords).values({ userId: user.id, website, password });
        return true;
    } catch {
        return false;
    }
}

export async function removePassword(user: schemas.User, website: string) {
    try {
        await db
            .delete(schemas.passwords)
            .where(
                and(eq(schemas.passwords.website, website), eq(schemas.passwords.userId, user.id))
            );
        return true;
    } catch {
        return false;
    }
}

export async function removePasswordById(user: schemas.User, id: number) {
    try {
        await db
            .delete(schemas.passwords)
            .where(and(eq(schemas.passwords.id, id), eq(schemas.passwords.userId, user.id)));
        return true;
    } catch {
        return false;
    }
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

export async function modifyPasswordById(user: schemas.User, id: number, password: string) {
    try {
        await db
            .update(schemas.passwords)
            .set({ password })
            .where(and(eq(schemas.passwords.id, id), eq(schemas.passwords.userId, user.id)));
        return true;
    } catch {
        return false;
    }
}

export async function getPassword(user: schemas.User, website: string) {
    try {
        const res = await db
            .select({ password: schemas.passwords.password })
            .from(schemas.passwords)
            .where(
                and(eq(schemas.passwords.website, website), eq(schemas.passwords.userId, user.id))
            )
            .limit(1);
        return res.at(0)?.password ?? null;
    } catch {
        return null;
    }
}

export async function getPasswordById(user: schemas.User, id: number) {
    try {
        const res = await db
            .select({ password: schemas.passwords.password })
            .from(schemas.passwords)
            .where(and(eq(schemas.passwords.id, id), eq(schemas.passwords.userId, user.id)))
            .limit(1);
        return res.at(0)?.password ?? null;
    } catch {
        return null;
    }
}

export async function createUser(phoneNumber: string, publicKey: string) {
    const id = generateUserId();

    await db.insert(schemas.users).values({ id, publicKey });
    await db.insert(schemas.phones).values({ userId: id, number: phoneNumber });

    return id;
}

export async function addPhoneNumber(oldPhoneNumber: string, newPhoneNumber: string) {
    try {
        const rows = await db
            .select({ userId: schemas.phones.userId })
            .from(schemas.phones)
            .where(like(schemas.phones.number, `%${oldPhoneNumber}`))
            .limit(1);

        if (!rows.at(1)) return false;

        await db.insert(schemas.phones).values({ userId: rows[1].userId, number: newPhoneNumber });
        return true;
    } catch {
        return false;
    }
}

export async function getAllPasswords(user: App.User) {
    return await db.select().from(schemas.passwords).where(eq(schemas.passwords.userId, user.id));
}
