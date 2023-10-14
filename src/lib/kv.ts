import { kv } from "@vercel/kv";
import type { Conversation } from "./gpt";

export async function getCallUserId(callId: string): Promise<string | null> {
    return kv.get(callId);
}

export async function setCallUserId(callId: string, userId: string) {
    try {
        kv.set(callId, userId);
        return true;
    } catch {
        return false;
    }
}

export async function deleteCallUserId(callId: string) {
    return (await kv.del(callId)) == 1;
}

export async function getConversation(callId: string): Promise<Conversation | null> {
    return await kv.get("convo" + callId);
}

export async function setConversation(callId: string, messages: Conversation) {
    try {
        kv.set("convo" + callId, messages);
        return true;
    } catch {
        return false;
    }
}

export async function deleteConversation(callId: string) {
    return (await kv.del("convo" + callId)) == 1;
}
