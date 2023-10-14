import { config } from "dotenv";
import type { Config } from "drizzle-kit";

config();

export default {
    schema: "./src/lib/schemas.ts",
    out: "./.drizzle",
    driver: "mysql2",
    dbCredentials: {
        connectionString: `mysql://${process.env["DATABASE_USERNAME"]}:${process.env["DATABASE_PASSWORD"]}@${process.env["DATABASE_HOST"]}/bell-hacks-2023?ssl={"rejectUnauthorized":true}`,
    },
} satisfies Config;
