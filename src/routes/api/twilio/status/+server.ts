import { deleteCallUserId, deleteConversation } from "$lib/kv.js";
import { json } from "@sveltejs/kit";

export async function GET({ locals, url }) {
    const status = url.searchParams.get("CallStatus");

    if (locals.callId && status === "completed") {
        deleteCallUserId(locals.callId);
        deleteConversation(locals.callId);
    }

    return json({ success: true });
}
