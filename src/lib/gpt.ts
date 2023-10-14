import { GPT_KEY } from "$env/static/private";
import { addPassword, getPassword, modifyPassword, removePassword } from "$lib/database";
import OpenAI from "openai";
import generatePassword from "./generatePassword";

export type Conversation = OpenAI.Chat.Completions.ChatCompletionMessageParam[];
const openai = new OpenAI({ apiKey: GPT_KEY });

export async function askGPT(user: App.User, convo: Conversation | null, userInput: string) {
    const messages: Conversation = convo ?? [
        {
            role: "system",
            content:
                "You are a password manager assistant and you will help the customer with their needs.",
        },
    ];

    messages.push({
        role: "user",
        content: userInput,
    });

    return chatCompletion(user, messages);
}

async function chatCompletion(user: App.User, messages: Conversation, end = false) {
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages,
            functions,
        });

        const responseMessage = response.choices[0].message;
        messages.push(responseMessage);
        if (responseMessage.content) return { content: responseMessage.content, messages, end };

        if (!responseMessage.function_call) throw "Something went wrong...";
        const { name, arguments: args } = responseMessage.function_call;

        // eslint-disable-next-line @typescript-eslint/ban-types
        const functionsList: Record<string, Function> = {
            getPassword: async ({ website }: { website: string }) => {
                getPassword(user, website);
            },
            addPassword: async ({ website }: { website: string }) => {
                const password = generatePassword()
                if (await addPassword(user, website, password)) {
                    return password
                }
                else return null
            },
            modifyPassword: async ({ website }: { website: string }) => {
                const password = generatePassword()
                if (await modifyPassword(user, website, password)) {
                    return password
                }
                else return null
            },
            removePassword: async ({ website }: { website: string }) => {
                removePassword(user, website);
            },
            endCall: () => {
                end = true;
            },
        };

        const result = functionsList[name](JSON.parse(args));
        messages.push({ role: "function", content: JSON.stringify(result), name: name });

        return chatCompletion(user, messages, end);
    } catch (error) {
        console.error("An error occured:", error);
        throw "ChatGPT error";
    }
}

const params = {
    type: "object",
    properties: {
        website: {
            type: "string",
            description:
                "Is gonna be the name of the website the user is gonna be adding a password for",
        },
    },
    required: ["website"],
};

const functions = [
    {
        name: "addPassword",
        description:
            "Use this fonction to answer the user about his personnal information. Input is gonna the User id and the name of the website they are trying to add a website for, will return ther password or null if it didnt worked",
        parameters: params,
    },
    {
        name: "getPassword",
        description:
            "Will return password associated with the name of the Website based on the uId",
        parameters: params,
    },
    {
        name: "removePassword",
        description:
            "Will remove password associated with the name of the Website based on the uId, will return true if the pass has been succesfully deleted.",
        parameters: params,
    },
    {
        name: "modifyPassword",
        description:
            "Will modify the and generate another password associated with the name of the Website based on the uId, will return the pasword if the operation succeeded and null if it did not",
        parameters: params,
    },
    {
        name: "endCall",
        description:
            "This function will end the call with the user. Only use this function if you are sure the customer says they want to quit",
        parameters: {
            type: "object",
            properties: {},
            required: [],
        },
    },
];
