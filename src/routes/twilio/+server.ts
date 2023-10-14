import { findUserId } from "$lib/database";
import { gatherLoginSercretKey, gatherNewPhoneChoice } from "$lib/twilio.js";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    if (!phone) throw fail(400);

    const userId = await findUserId(phone);

    const response = new twilio.twiml.VoiceResponse();
    response.say("Welcome to Phone Base!");

    if (userId) {
        gatherLoginSercretKey(response);
        response.say("We didn't receive any input. Goodbye!");
    } else {
        gatherNewPhoneChoice(response);
        response.redirect({ method: "GET" }, "/twilio/register");
    }

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
