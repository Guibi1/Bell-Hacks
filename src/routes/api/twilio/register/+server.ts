import { createUser } from "$lib/database";
import { setCallUserId } from "$lib/kv.js";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ locals, url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    if (!locals.callId || !phone) throw fail(400);

    const response = new twilio.twiml.VoiceResponse();

    const { id, privateKey } = await createUser(phone);
    await setCallUserId(locals.callId, id);

    response.say("Your account has been successfully created.");
    response.say("You will now hear your secret key twice.");
    response.say(
        "Make sure to remember the four words, as this is the only time that Phone Base will provide them to you."
    );
    response.pause({ length: 2 });

    for (let i = 0; i < 2; i++) {
        for (let j = 0; j < privateKey.length; j++) {
            response.say(privateKey[j]);
            response.pause({ length: 1 });
        }
    }

    response.say("You will now be redirected to the main menu. Thank you for using Phone Base!");
    response.pause({ length: 1 });

    response.say("Hi, what do you want to do today?");
    response.redirect({ method: "GET" }, "/api/twilio/ask");

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
