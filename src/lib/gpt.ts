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
                "You are a password manager assistant and you will help the customer with their needs. Yp",
        },
        {
            role: "user",
            content: userInput,
        },
    ];

    messages.push({
        role: "user",
        content: userInput,
    });

    return chatCompletion(user, messages);
}

async function chatCompletion(user: App.User, messages: Conversation, end = false,password=null) {
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-4",
            messages,
            functions,
            max_tokens: 100,
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
                const password = generatePassword();
                if (await addPassword(user, website, password)) {
                   ;
                } else return null;
            },
            modifyPassword: async ({ website }: { website: string }) => {
                const password = generatePassword();
                if (await modifyPassword(user, website, password)) {
                    ;
                } else return null;
            },
            removePassword: async ({ website }: { website: string }) => {
                removePassword(user, website);
            },
            endCall: () => {
                end = true;
            },
        };
        password=password

        const result = functionsList[name](JSON.parse(args));
        messages.push({ role: "function", content: JSON.stringify(result), name: name });

        return chatCompletion(user, messages, end,password);
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
                "This is going to be the name of the website named by the user. It will always be the name of the website, never the url. It is not a url. And do not reprimend the user if he tells you the url, just take the name and move on. ",
        },
    },
    required: ["website"],
};

const functions = [
    {
        name: "addPassword",
        description:
            "This fonction is going to add a password to the wanted website. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "getPassword",
        description:
            "This fonction is going to retreive and return the password of the wanted website. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "removePassword",
        description:
            "This fonction is going to remove a password associated with the wanted website. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "modifyPassword",
        description:
            "This fonction is going generate a new password for the wanted website. It will return true if the process succeeded",
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
