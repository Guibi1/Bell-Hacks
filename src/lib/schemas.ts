import { relations } from "drizzle-orm";
import { mysqlTable, serial, text, uniqueIndex, varchar } from "drizzle-orm/mysql-core";

export const users = mysqlTable("users", {
    id: varchar("id", { length: 24 }).primaryKey(),
    publicKey: text("pub_key").notNull(),
});

export const passwords = mysqlTable(
    "passwords",
    {
        id: serial("id").primaryKey(),
        userId: varchar("user_id", { length: 24 }).notNull(),
        password: varchar("password", { length: 256 }).notNull(),
        website: varchar("website", { length: 512 }).notNull(),
    },
    (entry) => ({
        userIndex: uniqueIndex("user_idx").on(entry.userId),
    })
);

export const phones = mysqlTable(
    "phones",
    {
        id: serial("id").primaryKey(),
        userId: varchar("user_id", { length: 24 }).notNull(),
        number: varchar("number", { length: 64 }).notNull(),
    },
    (entry) => ({
        userIndex: uniqueIndex("user_idx").on(entry.userId),
        numberIndex: uniqueIndex("numberx").on(entry.number),
    })
);

// Relations
export const usersRelations = relations(users, ({ many }) => ({
    passwords: many(passwords),
    phones: many(phones),
}));

export const passwordsRelations = relations(passwords, ({ one }) => ({
    userId: one(users, { fields: [passwords.userId], references: [users.id] }),
}));

export const phonesRelations = relations(phones, ({ one }) => ({
    userId: one(users, { fields: [phones.userId], references: [users.id] }),
}));

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

export type Password = typeof passwords.$inferSelect;
export type InsertPassword = typeof passwords.$inferInsert;
