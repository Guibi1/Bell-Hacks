import { verifyPrivateKey } from "$lib/crypto";
import { findUser } from "$lib/database";
import { setCallUserId } from "$lib/kv";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    const speechResult = url.searchParams.get("SpeechResult");
    if (!locals.callId || !phone || !speechResult) throw fail(400);

    const user = await findUser(phone);
    if (!user) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    const words = speechResult.toLowerCase().split(" ");
    if (await verifyPrivateKey(words, user.publicKey)) {
        setCallUserId(locals.callId, user.id);
        response.say("Hi, what do you want to do today?");
        response.redirect({ method: "GET" }, "/api/twilio/ask");

        setHeaders({ "Content-Type": "text/xml" });
        return text(response.toString());
    }

    const gather = response.gather({
        input: ["speech"],
        action: "/api/twilio/login",
        method: "GET",
    });
    gather.say("Incorrect passphrase. Please tell us your 4 words sercret passkey.");

    response.say("We didn't receive any input. Goodbye!");

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
