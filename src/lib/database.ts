import { DATABASE_HOST, DATABASE_PASSWORD, DATABASE_USERNAME } from "$env/static/private";
import * as schemas from "$lib/schemas";
import { connect } from "@planetscale/database";
import { eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/planetscale-serverless";

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
    await db.insert(schemas.passwords).values({ id: 3, userId: user.id, website, password });
}
