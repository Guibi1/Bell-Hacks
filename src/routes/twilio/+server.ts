import { findUserId } from "$lib/database";
import { wordList } from "$lib/word-list";
import { fail, text } from "@sveltejs/kit";
import twilio from "twilio";

export async function GET({ url, setHeaders }) {
    const phone = url.searchParams.get("Caller");
    if (!phone) throw fail(400);

    const userId = await findUserId(phone);

    const response = new twilio.twiml.VoiceResponse();
    response.say("Welcome to Phone Base!");

    if (userId) {
        const gather = response.gather({
            input: ["speech"],
            action: "/twilio/login",
            method: "GET",
            speechModel: "experimental_utterances",
            hints: wordList.slice(0, 400).join(" "),
        });
        gather.say("Please tell us your 4 words sercret passkey.");

        response.say("We didn't receive any input. Goodbye!");
    } else {
        const gather = response.gather({
            input: ["dtmf"],
            action: "/twilio/add-phone",
            method: "GET",
        });
        gather.say(
            "If you are new to Phone Base and would like to create an account, press the # symbol."
        );
        gather.say(
            "If you already have an account, compose your old phone number, followed by the # symbol."
        );

        response.redirect({ method: "GET" }, "/twilio/register");
    }

    setHeaders({ "Content-Type": "text/xml" });
    return text(response.toString());
}
