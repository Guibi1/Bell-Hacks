import { getUser } from "$lib/database";
import { askGPT } from "$lib/gpt";
import { getConversation, getPrivateKey, setConversation } from "$lib/kv";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders, fetch }) {
    const speechResult = url.searchParams.get("SpeechResult");
    const user = await getUser(locals.userId);
    if (!speechResult || !locals.callId || !locals.userId || !user) throw fail(400);
    const privateKey = await getPrivateKey(locals.callId);
    if (!privateKey) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    console.log(
        "🚀 ~ file: +server.ts:15 ~ GET ~ await getConversation(locals.userId):",
        await getConversation(locals.userId)
    );
    const answer = await askGPT(
        fetch,
        { ...user, privateKey },
        await getConversation(locals.userId),
        speechResult
    );

    response.say(answer.content);
    setConversation(locals.callId, answer.messages);

    if (!answer.end) {
        response.redirect({ method: "GET" }, "/api/twilio/ask");
    }

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
