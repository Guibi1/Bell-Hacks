import { getCallUserId } from "$lib/kv";
import type { Handle } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";

export const handleCaller: Handle = async ({ event, resolve }) => {
    if (event.url.pathname.startsWith("/api/twilio")) {
        const caller = event.url.searchParams.get("CallSid");

        if (caller) {
            event.locals.userId = await getCallUserId(caller);
        }
    }

    return resolve(event);
};

export const handle = sequence(handleCaller);
