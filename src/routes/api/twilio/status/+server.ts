import { deleteCallUserId } from "$lib/kv.js";
import { json } from "@sveltejs/kit";

export async function GET({ url }) {
    const callId = url.searchParams.get("CallSid");
    const status = url.searchParams.get("CallStatus");

    if (callId && status === "completed") {
        deleteCallUserId(callId);
    }

    return json({ success: true });
}
