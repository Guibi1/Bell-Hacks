import { GPT_KEY } from "$env/static/private";
import { decrypt, encrypt } from "$lib/crypto";
import { addPassword, getPassword, modifyPassword, removePassword } from "$lib/database";
import generatePassword from "$lib/generatePassword";
import OpenAI from "openai";

export type Conversation = OpenAI.Chat.Completions.ChatCompletionMessageParam[];
const openai = new OpenAI({ apiKey: GPT_KEY });

export async function askGPT(
    f: typeof fetch,
    user: App.User & { privateKey: string[] },
    convo: Conversation | null,
    userInput: string
) {
    const messages: Conversation = convo ?? [
        {
            role: "system",
            content:
                "You are a password manager assistant and you will help the customer with their needs. However you can always try to help the usr if hes in needs. The customer is usually an elderly or a person with vision issues. Be mindful....",
        },
    ];

    messages.push({
        role: "user",
        content: userInput,
    });

    return chatCompletion(f, user, messages);
}

async function chatCompletion(
    f: typeof fetch,
    user: App.User & { privateKey: string[] },
    messages: Conversation,
    end = false,
    password?: string
) {
    if (password) {
        const content = `Your password is ${password}. Is there anything else you want today?`;
        messages.push({ role: "assistant", content });
        return { content, messages, end };
    }

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
                const passwd = await getPassword(user, website);
                if (passwd) {
                    password = await decrypt(f, user.privateKey, user.publicKey, passwd);
                    return true;
                } else return false;
            },
            addPassword: async ({ website }: { website: string }) => {
                const passwd = generatePassword();
                const encrypted = await encrypt(f, user.publicKey, passwd);
                if (await addPassword(user, website, encrypted)) {
                    password = passwd;
                    return true;
                } else return false;
            },
            modifyPassword: async ({ website }: { website: string }) => {
                const passwd = generatePassword();
                const encrypted = await encrypt(f, user.publicKey, passwd);
                if (await modifyPassword(user, website, encrypted)) {
                    password = passwd;
                    return true;
                } else return false;
            },
            removePassword: async ({ website }: { website: string }) => {
                return await removePassword(user, website);
            },
            endCall: async () => (end = true),
        };

        const result = await functionsList[name](JSON.parse(args));
        messages.push({ role: "function", content: JSON.stringify(result), name: name });

        console.log("🚀 ~ file: gpt.ts:94 ~ password:", password);
        return chatCompletion(f, user, messages, end, password);
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
            "Adds a password to the wanted website. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "getPassword",
        description:
            "Retreives the password of the wanted website and shows it to the user. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "removePassword",
        description:
            "Removes a password associated with the wanted website. It will return true if the process succeeded",
        parameters: params,
    },
    {
        name: "modifyPassword",
        description:
            "Generate a new password for the wanted website, and override the old one. It will return true if the process succeeded",
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
