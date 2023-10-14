import { kv } from "@vercel/kv";
import type { Conversation } from "./gpt";

export async function getCallUserId(callId: string): Promise<string | null> {
    return await kv.get(callId);
}

export async function setCallUserId(callId: string, userId: string) {
    try {
        await kv.set(callId, userId);
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
        await kv.set("convo" + callId, messages);
        return true;
    } catch {
        return false;
    }
}

export async function deleteConversation(callId: string) {
    return (await kv.del("convo" + callId)) == 1;
}

export async function getPrivateKey(callId: string): Promise<string[] | null> {
    return await kv.get("priv" + callId);
}

export async function setPrivateKey(callId: string, messages: string[]) {
    try {
        await kv.set("priv" + callId, JSON.stringify(messages));
        return true;
    } catch {
        return false;
    }
}

export async function deletePrivateKey(callId: string) {
    return (await kv.del("priv" + callId)) == 1;
}
