import { getCallUserId } from "$lib/kv";
import type { Handle } from "@sveltejs/kit";
import { sequence } from "@sveltejs/kit/hooks";

export const handleCaller: Handle = async ({ event, resolve }) => {
    if (event.url.pathname.startsWith("/twilio")) {
        const callId = event.url.searchParams.get("CallSid");

        if (callId) {
            event.locals.callId = callId;
            event.locals.userId = await getCallUserId(callId);
        }
    }

    return resolve(event);
};

export const handle = sequence(handleCaller);
