import { kv } from "@vercel/kv";

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
