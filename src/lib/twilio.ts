import { wordList } from "$lib/word-list";
import type twilio from "twilio";

export function gatherLoginSercretKey(response: twilio.twiml.VoiceResponse) {
    const gather = response.gather({
        input: ["speech"],
        action: "/twilio/login",
        method: "GET",
        speechModel: "experimental_utterances",
        hints: wordList.join(", "),
        speechTimeout: "auto",
    });
    gather.say("Please tell us your 4 words sercret passkey.");

    return gather;
}

export function gatherNewPhoneChoice(response: twilio.twiml.VoiceResponse) {
    const gather = response.gather({
        input: ["dtmf"],
        action: "/twilio/add-phone",
        method: "GET",
    });
    gather.say(
        "If you are new to Phone Base and would like to create an account, press the # symbol. If you already have an account, compose your old phone number, followed by the # symbol."
    );

    return gather;
}
